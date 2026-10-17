#!/usr/bin/env bash
# Extrait la partie « téléphone » du final (l'appli FoundClub, de « Ton coach il a juste à aller sur l'application »
# jusqu'à « garder le rythme ») SANS la tête d'ach10 (le médaillon en haut à droite) — demande d'Adel du 17/10/2026.
# Image : une variante de index.html où la vidéo d'ach10 et l'anneau du médaillon sont cachés, rendue en entier puis coupée.
# Son : celui du rendu final (voix + bruitages, déjà réglé), coupé aux mêmes images, fondus de 50 et 150 ms.
# Bornes (temps du final, en images à 30 i/s) : 1128 = 37,60 s, début de « Ton coach » ;
# 1601 = 53,37 s, le titre « Continuer à jouer & garder le rythme » encore à l'écran, juste avant « Maintenant ».
set -euo pipefail
cd "$(dirname "$0")/.."
: "${HYPERFRAMES_BROWSER_PATH:=$(ls /opt/pw-browsers/chromium_headless_shell-*/chrome-linux/headless_shell 2>/dev/null | head -1 || true)}"
export HYPERFRAMES_BROWSER_PATH
python3 -I outils/assembler.py > /dev/null
sed 's|</style>|      #cadre-video, #medaillon-anneau { opacity: 0 !important; }  /* variante sans la tête d'"'"'ach10 (visibility ne suffit pas : le moteur réaffiche les vidéos actives) */\n    </style>|' index.html > index-sans-tete.html
npx hyperframes render -c index-sans-tete.html -f 30 --crf 18 -o rendus/sans-tete-brut.mp4 --quiet
rm index-sans-tete.html
DEBUT=$(python3 -c "print(1128 / 30)"); DUREE=$(python3 -c "print((1601 - 1128) / 30)")
ffmpeg -y -v error -ss "$DEBUT" -i rendus/sans-tete-brut.mp4 -ss "$DEBUT" -i rendus/matchs-amicaux-2-final.mp4 -t "$DUREE" \
  -map 0:v:0 -map 1:a:0 -af "afade=t=in:d=0.05,afade=t=out:st=$(python3 -c "print($DUREE - 0.15)"):d=0.15" \
  -c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p -c:a aac -b:a 192k -ar 48000 -movflags +faststart rendus/matchs-amicaux-2-telephone.mp4
ffmpeg -y -v error -i rendus/matchs-amicaux-2-telephone.mp4 -map 0:v:0 -c:v copy -an -movflags +faststart rendus/matchs-amicaux-2-telephone-muet.mp4
ffprobe -v error -show_entries stream=codec_type,duration,nb_frames -of compact rendus/matchs-amicaux-2-telephone.mp4
