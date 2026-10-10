#!/usr/bin/env bash
# Prepare une session cloud Claude Code pour monter une video dans ce depot :
# outils npm (hyperframes, gsap, Montserrat), Whisper en local (sherpa-onnx + modele turbo),
# competences HyperFrames pour l'agent, et navigateur de rendu. Relancable sans risque.
set -euo pipefail
cd "$(dirname "$0")"
npm install --no-audit --no-fund
pip install -q sherpa-onnx soundfile numpy
mkdir -p modeles
BASE=https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models
[ -f modeles/sherpa-onnx-whisper-turbo/turbo-encoder.int8.onnx ] || curl -sSL "$BASE/sherpa-onnx-whisper-turbo.tar.bz2" | tar xj -C modeles
[ -f modeles/silero_vad.onnx ] || curl -sSL -o modeles/silero_vad.onnx "$BASE/silero_vad.onnx"
npx hyperframes skills update hyperframes talking-head-recut hyperframes-core hyperframes-animation >/dev/null
NAV=$(ls /opt/pw-browsers/chromium_headless_shell-*/chrome-linux/headless_shell 2>/dev/null | head -1 || true)
echo "ffmpeg     : $(ffmpeg -version | head -1 | cut -d' ' -f1-3)"
echo "whisper    : $(ls modeles/sherpa-onnx-whisper-turbo/*.onnx | wc -l) fichiers de modele"
echo "navigateur : ${NAV:-aucun en local -> npx hyperframes browser ensure}"
