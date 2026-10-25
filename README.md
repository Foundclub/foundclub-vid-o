# Vidéos FoundClub

Projets vidéo de FoundClub montés avec [HyperFrames](https://github.com/heygen-com/hyperframes) : la vidéo est une page HTML animée avec GSAP, filmée image par image dans Chrome, puis encodée par ffmpeg.

## Démarrer une session cloud

```bash
./installer-cloud.sh     # environ 3 min : outils, Whisper en local (modeles/, non versionné), compétences HyperFrames
```

Une **nouvelle vidéo à monter** se dépose dans `a-monter/` (moins de 100 Mo, la limite de GitHub par fichier), poussée depuis le PC d'Adel. La session crée ensuite son propre dossier de projet à côté de `ach10/`, en reprenant `ach10/outils/` (transcription, calage mot à mot, assemblage, rendu).

## `ach10/` — la vidéo d'ach10 (ambassadeur FoundClub)

Vidéo verticale de **57,5 s** (1080×1920, 30 images/s) : ach10 parle face caméra, et l'app arrive en motion design à partir de **vraies captures d'écran**, avec le design system FoundClub (Montserrat, bleu `#01B3F4`, bleu nuit `#001218`, vert `#27D6A3`). Les sous-titres sont incrustés et le son est réglé à **-14 LUFS**.

**Rendu final** (10/10/2026, mis à jour le même jour : trois « FoundClub » à l'anglaise, « V4 ok » d'Adel, puis sound design, « v5 ok ») : `ach10/rendus/ach10-final.mp4`, identique octet pour octet à `ach10-complet-v5.mp4`, fait à partir de **l'original** (`medias/video/ach10-original.mov`, 15 Mbit/s). Le montage est le même que `ach10-complet-v2.mp4`, la version validée par Adel, rendue depuis la version légère (4 Mbit/s).

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

## `ergysport/` — ach10 x Ergysport (collaboration commerciale)

Vidéo verticale d'ach10 pour la marque **Ergysport by Nutergia** (micronutrition sportive) : 31 s de parole, puis un carton final de 3 s. L'original (`a-monter/ach10-ergysport.mov`) est déjà monté par ach10 : la loupe d'ouverture, les coupes et le logo incrusté vers 10 s sont à lui. On ne fait qu'habiller par-dessus.

- **Direction artistique** : relevée sur les captures d'ergysport.com envoyées par Adel, le site n'étant pas joignable depuis la session cloud.
  - **Couleurs** : orange `#FF6B00`, dégradé `#FD7407` → `#FBB12B`, bleu marine `#0A3457`, blanc.
  - **Formes** : cartes blanches aux coins arrondis, dont un coin plus serré.
  - **Police** : Fira Sans Condensed, très grasse et en capitales. Elle est **proche** de celle du site, sans être forcément la même.
  - **Logo officiel** : fourni par Adel, dans `medias/marque/`.
- **Ce qu'on voit** : les titres en haut, les trois piliers (préparation, hydratation, récupération), une étiquette sous chaque produit qu'ach10 montre (whey, créatine, gélules récupération, multivitamines, barres, boosts), les sous-titres et le carton « Performez sainement ! » (la phrase du site).
- **La mention « Collaboration commerciale »** reste à l'écran **du début à la fin**. Elle est obligatoire (loi du 9 juin 2023 sur l'influence commerciale).
- **Sound design** : la bibliothèque synthétisée d'`ach10/` (`outils/sons.py`). `sons.json` liste 45 bruitages, réglés à la mesure (`outils/mesurer-sons.py sons.json medias/video/source.mp4`).

