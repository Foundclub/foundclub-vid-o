#!/usr/bin/env bash
# Rend tous les clips (ou ceux donnés) l'un après l'autre ; un journal par clip dans rendus/journal-NN.txt.
# Usage : outils/rendre-tout.sh [NN ...]
cd "$(dirname "$0")/.."
LISTE=${*:-$(ls clips | sed 's/.json//')}
for NN in $LISTE; do
  if outils/rendre-clip.sh "$NN" > "rendus/journal-$NN.txt" 2>&1; then echo "$NN ok $(tail -1 rendus/journal-$NN.txt)"; else echo "$NN ECHEC (voir rendus/journal-$NN.txt)"; fi
done
echo fini
