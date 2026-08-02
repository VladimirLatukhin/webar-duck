#!/bin/bash
# Compile postcard.png -> targets.mind inside Docker (avoids Windows canvas build pains)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
docker run --rm -v "$ROOT:/work" -w /work node:20-bookworm bash -c '
  set -e
  apt-get update -qq
  apt-get install -y -qq build-essential libcairo2-dev libpango1.0-dev libjpeg-dev libgif-dev librsvg2-dev >/dev/null
  npm install --silent
  # Prefer official OfflineCompiler from mind-ar if exported
  node <<'"'"'NODE'"'"'
import { writeFile } from "fs/promises";
import { createRequire } from "module";
import { loadImage } from "canvas";

const require = createRequire(import.meta.url);
let OfflineCompiler;
try {
  const m = await import("mind-ar/dist/mindar-image.prod.js");
  OfflineCompiler = m.OfflineCompiler || m.default?.OfflineCompiler;
} catch {}
if (!OfflineCompiler) {
  try {
    const m = await import("mind-ar");
    OfflineCompiler = m.OfflineCompiler;
  } catch {}
}
if (!OfflineCompiler) {
  console.error("OfflineCompiler missing; listing mind-ar package...");
  const { readdirSync } = await import("fs");
  try { console.log(readdirSync("node_modules/mind-ar/dist").join("\n")); } catch(e) { console.error(e); }
  process.exit(2);
}
const image = await loadImage("assets/postcard.png");
const compiler = new OfflineCompiler();
await compiler.compileImageTargets([image], (p) => console.log("progress", Math.round(p*100)/100));
const buffer = compiler.exportData();
await writeFile("assets/targets.mind", Buffer.from(buffer));
console.log("OK targets.mind", buffer.byteLength || buffer.length);
NODE
'
