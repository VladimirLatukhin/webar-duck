#!/usr/bin/env node
/**
 * Compile postcard.png -> assets/targets.mind using MindAR OfflineCompiler.
 * Run: npm install && npm run compile
 */
import { writeFile } from "node:fs/promises";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { createRequire } from "node:module";
import { loadImage } from "canvas";

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, "..");
const require = createRequire(import.meta.url);

async function loadOfflineCompiler() {
  // mind-ar package layouts differ by version; try common paths
  const candidates = [
    "mind-ar/dist/mindar-image.prod.js",
    "mind-ar/dist/mindar-image-offline.prod.js",
  ];
  for (const c of candidates) {
    try {
      const mod = await import(c);
      if (mod.OfflineCompiler) return mod.OfflineCompiler;
      if (mod.default?.OfflineCompiler) return mod.default.OfflineCompiler;
    } catch {
      /* try next */
    }
  }
  // Fallback: clone-style path if installed from git examples
  try {
    const mod = await import("mind-ar/src/image-target/offline-compiler.js");
    return mod.OfflineCompiler;
  } catch {
    /* ignore */
  }
  throw new Error(
    "OfflineCompiler not found in mind-ar. Use the web compiler: https://hiukim.github.io/mind-ar-js-doc/tools/compile/"
  );
}

const OfflineCompiler = await loadOfflineCompiler();
const imagePath = join(root, "assets", "postcard.png");
const outPath = join(root, "assets", "targets.mind");

const image = await loadImage(imagePath);
const compiler = new OfflineCompiler();
await compiler.compileImageTargets([image], (p) => console.log("progress", p));
const buffer = compiler.exportData();
await writeFile(outPath, Buffer.from(buffer));
console.log("wrote", outPath, buffer.byteLength || buffer.length);
