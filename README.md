# Vidéos FoundClub

Projets vidéo de FoundClub montés avec [HyperFrames](https://github.com/heygen-com/hyperframes) : la vidéo est une page HTML animée avec GSAP, filmée image par image dans Chrome, puis encodée par ffmpeg.

## Démarrer une session cloud

```bash
./installer-cloud.sh     # environ 3 min : outils, Whisper en local (modeles/, non versionné), compétences HyperFrames
```

Une **nouvelle vidéo à monter** se dépose dans `a-monter/` (moins de 100 Mo, la limite de GitHub par fichier), poussée depuis le PC d'Adel. La session crée ensuite son propre dossier de projet à côté de `ach10/`, en reprenant `ach10/outils/` (transcription, calage mot à mot, assemblage, rendu).

## `ach10/` — la vidéo d'ach10 (ambassadeur FoundClub)

Vidéo verticale de **57,5 s** (1080×1920, 30 images/s) : ach10 parle face caméra, et l'app arrive en motion design à partir de **vraies captures d'écran**, avec le design system FoundClub (Montserrat, bleu `#01B3F4`, bleu nuit `#001218`, vert `#27D6A3`). Les sous-titres sont incrustés et le son est réglé à **-14 LUFS**.

**Rendu final** (10/10/2026, mis à jour le même jour avec les trois « FoundClub » à l'anglaise, « V4 ok » d'Adel) : `ach10/rendus/ach10-final.mp4`, identique octet pour octet à `ach10-complet-v4.mp4`, fait à partir de **l'original** (`medias/video/ach10-original.mov`, 15 Mbit/s). Le montage est le même que `ach10-complet-v2.mp4`, la version validée par Adel, rendue depuis la version légère (4 Mbit/s).

**Nouvelle prise « FoundClub »** (10/10/2026) : à 18 s, ach10 prononçait « FoundClub » à la française. Il a refait la phrase « Cette application, c'est FoundClub » (`a-monter/ach10-foundclub.mov`, 3 prises). `outils/remplacer-foundclub.py` prend **seulement le son** de la prise 1 et le colle de 16,7 à 18,9 s, sur les lèvres de l'ancienne prise. La phrase est coupée en deux morceaux recalés chacun, à 20 ms près. Le son est ensuite égalisé, mis au même niveau et limité. Hors de ce passage, la voix d'origine est intacte, échantillon pour échantillon. `outils/preparer-video.sh` l'applique tout seul ; `PRISE=2` ou `PRISE=3` choisit une autre prise. Prise 1 validée par Adel (« prise 1 ok »). Les deux autres « FoundClub » reçoivent des **greffes** prises dans la même prise (« B essaye ») :
- vers 34 s, seule la voyelle « -ound » est remplacée, à vitesse presque normale ;
- vers 48 s, en fin de phrase, c'est le mot entier, à vitesse normale.

Whisper entendait « Foon Club » et « FUNCLUB » ; il entend maintenant « Found Club » et « FoundClub ».

Les versions : `ach10-complet-v3.mp4` n'a que la phrase de 18 s ; `ach10-complet-v4.mp4` a les trois « FoundClub ».

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

### Sound design (10/10/2026)

La version `ach10/rendus/ach10-complet-v5.mp4` reprend l'image de la v4 et ajoute **96 bruitages**, posés sur les animations et sur les changements de plan (les coupes d'ach10).

Les bruitages sont **synthétisés par `outils/sons.py`** : aucun fichier tiers, aucun droit à payer. Il y en a 14 familles :
- **mouvements** : whoosh, swish, souffle, montée ;
- **pops et notifications** : pop, bulle de message, choix du sondage ;
- **interface** : clic d'écran, appui du doigt, surligneur, coupe de plan ;
- **effets** : impact du logo, scintillement du reflet, secousse.

- **Où et quand** : `sons.json` liste chaque bruitage avec son instant, sa famille et un réglage fin (`db`, `note`). On le modifie à la main.
- **Le premier jet** de cette liste vient de l'inventaire des 152 animations de la timeline et des 8 coupes repérées dans la vidéo.
- **Les niveaux** : `outils/mesurer-sons.py` mesure chaque bruitage face à la voix. Ils sont réglés de 8 dB (impacts) à 18 dB (petits clics) sous la voix.
- **Le mélange** : `outils/rendre.sh` fabrique la piste, la mélange sous la voix (limiteur à -1 dBFS) puis règle le tout à -14 LUFS.

### Avant de publier : à revérifier

