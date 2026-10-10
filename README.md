# Vidéos FoundClub

Projets vidéo de FoundClub montés avec [HyperFrames](https://github.com/heygen-com/hyperframes) : la vidéo est une page HTML animée avec GSAP, filmée image par image dans Chrome, puis encodée par ffmpeg.

## `ach10/` — la vidéo d'ach10 (ambassadeur FoundClub)

Vidéo verticale de **57,5 s** (1080×1920, 30 images/s) : ach10 parle face caméra, et l'app arrive en motion design à partir de **vraies captures d'écran**, avec le design system FoundClub (Montserrat, bleu `#01B3F4`, bleu nuit `#001218`, vert `#27D6A3`). Les sous-titres sont incrustés et le son est réglé à **-14 LUFS**.

Rendu validé par Adel le 10/10/2026 : `ach10/rendus/ach10-complet-v2.mp4`, fait à partir de la **version légère** de sa vidéo. Le rendu final en pleine qualité attend l'original (voir plus bas).

### Les 9 scènes

| # | Temps | Ce qu'il dit | Ce qu'on voit | État |
|---|---|---|---|---|
| 1 | 0–5 s | « encore les groupes WhatsApp ? » | EN 2026, / ENCORE SUR / WHATSAPP ? dans un bandeau bleu | FAIT |
| 2 | 5–12 s | « convocations, entraînements, matchs… on s'y perd » | Faux groupe du club, les 3 mots en messages, 14 messages inventés, compteur jusqu'à 99+, « ON S'Y PERD. » | FAIT |
| 3 | 12–19 s | « changer l'organisation de ton club… c'est FoundClub » | ORGANISER / TON CLUB, puis icône FC et FOUNDCLUB avec un reflet | FAIT (« Mais aujourd'hui » retiré à la demande d'Adel) |
| 4 | 19–27 s | « le club, les joueurs, les dirigeants, les parents » | ach10 en médaillon, téléphone : accueil dirigeant, Gérer mon club, accueil joueur, accueil dirigeant, accueil parent, une étiquette par mot | FAIT |
| 5 | 27–34 s | « plutôt que les groupes WhatsApp… tout centraliser au même endroit » | Canal du club, 6 messages aspirés dans le téléphone, planning 3 jours, appel, AU MÊME ENDROIT | FAIT |
| 6 | 34–42 s | « pas seulement la gestion… la connexion entre les joueurs et les clubs » | Planche des compos des 5 sports, puis recherche de clubs, fiche club (numéro flouté), recrutement, affiche de détection (logo FC posé sur l'image cassée) | FAIT |
| 7 | 42–46 s | « joueur, éducateur, président, dirigeant, parent » | Écran « Quel est ton statut ? », cadre vert qui suit le mot, 5 étiquettes | FAIT |
| 8 | 46–49 s | « c'est le moment de venir découvrir FoundClub » | Carte App Store aux couleurs FoundClub posée sur sa bannière blanche (47,03–49,25 s) | FAIT |
| 9 | 49–57,5 s | « dis-moi en commentaire… Ciao mes petits potes ! » | DIS-LE EN COMMENTAIRE, sondage ENCORE WHATSAPP / UNE APPLICATION, carton final (badges App Store et Google Play, foundclub.app) | FAIT |

### Avant de publier : à revérifier

- **« Collaboration commerciale »** : elle n'est pas dans la vidéo, sur décision d'Adel (« pas pour l'instant »). Elle est **obligatoire** si ach10 reçoit une contrepartie (loi du 9 juin 2023, art. 5). C'est à trancher avant toute publication.
- **Note App Store « 5,0 »** (6 avis le 10/10/2026) et **« iPhone · Android · Web »** sur la carte de la scène 8.
- **Vrais clubs visibles** (Collonges Basket, AIS Université Club) dans la recherche et le recrutement : montrés tels quels, sur décision d'Adel (« B »).
- **Numéro de téléphone de la fiche club** : flouté, sur décision d'Adel (« flou ok »).

### Fabriquer la vidéo

Il faut Node 22, ffmpeg, Python 3 et Chrome Headless Shell (`npx hyperframes browser ensure`, ou une copie locale désignée par `HYPERFRAMES_BROWSER_PATH`).

```bash
npm install                        # à la racine du dépôt : hyperframes, gsap, Montserrat
cd ach10
outils/preparer-video.sh           # crée medias/video/ach10-source.mp4 (original s'il est là, sinon version légère)
outils/rendre.sh ach10-final       # assemble, contrôle, rend, règle le son → rendus/ach10-final.mp4
```

**`index.html` est fabriqué** par `outils/assembler.py` à partir de `gabarits/` (scènes en HTML, CSS, JS), de `calage.json` (l'instant où chaque mot-clé est prononcé) et des sous-titres écrits dans le script. On modifie les gabarits, jamais `index.html` à la main.

### Remplacer la version légère par l'original

1. Déposer la vidéo d'origine sous le nom `ach10/medias/video/ach10-original.mov` (moins de 100 Mo, la limite de GitHub par fichier).
2. Relancer `outils/preparer-video.sh`, puis `outils/rendre.sh ach10-final`. Le montage ne bouge pas : il est calé en secondes, et l'original a la même durée.

### Transcription et calage mot à mot

Whisper (modèle `turbo`, via [sherpa-onnx](https://github.com/k2-fsa/sherpa-onnx)), en local. Le modèle n'est pas versionné (1 Go) :

```bash
pip install sherpa-onnx soundfile numpy
curl -LO https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-whisper-turbo.tar.bz2 && tar xjf sherpa-onnx-whisper-turbo.tar.bz2
curl -LO https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/silero_vad.onnx
```

- `outils/transcrire.py` : transcription par morceaux, en sous-titres.
- `outils/caler_mots.py` : l'instant exact où un mot vient d'être dit (recherche par dichotomie), source de `calage.json`.
- `outils/reecouter.py` : réécoute d'un passage douteux.
- `transcription/ach10-transcription.srt` : le texte corrigé à la main (« Foon Club » → FoundClub, « s'arrive » → s'arrête).

### Sources des images

- **Captures de l'app** (`medias/captures/`) : envoyées par Adel les 9 et 10/10/2026, plus 10 captures du dépôt `foundclub-social-atelier`.
- **Badge App Store** : fichier officiel d'Apple (`developer.apple.com/assets/elements/badges/download-on-the-app-store.svg`).
- **Badge Google Play** : copie SVG du badge officiel ([steverichey/google-play-badge-svg](https://github.com/steverichey/google-play-badge-svg)). Le site de Google n'était pas joignable depuis la session cloud.
- **Messages et noms des scènes 2 et 5** : inventés. Aucun vrai nom, aucun emoji.
