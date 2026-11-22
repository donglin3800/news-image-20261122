// news-image-20261122: write one image summing up Sunday 22 November
// 2026's world news to /output/entry.png.
//
// The front page is drawn ahead of time by draw_news_image.py (Pillow)
// and shipped in this repository as entry.png. This program does nothing
// but place that file where the grader looks, so the graded run is
// deterministic, uses no network, and needs only the Node 22 standard
// library. Two runs therefore write byte-identical files.
//
// Local check:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
// then open out/entry.png. The copy is byte-for-byte: no re-encoding,
// no timestamps in the output, so repeated runs hash identically.

import { copyFileSync, mkdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const repoRoot = dirname(fileURLToPath(import.meta.url));
const shipped = join(repoRoot, "entry.png");

// The gate caps the image at 1 MiB; refuse to ship anything larger.
const MAX_BYTES = 1024 * 1024;
const size = statSync(shipped).size;
if (size > MAX_BYTES) {
  throw new Error(`entry.png is ${size} bytes, over the 1 MiB gate limit`);
}

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
const target = join(outDir, "entry.png");
copyFileSync(shipped, target);
// Confirm the copy landed intact before reporting success.
const copied = statSync(target).size;
if (copied !== size) {
  throw new Error(`copied entry.png is ${copied} bytes, expected ${size}`);
}
console.log(`wrote ${target} (${copied} bytes)`);
