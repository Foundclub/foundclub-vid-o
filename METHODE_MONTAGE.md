# Méthode de montage — ce qu'une session doit savoir avant de toucher une vidéo

Écrit le 27/10/2026 par la session cloud qui a monté ach10, Matchs amicaux 1 à 4, World Cup, Ergysport, les clips
de l'épisode #41 et de l'épisode #42 « Match bourbier », et la miniature #42. Tout ce qui est écrit ici a été payé une fois.
**Un état (chiffre, fichier, version) se vérifie par commande avant d'être cru** : ce document ne sait pas ce qui a changé depuis.

---

## 1. Travailler avec Adel

- Adel **pilote, il ne relit pas le code**. Il valide des écrans et des vidéos, pas des fichiers. On lui parle en français
  simple et imagé, en **écrans** (« à 0:42, le titre arrive »), jamais en chemins de fichiers.
- Chaque message de fond se termine par un bloc **« ⚖️ CE QUE TU DOIS DÉCIDER »** numéroté, avec une recommandation,
  les options, et le format de réponse attendu (`1- A 2- ok`). S'il n'y a rien à décider, on l'écrit.
- On ne lui pose que les vraies questions (contenu, goût, droits, argent). Le technique réversible et vérifiable, on le
  tranche, on le fait, on le rapporte.
- **On finit sur une preuve**, jamais sur « c'est fait » : décodage complet, mesure du son, image vérifiée. Ce qui n'a
  pas pu être vérifié s'écrit en tête : `NON VÉRIFIÉ : <quoi> — commande qui le prouverait : <cmd>`.
- Il répond souvent à la voix (dictée) : « Ashraf », « Achh10 », « ach » = **Achraf Berriss**, chaîne YouTube **Achh10**,
  série **AchhLife** (saison 3). Son club : **Montpellier Atlas Paillade** (N2, maillot noir DGL Groupe).
