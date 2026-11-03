#!/usr/bin/env node
// Capture pages as one labelled video that plays on phones, or as stills.
//
//   node capture.mjs clip out.mp4 --size 960x540 --seconds 6 "A Tight fan=a.html" "B Loose fan=b.html"
//   node capture.mjs still outdir --size 1440x900 "A Tight fan=a.html" "B Loose fan=https://..."
//
// Both:  --size WxH (default 1280x720)  --scale N  --dark  --wait MS (after load)
// clip:  --seconds N (default 6)  --speed 0.5  --run "JS to run at the start"
//        --crop WxH+X+Y (CSS px, the part of the page to keep)
//        --stack (one 1920x1080 clip with the options in sync, instead of out-a.mp4, out-b.mp4 and so on)
//
// T3 draws an embedded video in a 16:9 box, so a clip of any other shape shows small there.
// Use a 16:9 --size, or --crop a 16:9 region around what moves.
// still: --full (whole page height)
//
// Needs Node 22+, Chrome, and ffmpeg for clips. Prints each page's errors and any sideways scroll.
import { spawn, spawnSync } from "node:child_process";
import { existsSync, mkdirSync, mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { homedir, tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { pathToFileURL } from "node:url";

const USAGE = "usage: capture.mjs clip out.mp4|still outdir [flags] \"A Name=url-or-file\" ...";
const VALUE_FLAGS = new Set(["size", "scale", "wait", "seconds", "speed", "run", "crop"]);
const BOOL_FLAGS = new Set(["dark", "full", "stack"]);

function parseArgs(argv) {
  const [mode, out, ...rest] = argv;
  if (!["clip", "still"].includes(mode) || !out) die(USAGE);
  const flags = {};
  const options = [];
  for (let i = 0; i < rest.length; i++) {
    const a = rest[i];
    if (a.startsWith("--")) {
      const name = a.slice(2);
      if (BOOL_FLAGS.has(name)) flags[name] = true;
      else if (VALUE_FLAGS.has(name) && i + 1 < rest.length) flags[name] = rest[++i];
      else die(`unknown flag ${a}\n${USAGE}`);
    } else {
      const eq = a.indexOf("=");
      if (eq < 1) die(`bad option "${a}", expected "A Name=url"`);
      const label = a.slice(0, eq).trim();
      const target = a.slice(eq + 1).trim();
      options.push({ label, url: /^[a-z]+:/i.test(target) ? target : fileUrl(target) });
    }
  }
  if (!options.length) die(USAGE);
  const size = /^(\d+)x(\d+)$/.exec(flags.size || "1280x720");
  if (!size) die(`bad --size ${flags.size}, expected WxH`);
  const w = +size[1];
  const h = +size[2];
  const defaultScale = mode === "clip" || w < 800 ? 2 : 1;
  const crop = flags.crop ? /^(\d+)x(\d+)\+(\d+)\+(\d+)$/.exec(flags.crop) : null;
  if (flags.crop && !crop) die(`bad --crop ${flags.crop}, expected WxH+X+Y`);
  return {
    mode, out, options, w, h,
    scale: +(flags.scale || defaultScale),
    dark: !!flags.dark,
    full: !!flags.full,
    wait: +(flags.wait ?? (mode === "clip" ? 500 : 1200)),
    seconds: +(flags.seconds || 6),
    stack: !!flags.stack,
    crop: crop ? { w: +crop[1], h: +crop[2], x: +crop[3], y: +crop[4] } : { w, h, x: 0, y: 0 },
    speed: +(flags.speed || 1),
    run: flags.run || "",
  };
}

function fileUrl(p) {
  const cut = p.search(/[?#]/);
  const path = cut < 0 ? p : p.slice(0, cut);
  const abs = resolve(path);
  if (!existsSync(abs)) die(`no such file: ${abs}`);
  return pathToFileURL(abs).href + (cut < 0 ? "" : p.slice(cut));
}

function die(msg) {
  console.error(msg);
  process.exit(2);
}

function findChrome() {
  const known = [
    process.env.CHROME,
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium",
  ];
  const exe = known.find((p) => p && existsSync(p));
  if (!exe) die("Chrome not found. Set CHROME to its path.");
  return exe;
}

async function startChrome(dir) {
  const proc = spawn(findChrome(), [
    "--headless=new", "--remote-debugging-port=0", `--user-data-dir=${join(dir, "profile")}`,
    "--hide-scrollbars", "--no-first-run", "--mute-audio", "--autoplay-policy=no-user-gesture-required",
    "--disable-background-timer-throttling", "--disable-renderer-backgrounding", "about:blank",
  ], { stdio: ["ignore", "ignore", "pipe"] });
  const port = await new Promise((ok, fail) => {
    let log = "";
    const timer = setTimeout(() => fail(new Error(`Chrome did not start:\n${log}`)), 20000);
    proc.stderr.on("data", (chunk) => {
      log += chunk;
      const m = /DevTools listening on ws:\/\/[^:]+:(\d+)/.exec(log);
      if (m) { clearTimeout(timer); ok(+m[1]); }
    });
  });
  return { proc, port };
}

async function openPage(port) {
  const res = await fetch(`http://127.0.0.1:${port}/json/new?about:blank`, { method: "PUT" });
  const { webSocketDebuggerUrl: url } = await res.json();
  const ws = new WebSocket(url);
  await new Promise((ok, fail) => { ws.onopen = ok; ws.onerror = fail; });
  let id = 0;
  const waiting = new Map();
  const handlers = new Map();
  ws.onmessage = (e) => {
    const m = JSON.parse(e.data);
    if (m.id && waiting.has(m.id)) {
      const { ok, fail } = waiting.get(m.id);
      waiting.delete(m.id);
      if (m.error) fail(new Error(m.error.message)); else ok(m.result);
    } else if (m.method && handlers.has(m.method)) {
      handlers.get(m.method)(m.params);
    }
  };
  return {
    send: (method, params = {}) => new Promise((ok, fail) => {
      waiting.set(++id, { ok, fail });
      ws.send(JSON.stringify({ id, method, params }));
    }),
    on: (method, fn) => handlers.set(method, fn),
    close: () => ws.close(),
  };
}

const sleep = (ms) => new Promise((ok) => setTimeout(ok, ms));

function labelScript(label, a) {
  const left = a.crop.x + 10;
  const bottom = a.h - (a.crop.y + a.crop.h) + 10;
  return `window.__labBare = true;
addEventListener("DOMContentLoaded", function () {
  ${label ? `var d = document.createElement("div");
  d.textContent = ${JSON.stringify(label)};
  d.style.cssText = "all:initial;position:fixed;left:${left}px;bottom:${bottom}px;z-index:2147483647;pointer-events:none;background:#fff;color:#111;font:600 13px/1 -apple-system,system-ui,sans-serif;padding:6px 8px;border-radius:7px;border:1px solid #111";
  document.documentElement.appendChild(d);` : ""}
});`;
}

async function loadPage(page, opt, a, label) {
  const errors = [];
  page.on("Runtime.exceptionThrown", (e) => {
    const d = e.exceptionDetails;
    errors.push((d.exception && d.exception.description) || d.text);
  });
  page.on("Network.loadingFailed", (e) => {
    if (!e.canceled && e.type !== "Media") errors.push(`failed to load ${e.type}: ${e.errorText}`);
  });
  await page.send("Page.enable");
  await page.send("Runtime.enable");
  await page.send("Network.enable");
  await page.send("Emulation.setDeviceMetricsOverride", {
    width: a.w, height: a.h, deviceScaleFactor: a.scale, mobile: a.w <= 500,
  });
  if (a.dark) {
    await page.send("Emulation.setEmulatedMedia", { features: [{ name: "prefers-color-scheme", value: "dark" }] });
  }
  await page.send("Page.addScriptToEvaluateOnNewDocument", { source: labelScript(label, a) });
  return { errors, navigate: async () => {
    const loaded = new Promise((ok) => page.on("Page.loadEventFired", ok));
    await page.send("Page.navigate", { url: opt.url });
    await Promise.race([loaded, sleep(20000)]);
    await sleep(a.wait);
  } };
}

async function report(page, opt, errors) {
  const r = await page.send("Runtime.evaluate", {
    expression: "document.documentElement.scrollWidth - document.documentElement.clientWidth",
    returnByValue: true,
  });
  if (r.result.value > 0) console.log(`  ${opt.label}: sideways scroll of ${r.result.value} px`);
  for (const e of new Set(errors)) console.log(`  ${opt.label}: ${String(e).split("\n")[0]}`);
}

async function still(port, opt, a) {
  const page = await openPage(port);
  const { errors, navigate } = await loadPage(page, opt, a, "");
  await navigate();
  await page.send("Runtime.evaluate", { expression: "document.fonts.ready", awaitPromise: true });
  const params = { format: "jpeg", quality: 85 };
  if (a.full) {
    const { cssContentSize: s } = await page.send("Page.getLayoutMetrics");
    params.captureBeyondViewport = true;
    params.clip = { x: 0, y: 0, width: a.w, height: Math.ceil(s.height), scale: 1 };
  }
  const shot = await page.send("Page.captureScreenshot", params);
  const name = opt.label.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
  const file = join(a.out, `${name}.jpg`);
  writeFileSync(file, Buffer.from(shot.data, "base64"));
  console.log(file);
  await report(page, opt, errors);
  page.close();
}

async function record(port, opt, a, labelled, dir, index) {
  const page = await openPage(port);
  const { errors, navigate } = await loadPage(page, opt, a, labelled ? opt.label : "");
  const frames = [];
  page.on("Page.screencastFrame", (e) => {
    frames.push({ t: e.metadata.timestamp, data: e.data });
    page.send("Page.screencastFrameAck", { sessionId: e.sessionId }).catch(() => {});
  });
  await page.send("Page.startScreencast", {
    format: "jpeg", quality: 90, everyNthFrame: 1, maxWidth: a.w * a.scale, maxHeight: a.h * a.scale,
  });
  await navigate();
  const t0 = Date.now() / 1000;
  if (a.run) await page.send("Runtime.evaluate", { expression: a.run, userGesture: true });
  await sleep(a.seconds * 1000);
  await page.send("Page.stopScreencast");
  await report(page, opt, errors);
  page.close();

  const before = frames.filter((f) => f.t < t0).pop();
  const after = frames.filter((f) => f.t >= t0 && f.t < t0 + a.seconds);
  const timeline = (before ? [{ t: t0, data: before.data }] : []).concat(after);
  if (!timeline.length) die(`${opt.label}: Chrome sent no frames. Check the page loads.`);
  const folder = join(dir, `f${index}`);
  mkdirSync(folder);
  const lines = [];
  timeline.forEach((f, i) => {
    const file = join(folder, `${String(i).padStart(6, "0")}.jpg`);
    writeFileSync(file, Buffer.from(f.data, "base64"));
    const end = i + 1 < timeline.length ? timeline[i + 1].t : t0 + a.seconds;
    lines.push(`file '${file}'`, `duration ${Math.max(end - f.t, 0.001).toFixed(4)}`);
    if (i + 1 === timeline.length) lines.push(`file '${file}'`);
  });
  const list = join(dir, `f${index}.txt`);
  writeFileSync(list, lines.join("\n"));
  console.log(`  ${opt.label}: ${timeline.length} frames in ${a.seconds} s`);
  return list;
}

function findFfmpeg() {
  const known = [join(homedir(), ".local/bin/ffmpeg"), "/opt/homebrew/bin/ffmpeg", "/usr/local/bin/ffmpeg"];
  const onPath = spawnSync("ffmpeg", ["-version"], { stdio: "ignore" });
  if (!onPath.error) return "ffmpeg";
  const exe = known.find((p) => existsSync(p));
  if (!exe) die("ffmpeg not found. Run setup.sh next to this script.");
  return exe;
}

function ffmpeg(args) {
  const r = spawnSync(findFfmpeg(), ["-y", "-loglevel", "error", ...args], { stdio: "inherit" });
  if (r.error || r.status !== 0) die("ffmpeg failed");
}

const even = (n) => Math.max(2, Math.floor(n / 2) * 2);
const OUTPUT = ["-c:v", "libx264", "-crf", "21", "-preset", "veryfast", "-profile:v", "high", "-level", "4.2",
  "-color_range", "tv", "-movflags", "+faststart"];

function tileFilter(index, a, w, h) {
  const c = a.crop;
  return `[${index}:v]fps=${Math.round(30 / a.speed)},` +
    `crop=iw*${c.w / a.w}:ih*${c.h / a.h}:iw*${c.x / a.w}:ih*${c.y / a.h},` +
    `scale=${w}:${h}:in_range=full:out_range=tv,format=yuv420p`;
}

function input(list) {
  return ["-f", "concat", "-safe", "0", "-i", list];
}

function encodeOne(list, out, a) {
  const w = even(Math.min(a.crop.w * a.scale, 1920));
  const h = even((w * a.crop.h) / a.crop.w);
  const graph = `${tileFilter(0, a, w, h)},setpts=PTS/${a.speed},fps=30[v]`;
  ffmpeg([...input(list), "-filter_complex", graph, "-map", "[v]", "-t", String(a.seconds / a.speed), ...OUTPUT, out]);
}

function encodeStack(lists, out, a) {
  const GAP = 6;
  const aspect = a.crop.w / a.crop.h;
  let best = { w: 0 };
  for (let cols = 1; cols <= lists.length; cols++) {
    const rows = Math.ceil(lists.length / cols);
    const w = even(Math.min(1920 / cols - GAP, (1080 / rows - GAP) * aspect));
    if (w > best.w) best = { w, h: even(w / aspect), cols };
  }
  const { w, h, cols } = best;
  const tiles = lists.map((_, i) => `${tileFilter(i, a, w, h)},pad=${w + GAP}:${h + GAP}:${GAP / 2}:${GAP / 2}:color=0x111111[t${i}]`);
  const layout = lists.map((_, i) => `${(i % cols) * (w + GAP)}_${Math.floor(i / cols) * (h + GAP)}`).join("|");
  const grid = lists.length > 1
    ? `${lists.map((_, i) => `[t${i}]`).join("")}xstack=inputs=${lists.length}:layout=${layout}:fill=0x111111[g]`
    : "[t0]null[g]";
  const canvas = `[g]pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=0x111111,setpts=PTS/${a.speed},fps=30[v]`;
  ffmpeg([...lists.flatMap(input), "-filter_complex", [...tiles, grid, canvas].join(";"), "-map", "[v]",
    "-t", String(a.seconds / a.speed), ...OUTPUT, out]);
}

function optionPath(out, opt) {
  const id = opt.label.split(/\s+/)[0].toLowerCase().replace(/[^a-z0-9]+/g, "");
  return out.replace(/(\.[a-z0-9]+)?$/i, `-${id}$1`);
}

const args = parseArgs(process.argv.slice(2));
const dir = mkdtempSync(join(tmpdir(), "capture-"));
let chrome;
try {
  chrome = await startChrome(dir);
  if (args.mode === "still") {
    mkdirSync(args.out, { recursive: true });
    for (const opt of args.options) await still(chrome.port, opt, args);
  } else {
    mkdirSync(dirname(resolve(args.out)), { recursive: true });
    const lists = [];
    for (const [i, opt] of args.options.entries()) {
      lists.push(await record(chrome.port, opt, args, args.options.length > 1, dir, i));
    }
    if (args.stack || args.options.length === 1) {
      if (args.stack) encodeStack(lists, args.out, args); else encodeOne(lists[0], args.out, args);
      console.log(resolve(args.out));
    } else {
      lists.forEach((list, i) => {
        const out = optionPath(args.out, args.options[i]);
        encodeOne(list, out, args);
        console.log(resolve(out));
      });
    }
    const shape = args.crop.w / args.crop.h;
    if (!args.stack && Math.abs(shape - 16 / 9) > 0.1) {
      console.log(`  Note: this clip is ${args.crop.w}x${args.crop.h}. T3 embeds show 16:9, so use --crop or link the file.`);
    }
  }
} finally {
  if (chrome) chrome.proc.kill();
  await sleep(200);
  rmSync(dir, { recursive: true, force: true });
}
