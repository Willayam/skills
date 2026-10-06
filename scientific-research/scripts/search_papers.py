#!/usr/bin/env python3
"""
Search academic databases for scientific papers.
Queries OpenAlex, Semantic Scholar, and optionally PubMed in parallel.
Returns merged, deduplicated results with funding data.
"""

import argparse
import json
import sys
import urllib.request
import urllib.parse
import urllib.error
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, as_completed


def search_openalex(query, limit=10, year_from=None, year_to=None, open_access=False):
    """Search OpenAlex for papers with funding data."""
    params = {
        "search": query,
        "per_page": min(limit, 50),
        "select": ",".join([
            "id", "doi", "title", "display_name", "publication_year",
            "publication_date", "authorships", "cited_by_count",
            "primary_location", "open_access", "type",
            "funders", "awards", "is_retracted", "abstract_inverted_index",
            "keywords", "topics"
        ]),
        "sort": "relevance_score:desc",
        "mailto": "your-email@example.com",  # Replace with your email for polite API access,
    }

    filters = []
    if year_from:
        filters.append(f"publication_year:>{int(year_from) - 1}")
    if year_to:
        filters.append(f"publication_year:<{int(year_to) + 1}")
    if open_access:
        filters.append("open_access.is_oa:true")
    if filters:
        params["filter"] = ",".join(filters)

    url = f"https://api.openalex.org/works?{urllib.parse.urlencode(params)}"

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "LifeOS-Research/1.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
    except Exception as e:
        return {"source": "openalex", "error": str(e), "papers": []}

    papers = []
    for work in data.get("results", []):
        # Reconstruct abstract from inverted index
        abstract = ""
        inv_idx = work.get("abstract_inverted_index")
        if inv_idx:
            word_positions = []
            for word, positions in inv_idx.items():
                for pos in positions:
                    word_positions.append((pos, word))
            word_positions.sort()
            abstract = " ".join(w for _, w in word_positions)

        # Extract authors
        authors = []
        for authorship in work.get("authorships", [])[:10]:
            author = authorship.get("author", {})
            name = author.get("display_name", "Unknown")
            authors.append(name)

        # Extract journal/source
        location = work.get("primary_location") or {}
        source = location.get("source") or {}
        journal = source.get("display_name", "Unknown")

        # Extract funders
        funders = []
        for funder in work.get("funders", []):
            funders.append({
                "name": funder.get("display_name", "Unknown"),
                "id": funder.get("id", ""),
            })

        # Extract awards/grants
        awards = []
        for award in work.get("awards", []):
            awards.append({
                "name": award.get("display_name", ""),
                "funder": award.get("funder_display_name", ""),
                "award_id": award.get("funder_award_id", ""),
            })

        doi = work.get("doi", "")
        if doi and doi.startswith("https://doi.org/"):
            doi = doi[len("https://doi.org/"):]

        papers.append({
            "title": work.get("display_name", work.get("title", "Untitled")),
            "authors": authors,
            "year": work.get("publication_year"),
            "journal": journal,
            "doi": doi,
            "cited_by_count": work.get("cited_by_count", 0),
            "type": work.get("type", "unknown"),
            "is_retracted": work.get("is_retracted", False),
            "open_access": work.get("open_access", {}).get("is_oa", False),
            "abstract": abstract[:500] if abstract else "",
            "funders": funders,
            "awards": awards,
            "topics": [t.get("display_name", "") for t in work.get("topics", [])[:5]],
            "source": "openalex",
        })

    return {"source": "openalex", "count": len(papers), "papers": papers}


def search_semantic_scholar(query, limit=10, year_from=None, year_to=None):
    """Search Semantic Scholar for papers with citation metrics."""
    params = {
        "query": query,
        "limit": min(limit, 100),
        "fields": "title,authors,year,abstract,citationCount,influentialCitationCount,externalIds,venue,publicationTypes,openAccessPdf,journal,isOpenAccess",
    }

    if year_from:
        params["year"] = f"{year_from}-"
        if year_to:
            params["year"] = f"{year_from}-{year_to}"
    elif year_to:
        params["year"] = f"-{year_to}"

    url = f"https://api.semanticscholar.org/graph/v1/paper/search?{urllib.parse.urlencode(params)}"

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "LifeOS-Research/1.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
    except Exception as e:
        return {"source": "semantic_scholar", "error": str(e), "papers": []}

    papers = []
    for paper in data.get("data", []):
        authors = [a.get("name", "Unknown") for a in paper.get("authors", [])[:10]]
        ext_ids = paper.get("externalIds", {}) or {}
        doi = ext_ids.get("DOI", "")

        journal_info = paper.get("journal") or {}
        journal = journal_info.get("name", paper.get("venue", "Unknown"))

        papers.append({
            "title": paper.get("title", "Untitled"),
            "authors": authors,
            "year": paper.get("year"),
            "journal": journal,
            "doi": doi,
            "cited_by_count": paper.get("citationCount", 0),
            "influential_citation_count": paper.get("influentialCitationCount", 0),
            "type": (paper.get("publicationTypes") or ["unknown"])[0] if paper.get("publicationTypes") else "unknown",
            "open_access": paper.get("isOpenAccess", False),
            "abstract": (paper.get("abstract") or "")[:500],
            "funders": [],
            "awards": [],
            "source": "semantic_scholar",
            "pubmed_id": ext_ids.get("PubMed", ""),
        })

    return {"source": "semantic_scholar", "count": len(papers), "papers": papers}