- Il veut voir avant de valider : envoyer **un aperçu court** (planche d'images, extrait de 10 s) avant un long rendu.

## 2. Le savoir-faire, outil par outil

| Besoin | Outil dans le dépôt | Remarque |
|---|---|---|
| Transcrire (mots horodatés) | `youtube-clips/outils/transcrire.py` (faster-whisper, utilisé par Codex sur le PC) · `ach10/outils/transcrire.py` (sherpa-onnx, CPU) | Sur le PC : faster-whisper **large-v3-turbo sur la RTX 3070 Ti** (`device="cuda", compute_type="float16"`), français, `word_timestamps=True`, `vad_filter=True`, `initial_prompt` avec les noms propres |
| Instant exact d'un mot | `ach10/outils/caler_mots.py` | Cherche depuis le début de la fenêtre : un mot répété demande sa propre fenêtre |
| Réécouter un passage | `ach10/outils/reecouter.py` | Pour corriger un mot douteux avant de l'écrire en sous-titre |
| Découper des extraits | `clips-bourbier/outils/exporter.py` | Fondu de 30 ms aux bouts, loudnorm en deux passes |
| Vertical 9:16 habillé | `clips-bourbier/habillage/` (gabarit, `outils/fiches.py`, `outils/rendre-tout.sh`) | Carré qui suit la personne (repères à la main) ou image entière sur fond flou |
| Miniature YouTube | `miniatures/bourbier-r3/` (HTML + `outils/rendre.mjs`) | Vraies photos détourées, aucune image générée par IA |
| Détourer une personne | `npx hyperframes remove-background image.png -o sortie.png` | Modèle local, 2 s par image |
| Bruitages | `ach10/outils/sons.py` (bibliothèque synthétisée : swish, pop, tap, whoosh, impact, choix…) | Niveaux réglés sur la voix d'ach10 (-11,7 LUFS) : corriger `GAIN_SONS` si la voix est plus faible |
| Vidéo animée (titres, motion) | HyperFrames (HTML + GSAP), compétences `hyperframes*` | Voir les pièges §4 |

## 3. Le style validé par Adel

- **Titres** en **Anton**, blanc et jaune `#ffd400`, contour noir épais (`-webkit-text-stroke` + `paint-order: stroke fill`),
  légère rotation sur la 2ᵉ ligne. **Pastille rouge** `#e30613`, fond bleu nuit, vidéo encadrée de blanc.
- **Sous-titres** : le mot en train d'être dit dans une pastille jaune. **Typographie française** : espace insécable avant
  `! ? : »` et après `«` (fonction `insecable()` dans les assembleurs).
- **Vidéos FoundClub, depuis le 28/10 (Adel)** : pas d'intro en motion ; des **stickers façon story** (fond blanc, texte noir,
  penchés, sans icône ni halo) plutôt que des pastilles lumineuses à icône ; **peu de sons, des bruits réels** (sticker, tampon,
  bande qui s'arrête, vibration, clic : `week-end-gache/outils/sons.py`), rien sur les titres ; **jamais d'étiquette posée sur
  l'écran de l'appli** (c'est ce qu'on montre). Les mêmes pops et whooshs partout font « IA ».
- **Bulle « suivre »** façon TikTok (photo de profil `clips-bourbier/habillage/medias/profil-achh10.jpg`, bouton + qui devient
  une coche), 2 s, à 3 s du début.
- **Rien qui fasse « IA »** : pas de faux joueurs, de faux maillots ni de logos redessinés. Le blason officiel de la Coupe de
  France est dans `miniatures/bourbier-r3/medias/cdf-blason.png`.
- **Anti-spoil** (règle d'Adel du 26/10) : rien ne dévoile le résultat d'un match avant la fin du calendrier ; tableau
  d'affichage flouté, « BUT ! » sans score, ce qui en dit un peu passe en dernier.
- **Le style des épisodes d'Achraf** se lit dans l'épisode #42 lui-même (`a-monter/bourbier/partie-*.mp4`, à recoller avec
  `clips-bourbier/outils/recoller.sh`) : ouverture en montage de mots, carte « SAISON 3 ÉPISODE N » façon glitch, résumé
  « Dans l'épisode précédent… », sous-titres blancs simples en bas, bandeaux de nom (« BEN ALI Mahfoud · Président Montpellier
  Atlas Paillade »), « Jour de match… », drone, demande d'abonnement vers 12 min, carton de fin AchhLife avec les réseaux.
  **Un nouvel épisode imite ce style**, il ne l'invente pas.

## 4. Les pièges déjà payés

- **Son qui sature après l'encodage AAC** : loudnorm en mode linéaire laisse passer des crêtes, et l'AAC les fait remonter.
  Chaîne qui marche : mesure en deux passes, puis
  `afade=t=in:st=0:d=0.05,aresample=192000,alimiter=limit=0.708:attack=2:release=60:level=0:latency=1,aresample=48000`.
  Toujours mesurer **après** l'encodage : `ffmpeg -i x.mp4 -af ebur128=peak=true -f null -` (cible -14 LUFS, crête sous -1 dBFS).
  La première trame peut claquer : le fondu de 50 ms au début est là pour ça.
- **HyperFrames** : une `<video>` dans un élément minuté est une erreur de lint (la vidéo doit être enfant direct du stage) ;
  `visibility:hidden` est écrasé par le moteur (cacher avec `opacity: 0 !important`) ; une transformation CSS sur un élément
  animé par GSAP en `xPercent` entre en conflit ; navigateur : `HYPERFRAMES_BROWSER_PATH` vers un Chrome headless.
- **Une vidéo HyperFrames longue** se rend **par séquences** (un fichier par scène), puis se recolle avec ffmpeg : un rendu
  de 25 min d'un seul tenant ne se reprend pas s'il casse.
- **`pgrep -f motif` se voit lui-même** (et `pkill -f` peut tuer sa propre commande) : attendre sur le contenu d'un fichier
  de sortie, ou exclure son propre PID.
- **Les sous-titres se chevauchaient** au changement de phrase : éteindre la phrase avant que la suivante arrive.
- **Whisper se trompe sur les noms propres** (Louhans-Cuiseaux → « loup en cuiseau », Atlas Paillade → « Atlas Payane »,
  Mosson → « motion », Saint-Orens → « Saint-Horinz »). Les mettre dans `initial_prompt`, et ne **jamais** sous-titrer un nom
  non vérifié sans le signaler à Adel. Dans un vestiaire (écho, musique), ne sous-titrer que ce qui est reconnu avec certitude.
