/* Comment bar for throwaway builds, so the user can look, dictate and copy their notes into the chat.
 *
 *   <script src="comment.js" data-title="Fan tools" data-options="A Tight fan, B Loose fan"></script>
 *
 * data-options lists the versions. Add =url to open another page: "A Tight fan=a.html, B Loose fan=b.html".
 * Without a url, the page switches itself. Picking B sets <html data-option="B"> and window.labOption,
 * fires a window "labOption" event with detail.id, and writes ?option=B to the URL.
 * On a phone or in a narrow window the bar fills the bottom of the screen and the page gets room to scroll past it.
 * A full-height layout should subtract the bar itself: height: calc(100dvh - var(--lab-comment-bar, 0px)).
 * ?bare=1 hides the bar and keeps the option switching. Copy includes the full URL, so sliders that write to the query string get reported.
 *
 * The field stays open with the cursor in it. A phone may raise its keyboard only after a first tap on the field
 * or an option. Next and the return key then move on and keep the cursor there.
 */
(function () {
  if (window.__labComment) return;
  window.__labComment = true;
  var bare = window.__labBare || /[?&]bare=1/.test(location.search);

  var data = (document.currentScript && document.currentScript.dataset) || {};
  var title = data.title || document.title || "this page";
  var options = (data.options || "").split(",").map(parseOption).filter(Boolean);
  var storeKey = "lab-comment:" + location.pathname.replace(/[^/]*$/, "") + title;
  var store = read();
  var current = firstOption();

  function parseOption(text) {
    text = text.trim();
    if (!text) return null;
    var eq = text.indexOf("=");
    var label = (eq > 0 ? text.slice(0, eq) : text).trim();
    return { id: label.split(/\s+/)[0], label: label, href: eq > 0 ? text.slice(eq + 1).trim() : "" };
  }

  function read() {
    try {
      var saved = JSON.parse(localStorage.getItem(storeKey) || "{}");
      return { notes: saved.notes || {}, open: saved.open !== false, last: saved.last || "" };
    } catch (e) {
      return { notes: {}, open: true, last: "" };
    }
  }

  function write() {
    try { localStorage.setItem(storeKey, JSON.stringify(store)); } catch (e) { /* private mode: notes last for this page view */ }
  }

  function find(id) {
    return options.filter(function (o) { return o.id === id; })[0];
  }

  function firstOption() {
    if (!options.length) return { id: "page", label: "", href: "" };
    var byPage = options.filter(function (o) {
      return o.href && new URL(o.href, location.href).pathname === location.pathname;
    })[0];
    var query = new URLSearchParams(location.search).get("option");
    return byPage || find(query) || find(store.last) || options[0];
  }

  function announce() {
    document.documentElement.setAttribute("data-option", current.id);
    window.labOption = current.id;
    window.dispatchEvent(new CustomEvent("labOption", { detail: { id: current.id } }));
  }

  // Stills and clips hide the bar, but the page still has to show the option it was asked for.
  if (bare) {
    announce();
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", announce);
    return;
  }

  // Without this a phone lays the page out 980 px wide, shrinks the bar and zooms when the field takes focus.
  if (!document.querySelector("meta[name=viewport]")) {
    var viewport = document.createElement("meta");
    viewport.name = "viewport";
    viewport.content = "width=device-width,initial-scale=1";
    document.head.appendChild(viewport);
  }

  var FULL_WIDTH = "(max-width:700px),(pointer:coarse)";
  var host = document.createElement("div");
  host.id = "lab-comment";
  var root = host.attachShadow({ mode: "open" });
  root.innerHTML =
    "<style>" +
    ":host{all:initial;-webkit-text-size-adjust:100%;text-size-adjust:100%;position:fixed;z-index:2147483647;left:0;right:0;height:0;bottom:0;font:14px/1.3 -apple-system,BlinkMacSystemFont,'Segoe UI',system-ui,sans-serif}" +
    ".dock{position:absolute;right:max(12px,env(safe-area-inset-right));bottom:max(12px,env(safe-area-inset-bottom));box-sizing:border-box;max-width:calc(100vw - 24px);display:flex;flex-direction:column;gap:6px;padding:6px;background:#1c1c1e;color:#f5f5f7;border:1px solid rgba(255,255,255,.18);border-radius:16px}" +
    ".dock.open{width:min(440px,calc(100vw - 24px))}" +
    ".dock:not(.open) .field,.dock:not(.open) .copy,.dock:not(.open) .next,.dock:not(.open) .clear,.dock.open .toggle{display:none!important}" +
    ".field{position:relative;display:flex}" +
    "textarea{box-sizing:border-box;width:100%;min-height:44px;max-height:28vh;resize:none;padding:11px 44px 11px 10px;border:0;border-radius:10px;background:#2c2c2e;color:inherit;font-size:16px;line-height:1.35;font-family:inherit}" +
    "textarea::placeholder{color:#8e8e93}" +
    ".row{display:flex;align-items:center;gap:6px}.opts{display:flex;gap:4px;overflow-x:auto;scrollbar-width:none;min-width:0}.opts::-webkit-scrollbar{display:none}" +
    ".spacer{flex:1}" +
    "button{position:relative;flex:none;min-width:34px;height:34px;padding:0 11px;border:0;border-radius:10px;background:#2c2c2e;color:inherit;font:inherit;font-weight:600;cursor:pointer;-webkit-tap-highlight-color:transparent;touch-action:manipulation}" +
    "@media (hover:hover){button:hover{background:#3a3a3c}}" +
    "@media (pointer:coarse){button{min-width:44px;height:44px}}" +
    "button:focus-visible,textarea:focus-visible{outline:2px solid #f5f5f7;outline-offset:1px}" +
    "button[aria-pressed=true]{background:#f5f5f7;color:#1c1c1e}" +
    "button.has::after{content:'';position:absolute;top:5px;right:5px;width:6px;height:6px;border-radius:50%;background:currentColor}" +
    "button[disabled]{opacity:.45;cursor:default}" +
    ".hide{position:absolute;top:4px;right:4px;width:36px;height:36px;min-width:0;padding:0;display:flex;align-items:center;justify-content:center;background:transparent;color:#aeaeb2}" +
    "[hidden]{display:none!important}" +
    "@media " + FULL_WIDTH + "{" +
    ".dock,.dock.open{left:0;right:0;width:auto;max-width:none;bottom:0;border-width:1px 0 0;border-radius:16px 16px 0 0;padding:8px 12px max(8px,env(safe-area-inset-bottom))}" +
    ".opts{flex:1}.opts button{flex:1 0 44px}.opts:not([hidden])+.spacer{display:none}" +
    "}" +
    "</style>" +
    "<div class='dock'>" +
    "<div class='field'><textarea rows='1' autocapitalize='sentences' aria-label='Comment'></textarea>" +
    "<button class='hide' type='button' aria-label='Hide comment box' title='Hide'><svg width='14' height='14' viewBox='0 0 14 14' fill='none' stroke='currentColor' stroke-width='1.8' stroke-linecap='round' aria-hidden='true'><path d='M2.5 2.5l9 9M11.5 2.5l-9 9'/></svg></button></div>" +
    "<div class='row'><div class='opts'></div><span class='spacer'></span>" +
    "<button class='toggle' type='button'>Comment</button>" +
    "<button class='next' type='button'>Next</button>" +
    "<button class='clear' type='button' hidden>Clear</button>" +
    "<button class='copy' type='button'>Copy all</button></div>" +
    "</div>";

  var dock = root.querySelector(".dock");
  var box = root.querySelector("textarea");
  var opts = root.querySelector(".opts");
  var toggle = root.querySelector(".toggle");
  var copyBtn = root.querySelector(".copy");
  var clearBtn = root.querySelector(".clear");
  var nextBtn = root.querySelector(".next");
  var clearing = false;
  var clearTimer = 0;

  options.forEach(function (o) {
    var b = document.createElement("button");
    b.type = "button";
    b.textContent = o.id;
    b.title = o.label;
    b.setAttribute("aria-label", o.label);
    b.onclick = function () { pick(o); };
    opts.appendChild(b);
  });
  if (!options.length) opts.hidden = true;
  if (options.length > 1) box.enterKeyHint = "next";

  function hasNotes() {
    return Object.keys(store.notes).some(function (k) { return store.notes[k].trim(); });
  }

  function paint() {
    Array.prototype.forEach.call(opts.children, function (b, i) {
      var o = options[i];
      b.setAttribute("aria-pressed", o.id === current.id ? "true" : "false");
      b.classList.toggle("has", !!(store.notes[o.id] || "").trim());
    });
    dock.classList.toggle("open", store.open);
    box.placeholder = current.label ? "Comment on " + current.label : "Comment";
    if (box.value !== (store.notes[current.id] || "")) box.value = store.notes[current.id] || "";
    copyBtn.disabled = !hasNotes();
    nextBtn.hidden = options.length < 2 || clearing;
    clearBtn.hidden = !clearing;
    grow();
    reserve();
  }

  var spacer = document.createElement("div");
  spacer.setAttribute("aria-hidden", "true");

  function reserve() {
    if (!document.body) return;
    if (spacer.parentNode !== document.body) document.body.appendChild(spacer);
    var height = window.matchMedia(FULL_WIDTH).matches ? dock.offsetHeight : 0;
    spacer.style.cssText = "flex:none;pointer-events:none;height:" + height + "px";
    document.documentElement.style.setProperty("--lab-comment-bar", height + "px");
  }

  function grow() {
    box.style.height = "auto";
    box.style.height = box.scrollHeight + "px";
  }

  function pick(o) {
    if (o.id === current.id) {
      if (store.open) focusField();
      return;
    }
    current = o;
    store.last = o.id;
    write();
    if (o.href && new URL(o.href, location.href).pathname !== location.pathname) {
      location.href = o.href;
      return;
    }
    if (!o.href) {
      var url = new URL(location.href);
      url.searchParams.set("option", o.id);
      history.replaceState(history.state, "", url);
      announce();
    }
    paint();
    if (store.open) focusField();
  }

  // iOS scrolls the whole page up by the keyboard's height when a field takes focus, unless focus asks it not to.
  // An iPhone can also focus the field on load with no keyboard, which needs a fresh focus inside the tap.
  function keyboardUp() {
    return !!window.visualViewport && window.innerHeight - window.visualViewport.height > 120;
  }

  function focusField() {
    if (root.activeElement === box) {
      if (keyboardUp()) return;
      box.blur();
    }
    box.focus({ preventScroll: true });
  }

  box.addEventListener("touchend", function (e) {
    if (keyboardUp()) return;
    e.preventDefault();
    focusField();
  }, { passive: false });

  function next() {
    pick(options[(options.indexOf(current) + 1) % options.length]);
  }

  function setOpen(open) {
    store.open = open;
    write();
    paint();
    if (open) focusField();
  }

  function compile() {
    var lines = ["Comments on " + title, location.href, ""];
    var list = options.length ? options : [current];
    list.forEach(function (o) {
      var note = (store.notes[o.id] || "").trim();
      if (note) lines.push((o.label ? o.label + ": " : "") + note);
    });
    return lines.join("\n");
  }

  function copyText(text) {
    function fallback() {
      var t = document.createElement("textarea");
      t.value = text;
      t.style.cssText = "position:fixed;top:0;left:0;opacity:0;font-size:16px";
      root.appendChild(t);
      t.focus();
      t.setSelectionRange(0, text.length);
      var ok = false;
      try { ok = document.execCommand("copy"); } catch (e) { /* reported below */ }
      t.remove();
      return ok;
    }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      return navigator.clipboard.writeText(text).then(function () { return true; }, fallback);
    }
    return Promise.resolve(fallback());
  }

  box.addEventListener("input", function () {
    store.notes[current.id] = box.value;
    write();
    paint();
  });
  toggle.onclick = function () { setOpen(true); };
  root.querySelector(".hide").onclick = function () { setOpen(false); };
  nextBtn.onclick = next;
  box.addEventListener("keydown", function (e) {
    if (e.key === "Enter" && !e.shiftKey && !e.isComposing && options.length > 1) {
      e.preventDefault();
      next();
    }
  });
  copyBtn.onclick = function () {
    copyText(compile()).then(function (ok) {
      copyBtn.textContent = ok ? "Copied" : "Copy failed";
      setTimeout(function () { copyBtn.textContent = "Copy all"; }, 1800);
      clearing = ok;
      clearTimeout(clearTimer);
      clearTimer = setTimeout(function () { clearing = false; paint(); }, 6000);
      paint();
    });
  };
  clearBtn.onclick = function () {
    store.notes = {};
    clearing = false;
    write();
    paint();
    focusField();
  };

  // Keys on a Mac: return moves to the next option, shift-return adds a line, Esc hides the box and c brings it back.
  document.addEventListener("keydown", function (e) {
    var el = e.composedPath ? e.composedPath()[0] : e.target;
    var typing = el && (el.isContentEditable || /^(input|textarea|select)$/i.test(el.tagName || ""));
    if (e.key === "Escape" && store.open) { setOpen(false); return; }
    if (e.key === "c" && !typing && !store.open && !e.metaKey && !e.ctrlKey && !e.altKey) {
      e.preventDefault();
      setOpen(true);
    }
  });

  // iOS leaves position:fixed behind the keyboard, so lift the bar by the height the keyboard takes.
  var view = window.visualViewport;
  if (view) {
    var place = function () {
      var hidden = Math.max(0, window.innerHeight - view.height - view.offsetTop);
      dock.style.transform = hidden ? "translateY(" + -hidden + "px)" : "";
    };
    view.addEventListener("resize", place);
    view.addEventListener("scroll", place);
  }

  document.documentElement.appendChild(host);
  paint();
  window.addEventListener("resize", reserve);
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", reserve);
  if (store.open) focusField();
  announce();
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", announce);
})();