- **« Collaboration commerciale »** : elle n'est pas dans la vidéo, sur décision d'Adel (« pas pour l'instant »). Elle est **obligatoire** si ach10 reçoit une contrepartie (loi du 9 juin 2023, art. 5). C'est à trancher avant toute publication.
- **Note App Store « 5,0 »** (6 avis le 10/10/2026) et **« iPhone · Android · Web »** sur la carte de la scène 8.
- **Vrais clubs visibles** (Collonges Basket, AIS Université Club) dans la recherche et le recrutement : montrés tels quels, sur décision d'Adel (« B »).
- **Numéro de téléphone de la fiche club** : flouté, sur décision d'Adel (« flou ok »).

### Fabriquer la vidéo

Il faut Node 22, ffmpeg, Python 3 et Chrome Headless Shell (`npx hyperframes browser ensure`, ou une copie locale désignée par `HYPERFRAMES_BROWSER_PATH`, trouvée toute seule en session cloud).

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

## `matchs-amicaux/` — la vidéo « matchs amicaux »

Vidéo verticale de **52,7 s** (1080×1920, 30 images/s, son à -14 LUFS), validée par Adel le 10/10/2026 : `matchs-amicaux/rendus/matchs-amicaux-final.mp4`. Elle est rendue depuis l'original (`a-monter/matchs-amicaux.mp4`).

Le message : les pros jouent tous les 3 jours, les amateurs passent parfois un mois sans match, et FoundClub permet au coach de trouver un adversaire près de chez lui. Les 11 scènes :
1. le calendrier des pros ;
2. le même calendrier, vide, pour les amateurs ;
3. les tampons COUPE, TRÊVE, REPORTÉ ;
4. la licence à 350 € ;
5. « Pourquoi pas un match amical ? » ;
6. les deux galères du coach ;
7. le logo ;
8. l'enregistrement d'écran d'Adel dans le téléphone, recalé sur la voix ;
9. « C'est tout. » ;
10. l'acceptation, puis le planning et les compos ;
11. « Envoie-la à ton coach », puis le carton final.

Fabriquer : `cd matchs-amicaux ; outils/preparer-video.sh ; outils/rendre.sh matchs-amicaux-final 18`. `outils/assembler.py` découpe aussi les extraits de l'enregistrement d'écran à la bonne vitesse.

À revérifier avant de publier :
- la mention « Collaboration commerciale », si la personne qui parle est rémunérée ;
- le point rouge d'enregistrement de l'iPhone, visible en haut du téléphone de 29 à 36 s (laissé tel quel).

## `world-cup/` — la vidéo « World Cup »

Vidéo verticale de **84,2 s** (1080×1920, 30 images/s, son à -14 LUFS), validée par Adel le 10/10/2026 : `world-cup/rendus/world-cup-final.mp4`. Elle est rendue depuis l'original (`a-monter/world-cup.mp4`), dont la prise en double (24,43–28,07 s) est coupée sur le changement de plan.

Le message : dans un an, la première Coupe du monde du foot amateur, avec des qualifications pays par pays et des phases finales en France. Les inscriptions sont ouvertes sur FoundClub. Les 13 scènes :
1. J-365 et le titre ;
2. « avec ton club ou tes potes » ;
3. « un défi un peu fou », « ouvert à tous » et les niveaux ;
4. la carte du monde en points, sans aucun pays nommé ;
5. le tableau du tournoi (8, 4, 2, puis le vainqueur) ;
6. le zoom sur la France et le tampon INSCRIPTIONS OUVERTES ;
7. le téléphone : 3 écrans World Cup **dessinés** (compte à rebours de 365 jours, choix de l'équipe, équipe inscrite), puis les 5 vraies captures de la création d'équipe ;
8. « Pourquoi ? » ;
9. « le sport plus accessible » et « 365 jours, on a besoin de vous » ;
10. les 5 cartes des besoins ;
11. le prochain épisode ;
12. « Envoie-la » ;
13. le titre final, puis le carton.

Fabriquer : `cd world-cup ; outils/preparer-video.sh ; outils/rendre.sh world-cup-final 18`.

À revérifier avant de publier :
- **Les écrans World Cup sont des maquettes** : la vidéo dit « les inscriptions sont déjà ouvertes », il faut que ce soit vrai dans l'app le jour de la publication ;
- **« Coupe du monde » et « World Cup » sont des marques de la FIFA** : à faire vérifier par un juriste avant de diffuser ;
- l'écran réel des liens d'invitation n'a pas été fourni : le bouton « Inviter mes joueurs » de la maquette le remplace ;
- la mention « Collaboration commerciale », si la personne qui parle est rémunérée.
