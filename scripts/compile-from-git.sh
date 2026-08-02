#!/bin/bash
set -euo pipefail
SRC=/tmp/webar-duck
WORK=/tmp/mind-ar-compile2
docker run --rm -v /tmp:/tmp alpine rm -rf "$WORK" >/dev/null 2>&1 || true
mkdir -p "$WORK"
cp "$SRC/assets/postcard.png" "$WORK/postcard.png"
cp "$SRC/scripts/run-offline-compile.mjs" "$WORK/run-offline-compile.mjs"
cp "$SRC/scripts/docker-compile-inner.sh" "$WORK/docker-compile-inner.sh"
chmod +x "$WORK/docker-compile-inner.sh"
docker run --rm -v "$WORK:/work" -w /work node:20-bookworm bash /work/docker-compile-inner.sh
cp -f "$WORK/targets.mind" "$SRC/assets/targets.mind"
ls -la "$SRC/assets/targets.mind"
