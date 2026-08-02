#!/bin/bash
set -euo pipefail
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get install -y -qq git build-essential libcairo2-dev libpango1.0-dev libjpeg-dev libgif-dev librsvg2-dev python3 ca-certificates >/dev/null
git clone --depth 1 --branch v1.2.5 https://github.com/hiukim/mind-ar-js.git
cd mind-ar-js
npm install --omit=dev
npm install canvas @tensorflow/tfjs @tensorflow/tfjs-backend-cpu --no-save
cp /work/postcard.png ./postcard.png
cp /work/run-offline-compile.mjs ./run-offline-compile.mjs
node ./run-offline-compile.mjs
