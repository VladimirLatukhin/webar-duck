import { writeFile } from "fs/promises";
import { loadImage } from "canvas";
import { OfflineCompiler } from "./src/image-target/offline-compiler.js";

const image = await loadImage("./postcard.png");
const compiler = new OfflineCompiler();
await compiler.compileImageTargets([image], (p) => console.log("progress", p));
const buffer = compiler.exportData();
await writeFile("/work/targets.mind", Buffer.from(buffer));
console.log("OK", buffer.byteLength || buffer.length);
