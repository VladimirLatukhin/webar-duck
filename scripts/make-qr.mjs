#!/usr/bin/env node
/**
 * Generate assets/qr.png from WEBAR_URL (or argv).
 * Example: WEBAR_URL=https://you.github.io/webar-duck/ npm run qr
 */
import { writeFile } from "node:fs/promises";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import QRCode from "qrcode";

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, "..");
const url = process.env.WEBAR_URL || process.argv[2];

if (!url || !/^https:\/\//i.test(url)) {
  console.error("Usage: WEBAR_URL=https://USER.github.io/webar-duck/ npm run qr");
  process.exit(1);
}

const out = join(root, "assets", "qr.png");
const buf = await QRCode.toBuffer(url, {
  type: "png",
  width: 512,
  margin: 2,
  errorCorrectionLevel: "M",
});
await writeFile(out, buf);
console.log("wrote", out, "->", url);