def search_pubmed(query, limit=10, year_from=None, year_to=None):
    """Search PubMed for papers with grant and COI data."""
    # Step 1: Search for PMIDs
    search_params = {
        "db": "pubmed",
        "term": query,
        "retmax": min(limit, 100),
        "retmode": "json",
        "sort": "relevance",
    }
    if year_from:
        search_params["mindate"] = f"{year_from}/01/01"
        search_params["datetype"] = "pdat"
    if year_to:
        search_params["maxdate"] = f"{year_to}/12/31"
        search_params["datetype"] = "pdat"

    search_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?{urllib.parse.urlencode(search_params)}"

    try:
        req = urllib.request.Request(search_url, headers={"User-Agent": "LifeOS-Research/1.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            search_data = json.loads(resp.read().decode())
    except Exception as e:
        return {"source": "pubmed", "error": f"Search failed: {e}", "papers": []}

    pmids = search_data.get("esearchresult", {}).get("idlist", [])
    if not pmids:
        return {"source": "pubmed", "count": 0, "papers": []}

    # Step 2: Fetch full records with grant and COI data
    fetch_params = {
        "db": "pubmed",
        "id": ",".join(pmids),
        "rettype": "xml",
    }
    fetch_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?{urllib.parse.urlencode(fetch_params)}"

    try:
        req = urllib.request.Request(fetch_url, headers={"User-Agent": "LifeOS-Research/1.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            xml_data = resp.read().decode()
    except Exception as e:
        return {"source": "pubmed", "error": f"Fetch failed: {e}", "papers": []}

    # Parse XML
    papers = []
    try:
        root = ET.fromstring(xml_data)
    except ET.ParseError as e:
        return {"source": "pubmed", "error": f"XML parse failed: {e}", "papers": []}

    for article in root.findall(".//PubmedArticle"):
        medline = article.find("MedlineCitation")
        if medline is None:
            continue

        # PMID
        pmid_el = medline.find("PMID")
        pmid = pmid_el.text if pmid_el is not None else ""

        # Article info
        art = medline.find("Article")
        if art is None:
            continue

        title_el = art.find("ArticleTitle")
        title = title_el.text if title_el is not None else "Untitled"

        # Journal
        journal_el = art.find(".//Journal/Title")
        journal = journal_el.text if journal_el is not None else "Unknown"

        # Year
        year = None
        pub_date = art.find(".//PubDate/Year")
        if pub_date is not None:
            try:
                year = int(pub_date.text)
            except (ValueError, TypeError):
                pass

        # Authors
        authors = []
        for author in art.findall(".//AuthorList/Author")[:10]:
            last = author.find("LastName")
            first = author.find("ForeName")
            if last is not None:
                name = last.text
                if first is not None:
                    name = f"{first.text} {last.text}"
                authors.append(name)

        # Abstract
        abstract_parts = []
        for abs_text in art.findall(".//Abstract/AbstractText"):
            label = abs_text.get("Label", "")
            text = abs_text.text or ""
            if label:
                abstract_parts.append(f"{label}: {text}")
            else:
                abstract_parts.append(text)
        abstract = " ".join(abstract_parts)[:500]

        # DOI
        doi = ""
        for id_el in art.findall(".//ELocationID"):
            if id_el.get("EIdType") == "doi":
                doi = id_el.text or ""
                break
        if not doi:
            pub_data = article.find("PubmedData")
            if pub_data is not None:
                for art_id in pub_data.findall(".//ArticleId"):
                    if art_id.get("IdType") == "doi":
                        doi = art_id.text or ""
                        break

        # Grants
        grants = []
        for grant in art.findall(".//GrantList/Grant"):
            grant_id = grant.find("GrantID")
            agency = grant.find("Agency")
            country = grant.find("Country")
            grants.append({
                "grant_id": grant_id.text if grant_id is not None else "",
                "agency": agency.text if agency is not None else "",
                "country": country.text if country is not None else "",
            })

        # Conflict of Interest statement
        coi = ""
        coi_el = medline.find(".//CoiStatement")
        if coi_el is not None:
            coi = coi_el.text or ""

        papers.append({
            "title": title,
            "authors": authors,
            "year": year,
            "journal": journal,
            "doi": doi,
            "pubmed_id": pmid,
            "cited_by_count": 0,  # PubMed doesn't provide this
            "abstract": abstract,
            "funders": [{"name": g["agency"], "country": g.get("country", "")} for g in grants],
            "grants": grants,
            "conflict_of_interest": coi,
            "source": "pubmed",
        })

    return {"source": "pubmed", "count": len(papers), "papers": papers}


def merge_and_deduplicate(results_list):
    """Merge papers from multiple sources, deduplicating by DOI."""
    seen_dois = {}
    all_papers = []

    for result in results_list:
        for paper in result.get("papers", []):
            doi = paper.get("doi", "")
            if doi and doi in seen_dois:
                # Merge data from duplicate: take the richer version
                existing = seen_dois[doi]
                # Keep higher citation count
                if paper.get("cited_by_count", 0) > existing.get("cited_by_count", 0):
                    existing["cited_by_count"] = paper["cited_by_count"]
                # Merge funders
                existing_funder_names = {f["name"] for f in existing.get("funders", [])}
                for funder in paper.get("funders", []):
                    if funder["name"] not in existing_funder_names:
                        existing.setdefault("funders", []).append(funder)
                # Take COI if we didn't have one
                if paper.get("conflict_of_interest") and not existing.get("conflict_of_interest"):
                    existing["conflict_of_interest"] = paper["conflict_of_interest"]
                # Take grants if we didn't have them
                if paper.get("grants") and not existing.get("grants"):
                    existing["grants"] = paper["grants"]
                # Merge sources
                if paper["source"] not in existing.get("sources_found_in", []):
                    existing.setdefault("sources_found_in", []).append(paper["source"])
                # Take influential_citation_count if available
                if paper.get("influential_citation_count"):
                    existing["influential_citation_count"] = paper["influential_citation_count"]
            else:
                paper["sources_found_in"] = [paper["source"]]
                if doi:
                    seen_dois[doi] = paper
                all_papers.append(paper)

    # Sort by citation count (descending)
    all_papers.sort(key=lambda p: p.get("cited_by_count", 0), reverse=True)

    return all_papers


def flag_funding_concerns(papers):
    """Add funding concern flags to papers."""
    # Known industry/pharma entities (partial match, case-insensitive)
    industry_keywords = [
        "pharma", "pfizer", "novartis", "roche", "merck", "johnson & johnson",
        "astrazeneca", "glaxo", "gsk", "sanofi", "bayer", "abbott", "amgen",
        "gilead", "bristol-myers", "eli lilly", "novo nordisk",
        "coca-cola", "pepsi", "nestle", "unilever", "mars", "danone",
        "monsanto", "dupont", "basf",
        "exxon", "shell", "bp", "chevron", "total",
        "facebook", "meta platforms", "google", "alphabet", "amazon", "apple", "microsoft",
        "tobacco", "philip morris", "altria", "british american tobacco",
    ]

    for paper in papers:
        concerns = []
        funders = paper.get("funders", [])

        for funder in funders:
            name = funder.get("name", "").lower()
            for keyword in industry_keywords:
                if keyword in name:
                    concerns.append(f"Industry funding: {funder.get('name', 'Unknown')}")
                    break

        paper["funding_concerns"] = concerns
        paper["has_funding_concerns"] = len(concerns) > 0

    return papers


def main():
    parser = argparse.ArgumentParser(description="Search academic databases for scientific papers")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--limit", type=int, default=10, help="Results per source (default: 10)")
    parser.add_argument("--pubmed", action="store_true", help="Include PubMed (adds COI data, slower)")
    parser.add_argument("--year-from", type=int, help="Papers from this year onward")
    parser.add_argument("--year-to", type=int, help="Papers up to this year")
    parser.add_argument("--open-access", action="store_true", help="Prefer open access papers")

    args = parser.parse_args()

    # Build search tasks
    tasks = {}
    with ThreadPoolExecutor(max_workers=3) as executor:
        tasks["openalex"] = executor.submit(
            search_openalex, args.query, args.limit, args.year_from, args.year_to, args.open_access
        )
        tasks["semantic_scholar"] = executor.submit(
            search_semantic_scholar, args.query, args.limit, args.year_from, args.year_to
        )
        if args.pubmed:
            tasks["pubmed"] = executor.submit(
                search_pubmed, args.query, args.limit, args.year_from, args.year_to
            )

        results = []
        errors = []
        for name, future in tasks.items():
            try:
                result = future.result(timeout=60)
                if "error" in result:
                    errors.append({"source": name, "error": result["error"]})
                results.append(result)
            except Exception as e:
                errors.append({"source": name, "error": str(e)})

    # Merge and deduplicate
    papers = merge_and_deduplicate(results)

    # Flag funding concerns
    papers = flag_funding_concerns(papers)

    # Filter retracted papers
    retracted = [p for p in papers if p.get("is_retracted")]
    papers = [p for p in papers if not p.get("is_retracted")]

    output = {
        "query": args.query,
        "total_results": len(papers),
        "sources_searched": list(tasks.keys()),
        "papers": papers,
        "retracted_papers": retracted,
        "errors": errors,
    }

    print(json.dumps(output, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