- **Un tableau d'affichage incrusté** déborde dans les recadrages (« MAP » dans le coin) : décaler le cadre ou flouter.
- **Le recadrage carré peut couper un bandeau de nom** : prendre un carré plus petit en haut de l'image (`"cote"`).

## 5. Fichiers et git

- **Les rushs et les rendus lourds ne vont jamais dans git** (limite GitHub : 100 Mo par fichier). Ils restent sur le disque
  (`D:\App\video\rushs\<épisode>\` pour les rushs) ; le dépôt ne garde que les outils, le papier de montage, les fiches, et les
  rendus de moins de 100 Mo. Ajouter les dossiers lourds au `.gitignore` **avant** le premier `git add`.
- Commit **par chemins explicites** (`git commit -m "…" -- chemin1 chemin2`), message en français, et on ne pousse que ce
  qu'Adel a validé ou ce qui est vérifié.

## 6. Monter un épisode long (interview + plans de coupe) : la marche à suivre

1. **Inventaire** (`<épisode>/inventaire.json`) : pour chaque rush, durée, caméra (nom de fichier DJI = date et heure de
   tournage), résolution, images/s, son présent ou non. Une **copie légère** 720p par rush pour travailler vite
   (`-c:v h264_nvenc` sur la RTX), une **planche** d'images toutes les 5 s, la **transcription** des rushs qui parlent.
   Si un micro séparé ou deux caméras filment la même scène : synchroniser par corrélation croisée du son (48 kHz,
   à l'échantillon près), pas à l'œil.
2. **Papier de montage** (`<épisode>/papier.md`) : l'histoire de l'épisode en phrases de l'interview, dans l'ordre, avec les
   plans de coupe sous chaque phrase et la durée visée. **Adel valide le papier avant tout montage.**
3. **Premier montage** depuis les copies légères, rendu par séquences, envoyé à Adel avec une planche par séquence.
4. **Finition** : habillage dans le style d'Achraf (§3), sous-titres corrigés, musique, son à -14 LUFS, rendu final depuis
   les rushs d'origine. Vérifier : décodage complet (`ffmpeg -v error -i x -f null -`), son (`ebur128`), planche d'images.
5. Ensuite seulement : la miniature (`miniatures/`) et les clips verticaux (`clips-bourbier/` comme modèle).

## 7. Le suivi des 20 scripts (bibliothèque de tournage)

`scripts-foundclub/bibliotheque-20-scripts.pdf` est le PDF d'origine (jamais modifié). Le suivi est dans
`scripts-foundclub/suivi.json` : une ligne par vidéo (`"03": {"etat": "fait", "date": …, "detail": …, "fichier": …}`) ;
`etat` vaut `fait` (monté et validé par Adel) ou `en cours` (tourné ou en montage) ; une vidéo absente est « à tourner ».
**Toute session qui monte une de ces vidéos coche sa ligne** : `en cours` au début, `fait` quand Adel a validé le rendu,
puis `python3 -I scripts-foundclub/outils/suivi.py` (sous Windows : `python scripts-foundclub\outils\suivi.py`) refait
`bibliotheque-20-scripts-suivi.pdf` (page de suivi en tête, pastille devant chaque ligne de la liste, bandeau d'état sur la
page du script), et on commite les trois fichiers ensemble. Il faut `pip install pypdf reportlab`.

**Le calendrier des publications** (clips AchhLife et vidéos FoundClub, un seul document) : `publications/CALENDRIER.pdf`,
écrit par `publications/calendrier.py` (les cases FoundClub sont dans `FOUNDCLUB` : une date → un numéro de script, `None`
pour une case qui attend la prochaine vidéo tournée ; titres et états lus dans `scripts-foundclub/suivi.json`). Quand une
vidéo est validée, la session la place dans la prochaine case vide, puis
`python3 -I publications/calendrier.py && node publications/pdf.mjs publications/CALENDRIER.html publications/CALENDRIER.pdf`.