**Rendu final** (10/10/2026, « v1 ok » d'Adel) : `ergysport/rendus/ergysport-final.mp4`, 33,4 s, -14 LUFS, identique octet pour octet à `ergysport-v1.mp4`.

Fabriquer : `cd ergysport ; outils/preparer-video.sh ; outils/rendre.sh ergysport-final 18`.

À revérifier avant de publier :
- **Les allégations santé** : ach10 parle de « crampes et courbatures » et de « vitalité ». Ces mots restent dans les sous-titres seulement, et aucun titre ne les reprend. C'est à faire valider par la marque, car les allégations sur les compléments alimentaires sont encadrées.
- **Les noms de produits** dans les étiquettes (« Protein' », « Bar' », « Natural Boost ») sont lus sur les emballages et sur le site. La marque doit les valider.

## `youtube-clips/` — l'épisode YouTube d'ach10 découpé en clips verticaux

La source est l'épisode **#41 « Des débuts en N2 très compliqués ! »** (AchhLife saison 3, épisode 3, chaîne Achh10, 26:07). Codex l'a analysé et découpé en 18 extraits : voir `youtube-clips/RAPPORT.md` et `extraits.json`.

Les **4 clips habillés**, validés par Adel le 12/10/2026, sont dans `youtube-clips/habillage/rendus/clip-NN-tiktok.mp4` (1080×1920, -14 LUFS) :

| Clip | Accroche | Durée |
|---|---|---|
| 18 | Le discours du coach / Est-ce que vous y croyez ? | 36,8 s |
| 07 | Tu te coupes un doigt / pour 200 000 € ? (partie 1) | 34,0 s |
| 05 | Mener 2-0… / et perdre 3-2 | 37,0 s |
| 10 | Ousmane Dembélé nous a tués / à tous mes frères attaquants | 33,2 s |

- **Le gabarit**, dans `youtube-clips/habillage/` :
  - en haut, l'accroche ;
  - au milieu, la vidéo en carré. Le cadre suit la personne qui parle et s'arrête au-dessus des sous-titres incrustés de la version YouTube ;
  - une barre de progression ;
  - des sous-titres qui passent en jaune mot à mot ;
  - un carton final : « Allez voir l'épisode complet sur YouTube », avec la vignette de l'épisode.
- **Les données de chaque clip** sont dans `clips/NN.json` : cadrage, accroche, phrases.
- **Fabriquer un clip** : `cd youtube-clips/habillage ; outils/rendre-clip.sh 18`.

## `matchs-amicaux-2/` — la vidéo « matchs amicaux » d'ach10

Vidéo verticale de **62,1 s** (1080×1920, 30 images/s, son à -14 LUFS), validée par Adel le 17/10/2026 (« ok », sur la v3) : `matchs-amicaux-2/rendus/matchs-amicaux-2-final.mp4`, identique octet pour octet à `apercu-v3.mp4`. Son à -14,2 LUFS, crête à -2,8 dBFS.

Deuxième vidéo sur les matchs amicaux, tournée par ach10 (`a-monter/matchs-amicaux-ach-1.mov`, 55,3 s). Elle reprend la charte et les scènes de `matchs-amicaux/` (calendrier, licence, téléphone, carton final). Ce qui change :
- **La presse** :
  - Pour les pros (0–3 s), ach10 reste plein cadre. La une de L'Équipe « L'UNFP en appelle à l'État pour stopper la multiplication des matches » tombe au-dessus de sa tête. C'est la capture envoyée par Adel le 17/10/2026 (`medias/presse/lequipe-unfp-capture-complete.png`), rognée au titre (`lequipe-unfp.png`). Elle remplace les cartes Soccerway et DH de la v2.
  - Pour les amateurs (11–13 s) : une carte au titre recopié mot pour mot, avec le nom du média en texte, sans logo, et le surligneur jaune : [ICI Limousin](https://www.ici.fr/emissions/les-echos-du-limousin/en-correze-le-casse-tete-des-matchs-de-foot-a-reprogrammer-en-raison-des-intemperies-de-ces-dernieres-semaines-9543588) (Corrèze, matchs à reprogrammer).
- **L'extrait de la vidéo de référence** : « Embrouille Entraîneur et Joueur — Dimanche prochain je vais jouer », envoyée par Adel le 17/10/2026 (`a-monter/reference-dimanche-prochain-je-vais-jouer.mp4`, non versionnée).
  - Le passage va de 30,50 à 34,23 s : « Et dimanche prochain, je vais jouer ! Je vais jouer, la tête de ma mère, que je vais jouer ! ».
  - `outils/preparer-extrait.sh` le pose en pleine largeur sur un fond flouté et baisse son son de 4 dB. Le résultat est `medias/reference/extrait.mp4`, versionné.
  - La vidéo d'ach10 est coupée à 19,400 s, entre son « je vais jouer ! » (gardé en entier) et « Mais c'est quoi la raison ». L'extrait s'y glisse et `outils/assembler.py` décale toute la suite de sa durée.
  - Sans `extrait.mp4`, un emplacement réservé de 2,5 s le remplace.
- **Les excuses des coachs** (« contre qui jouer ? », « s'organiser », « domicile ou extérieur ? ») sont rayées par un tampon vert « Plus d'excuses ».
- **Les bruitages** : la bibliothèque d'`ach10/` (`outils/sons.py`). `outils/assembler.py` écrit `sons.json` aux mêmes instants que les animations.

**La partie téléphone seule, sans la tête d'ach10** (demande d'Adel du 17/10/2026) : `rendus/matchs-amicaux-2-telephone.mp4` (avec la voix et les bruitages) et `rendus/matchs-amicaux-2-telephone-muet.mp4`. Ils durent 15,8 s, de « Ton coach il a juste à aller sur l'application » à « garder le rythme ». C'est la même image que le final, sans le médaillon en haut à droite. Les fabriquer : `outils/extraire-telephone.sh`, après le final.

Fabriquer : `cd matchs-amicaux-2 ; outils/preparer-video.sh ; outils/rendre.sh matchs-amicaux-2-final 18` (`outils/preparer-extrait.sh` seulement si l'extrait doit être refait : il lit la vidéo de référence complète, non versionnée). `calage.json` est dans le temps de la vidéo d'origine : c'est l'assembleur qui décale ce qui vient après l'extrait.

À revérifier avant de publier :
- **Les droits de l'extrait de référence** : c'est le contenu d'un tiers, dans une vidéo de marque.
- **« Licence jusqu'à 550 € »** : c'est ach10 qui le dit. La première vidéo disait 350 €.
- la mention « Collaboration commerciale », si ach10 est rémunéré pour cette vidéo.

## `matchs-amicaux-3/` — « Pas de match ce week-end ? » (l'extrait, le joueur au maillot FoundClub, l'appli)

Vidéo verticale de **16,8 s** (1080×1920, 30 images/s, son à -14,1 LUFS), validée par Adel le 19/10/2026 (« ok go rendu », sur la v1) : `matchs-amicaux-3/rendus/matchs-amicaux-3-final.mp4`, identique octet pour octet à `apercu-v1.mp4`.

Elle est faite à partir de la vidéo d'Adel `a-monter/matchs-amicaux-ref.mp4` (11,5 s, 2160×3840 à 60 i/s). On y voit l'extrait « Dimanche prochain je vais jouer », puis un joueur en maillot FoundClub qui parle aux coachs. Le montage d'origine portait la légende « Pas de match ce weekend ? On a la solution ! ». Les 5 temps :
1. **L'extrait** (0–3,7 s) : celui de `matchs-amicaux-2/medias/reference/extrait.mp4`, avec ses sous-titres. L'accroche « Pas de match ce week-end ? » est dans une bulle blanche en haut.
2. **Le volet bleu « On a la solution ! »** (3,4–4,3 s), avec l'icône FC. Il couvre le passage au joueur et le fondu au noir de la vidéo d'Adel : on lit le joueur à partir de 4,25 s.
3. **Le joueur** : « Tu cherches des matchs amicaux ? », puis le logo FoundClub sur « FoundClub, c'est fait pour toi ».
4. **L'appli, sans personne à l'écran** (à partir de « Télécharge l'app ») : l'enregistrement d'écran de `matchs-amicaux/` dans le téléphone.
   - « trouver des matchs amicaux » : appui sur la carte « Matchs amicaux ».
   - « publier ta propre annonce » : appui sur « + Créer un match amical ».
   - Puis, sans voix : « Proposer un match », le formulaire, et « Félicitations, proposition envoyée ! ».
5. **Le carton final** FoundClub.

Fabriquer : `cd matchs-amicaux-3 ; outils/preparer-video.sh ; outils/rendre.sh matchs-amicaux-3-final 18`.

À revérifier avant de publier : l'accord du joueur filmé (il n'est nommé nulle part), et les droits de l'extrait de référence (contenu d'un tiers, filigrane LEHUMOUR.FR). `calage.json` est dans le temps de la vidéo d'Adel ; l'assembleur le décale (le joueur commence à 3,733 s dans le montage).

## `matchs-amicaux-4/` — la Toussaint et la nouvelle fonctionnalité (deux joueurs en maillot FoundClub)

Vidéo verticale de **24,5 s** (1080×1920, 30 images/s, son à -14,1 LUFS), validée par Adel le 19/10/2026 (« ok go rendu », sur la v1) : `matchs-amicaux-4/rendus/matchs-amicaux-4-final.mp4`, identique octet pour octet à `apercu-v1.mp4`. Elle part de `a-monter/matchs-amicaux-4.mp4`. C'est la vidéo d'Adel, déjà montée : un gros plan d'ouverture et des coupes entre deux joueurs. Elle a été réduite en 1080×1920 à 30 i/s sur son PC pour passer sous les 100 Mo.

Les 6 temps, calés sur la voix :
1. « 2026 » en grand, puis « Des coachs qui galèrent pendant des heures » en rouge.
2. La pastille orange « Vacances de la Toussaint ». Elle ne porte pas de dates : la vidéo dit « arrivent ».
3. La pastille « Nouvelle fonctionnalité » et le logo FoundClub.
4. Sur « Maintenant… », les joueurs s'effacent et l'appli prend tout l'écran : appui sur « Matchs amicaux » (« trouver des matchs amicaux »), puis sur « + Créer un match amical » (« publier ta propre annonce »), puis la liste et « Proposer un match ».
5. Retour aux joueurs : « Coach, trouve ton prochain match ».
6. « Envoie-la à ton coach », puis le carton final.

Fabriquer : `cd matchs-amicaux-4 ; outils/preparer-video.sh ; outils/rendre.sh matchs-amicaux-4-final 18`.

À revérifier avant de publier : l'accord des deux joueurs filmés, et que la fonctionnalité matchs amicaux est bien ouverte dans l'app le jour de la publication (« on vient d'ouvrir une nouvelle fonctionnalité »).

## `miniatures/bourbier-r3/` — la miniature YouTube « Match bourbier » d'ach10

Miniature de l'épisode « Match bourbier contre cette R3 » (Coupe de France, 3ᵉ tour, chaîne Achh10), validée par Adel le 23/10/2026 (« garde celle de base ») : `miniatures/bourbier-r3/rendus/miniature-bourbier-r3.jpg`, 1280×720, 225 Ko (YouTube accepte jusqu'à 2 Mo). Elle remplace une version faite par ChatGPT, qui faisait « IA » (faux joueurs, faux maillot rouge, logo redessiné). Ici, rien n'est généré par IA : tout vient de l'épisode.

- Fond : la vue de drone à 15:12 (912 s) de l'épisode, recadrée pour enlever le tableau d'affichage. On y voit le terrain pelé.
- Achraf : la photo en maillot Coupe de France envoyée par Adel le 23/10/2026 (`a-monter/bourbier/achraf-maillot-cdf.jpg`), détourée avec `npx hyperframes remove-background`. La première version prenait son visage dans l'épisode à 7:08 (`medias/achraf-ep-net.png`, gardé).
- Le blason Coupe de France officiel (envoyé par Adel), l'étiquette « CHAMP DE PATATE » et sa flèche, le titre « MATCH BOURBIER » en Anton (licence OFL).
- Le coin en bas à droite reste libre pour la durée affichée par YouTube. La miniature passe le test de lecture à 120 px de large.

L'épisode est dans `a-monter/bourbier/partie-*.mp4` : 12 morceaux de 2 minutes, pour passer sous la limite de 100 Mo de GitHub. Pour le recoller :
`for f in a-monter/bourbier/partie-*.mp4; do echo "file '$PWD/$f'"; done > liste.txt ; ffmpeg -f concat -safe 0 -i liste.txt -c copy episode.mp4`.

Fabriquer : `cd miniatures/bourbier-r3 ; node outils/rendre.mjs index.html rendus/miniature.png ; ffmpeg -i rendus/miniature.png -q:v 2 rendus/miniature-bourbier-r3.jpg`.

## `clips-bourbier/` — l'épisode « Match bourbier » découpé en clips

Même méthode que `youtube-clips/` (épisode #41) : transcription locale, planches, sélection, découpe. L'épisode (22:39) vient de `a-monter/bourbier/` ; Montpellier Atlas Paillade, l'équipe d'Achraf, y bat Saint-Orens (R3) 3-0 au 3ᵉ tour de la Coupe de France.

**21 extraits** (16 à 56 s), chacun en `horizontal/clip-NN.mp4` (1920×1080) et en brouillon `vertical/clip-NN-9x16.mp4` (1080×1920, fond flou), son à -14 LUFS. Classement, notes et risques dans `clips-bourbier/RAPPORT.md` ; bornes et textes dans `extraits.json`. Les meilleurs : 10 « Un champ de patate ! » (le président), 04 « 10 000 personnes à la Mosson », 08 la causerie de la mi-temps sur l'état du terrain, 07 la causerie d'avant-match, 09 les 3 buts, 15 le terrain pelé vu du drone. Les 10 derniers (12 à 21) ajoutent les moments sans parole : chaque but seul, l'entrée des joueurs, le coup de sifflet final, l'entraînement, la bande-annonce du prochain épisode.

Les extraits 01 à 05 et 12 (l'histoire d'Achraf en Coupe de France) sont faits d'images télé (Eurosport, France 3) : la voix est la sienne, les images non.

Refaire les extraits : `cd clips-bourbier ; outils/recoller.sh ; python3 -I outils/exporter.py [numéros]`.

**Les 21 clips habillés** (23/10/2026, Adel : « on va tous les habiller car on va en publier au moins 2 par jour ») : `clips-bourbier/habillage/rendus/clip-NN-tiktok.mp4`, 1080×1920, 14 à 59 s, son entre -14,5 et -14,0 LUFS, crêtes sous -1,5 dBFS. Ordre de publication sur 11 jours : `clips-bourbier/CALENDRIER.md`.
- Gabarit repris de `youtube-clips/habillage/`, restylé le 24/10/2026 à la demande d'Adel avec les codes de la miniature : titres en Anton blanc et jaune à contour noir, pastille rouge, fond bleu nuit, vidéo encadrée de blanc, barre de progression rouge, le mot dit dans une pastille jaune ; carton final avec la nouvelle miniature et le titre « #42 Match piège pour notre entrée en Coupe de France ! ».
- Retours d'Adel du 24/10 : nouveaux titres sur 16 clips, coupes du 07 (24 s), 08 (à partir de 38 s), 14 (50 s), 15 (de 8 à 28 s) et 18 (11 s), décrites dans `habillage/outils/fiches.py` (`GARDER`).
- Deux formats (`format` dans `habillage/clips/NN.json`) : `carre` suit la personne qui parle (07, 08, 10, 20, repères posés à la main) ; `large` montre l'image entière en 16:9 sur fond flou (match, drone, montages).
- Les fiches sont écrites par `habillage/outils/fiches.py` (accroches, phrases corrigées à la main, cadrage). Dans les causeries du coach, seules les phrases reconnues avec certitude sont sous-titrées.
- Fabriquer : `cd clips-bourbier/habillage ; python3 -I outils/fiches.py ; outils/rendre-tout.sh [NN …]`.
- La bulle « suivre » (25/10/2026, Adel : « 1- ok 2- A ») : la photo de profil d'Achh10 (`habillage/medias/profil-achh10.jpg`) et le bouton + qui devient une coche, façon TikTok, 2 s à partir de 3 s, en haut à droite de la vidéo. Réglable par clip avec `"follow"` dans `clips/NN.json` (une autre seconde, ou -1 pour l'enlever).
- Son : un limiteur suréchantillonné à -3 dB et un fondu de 50 ms au début (la première trame claquait à +1,7 dBFS).
