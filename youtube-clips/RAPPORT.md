NON VÉRIFIÉ : correspondance automatique exacte des mots aux limites pour les clips 07, 12 — commande de relecture : `ffplay -autoexit youtube-clips/horizontal/clip-NN.mp4` ; remplacer NN par le numéro concerné, écouter le début et la fin. Les fichiers sont décodables intégralement ; les écarts ASR restent signalés.

NON VÉRIFIÉ : fidélité mot à mot de plusieurs phrases secondaires dans les échanges nocturnes et le vestiaire — commande de relecture : `ffplay -autoexit youtube-clips/horizontal/clip-07.mp4` (à répéter pour 08–12 et 14–18, avec contrôle à l’écoute).

NON VÉRIFIÉ : droits de réutilisation, accord des personnes visibles, droits sur les musiques éventuelles et statut commercial des marques — aucune commande ne prouve ces autorisations ; il faut les documents du détenteur des droits.

NON VÉRIFIÉ : explication de la réforme des divisions dans le clip 02 et certains noms de joueurs — pas de confirmation indépendante. Les propos sont ceux de la vidéo.

# Achh10 — sélection et découpes

Livraison du 12 octobre 2026 : **18 extraits**, dont **17 de 20 à 60 secondes et un micro-extrait de 14,90 secondes**. Chaque extrait existe en horizontal et en brouillon vertical, soit 36 MP4. Aucun titre, bruitage, musique ou motion design ajouté. Les sous-titres, inserts et animations déjà incrustés dans la vidéo restent présents.

## Source et méthode

Vidéo : [#41 Des DEBUTS en N2 TRÈS COMPLIQUÉ ! AchhLife Saison 3 épisode 3](https://www.youtube.com/watch?v=8T0INMoppoY), chaîne Achh10. Téléchargement effectué après l’autorisation explicite « si telecharge ». Il s’agit de la version YouTube recompressée, pas de l’original caméra.

| Élément | Résultat ffprobe |
|---|---|
| Durée | 1 566,975 s — 26 min 06,975 s |
| Image | 1 920 × 1 080, 16:9, H.264, 30 images/s |
| Couleur | SDR, 8 bits, yuv420p, BT.709 ; aucune métadonnée HDR détectée |
| Audio | Une piste AAC, stéréo, 44 100 Hz, environ 128 kbit/s |
| Taille source | 534 150 612 octets — conservée uniquement sur ce PC |

Transcription intégrale avec faster-whisper large-v3-turbo, français, CPU int8 et temps par mot ; relectures ciblées avec large-v3 pour les passages difficiles. Aucun recours au modèle medium. La version consolidée contient 2333 mots. Les estimations temporelles corrigées manuellement sont signalées dans le JSON. Le SRT reste une base de travail, surtout dans les passages avec des voix superposées.

Toute la vidéo a été parcourue par 13 planches, une image toutes les 5 secondes. Les 18 planches horizontales et les 18 planches verticales de 8 images ont été relues. Le récapitulatif initial, les longs passages de jeu et les montages musicaux ont été écartés de la sélection parlée.

Les silences ont été repérés avec `silencedetect=noise=-32dB:d=0.12` ; les coupes visent environ 0,15 s autour de la parole. Certaines répliques se suivent sans silence exploitable : les limites suivent alors la phrase, avec un fondu audio de 30 ms. Les temps par mot sont des estimations ; les écarts de reconnaissance aux limites sont indiqués, pas masqués.

## Classement

La note évalue l’intérêt éditorial, pas les droits de publication. Pour tous les extraits : droits vidéo, accord des tiers, musique éventuelle et statut commercial des marques non confirmés. Les risques particuliers sont indiqués dans le tableau ; le JSON contient le détail.

| N° | Début–fin source | Durée | Titre proposé | Accroche transcrite des 3 premières secondes | Note /10 | Risque particulier | Vérification H / V |
|---|---|---:|---|---|---:|---|---|
| 18 | 21:22.880–21:56.200 | 33.32 s | Est-ce que vous y croyez | Marquez, vous allez voir comment ça va se transformer. Allez, | 9.3 | Quelques formulations secondaires restent difficiles à distinguer | OK / OK |
| 10 | 12:26.830–12:56.620 | 29.79 s | C'est une obligation | Les gars, tout le monde est | 9.0 | Quelques mots du milieu du discours restent incertains | OK / OK |
| 05 | 06:14.220–06:47.850 | 33.63 s | Chaque erreur compte | défaite 3-2 malheureusement après avoir mené | 8.9 | Pas de risque particulier repéré | OK / OK |
| 13 | 18:59.830–19:25.480 | 25.65 s | Je vous laisse 10 minutes | Allez, allez, on lève la tête, on est pas dedans, on est | 8.9 | Animation d'abonnement YouTube déjà incrustée dans la source et conservée | OK / OK |
| 12 | 13:25.480–13:48.150 | 22.67 s | C'est le cœur | Par contre, l'instinct ce n'est pas la tête, | 8.8 | Chevauchement de 3,66 s avec le clip 11 : choisir l'un des deux dans une même compilation ; Quelques réponses et noms de joueurs restent incertains | À relire : début ASR, fin ASR / À relire : début ASR, fin ASR |
| 16 | 20:18.400–20:44.330 | 25.93 s | On va les faire trembler | On peut pas dire qu'on s'est ouvert quand on a perdu 2-0. | 8.8 | Références aux occasions déjà vécues dans le match ; Quelques formulations peu intelligibles | OK / OK |
| 14 | 19:26.270–19:51.780 | 25.51 s | Faites-vous violence | Faites-vous violence, trouvez les mots, | 8.7 | Gros mot final : putain ; Une formulation à la fin reste incertaine | OK / OK |
| 17 | 20:49.380–21:18.220 | 28.84 s | C'est fini les discours | On n'a aucun deuxième ballon ! | 8.5 | Gros mot : couilles | OK / OK |
| 07 | 10:05.000–10:35.560 | 30.56 s | 200 patates mon frère | je coupe ce doigt. Juste un ? | 8.4 | Débat hypothétique sur la perte d'un doigt ; Gros mot : putain ; Paroles familières et certaines réponses difficiles à distinguer | À relire : fin ASR / À relire : fin ASR |
| 09 | 11:15.150–11:58.650 | 43.50 s | Presque un demi-million | Quand tu manges, tu utilises les 3 | 8.3 | Débat hypothétique sur la perte d'un doigt ; Référence au débat précédent : comprendre la proposition nécessite le contexte visuel | OK / OK |
| 02 | 02:45.340–03:13.660 | 28.32 s | La poule la plus dure | c'est la poule la plus dure de National 2. Ah oui, | 8.2 | Présentation des divisions et de leur réforme : exactitude sportive non vérifiée | OK / OK |
| 01 | 02:17.450–02:39.800 | 22.35 s | Premier match officiel et premier trophée | premier match officiel et premier trophée | 8.1 | Animation d'abonnement YouTube déjà incrustée dans la source et conservée | OK / OK |
| 06 | 06:50.330–07:22.700 | 32.37 s | Pas encore aux normes | Match face à Rousset, équipe qui vient de | 8.0 | Le recadrage sur le visage coupe une partie des sous-titres déjà incrustés dans la source ; utiliser l'horizontal pour refaire l'habillage | OK / OK |
| 11 | 12:59.810–13:29.140 | 29.33 s | L'instinct et l'intuition | de l'instinct et de l'intuition, c'est votre force, | 8.0 | Plusieurs formulations du milieu du discours sont peu intelligibles | OK / OK |
| 04 | 05:08.740–05:23.640 | 14.90 s | Je ne vais pas pouvoir jouer | Pour ma part, malheureusement, je ne vais pas pouvoir jouer ce premier | 7.9 | Micro-extrait de 14,90 s, en complément des 17 extraits de 20 à 60 s ; Le recadrage sur le visage coupe une partie des sous-titres déjà incrustés dans la source ; utiliser l'horizontal pour refaire l'habillage | OK / OK |
| 08 | 10:39.700–11:13.600 | 33.90 s | Tu fais quoi avec 200000 | Tu fais quoi avec 200 000 après | 7.8 | Contexte du débat hypothétique sur la perte d'un doigt ; Voix et rires superposés | OK / OK |
| 15 | 19:52.680–20:18.230 | 25.55 s | On est trop gentil | Oh soyez plus vicieux les mecs, ils font que parler, ils font mes | 7.7 | Gros mot : couilles ; Propos : mettez des coups, rentrez-leur dedans, cassez le jeu ; risque d'être perçu comme une promotion des fautes ; Quelques formulations peu intelligibles | OK / OK |
| 03 | 03:23.200–03:49.830 | 26.63 s | La réserve du MHSC | pour commencer bien évidemment la | 6.8 | Accroche progressive ; ouvre par Pour commencer | OK / OK |

Le clip 03 garde une entrée progressive (« Pour commencer ») : une ouverture sur « la réserve du MHSC » vers 205,47 s serait plus directe, avec moins de respiration avant la phrase. Le 04 est volontairement un micro-extrait : la version longue diluait l’annonce et renvoyait au résumé du match. Le 11 commence sur l’instinct après suppression de l’introduction. Les clips 11 et 12 partagent 3,66 s : éviter de les publier ensemble dans une compilation.

## Brouillons verticaux

Les clips 04 et 06 suivent le visage à partir d’une détection MediaPipe à 4 images/s, avec médiane sur 5 échantillons, amortissement et interpolation continue. Les 16 autres gardent l’image entière centrée sur un fond flou : plusieurs interlocuteurs, vestiaire, tableau, logos, photos ou images de match.

Sur 04 et 06, le visage reste dans le cadre mais les sous-titres déjà incrustés sont coupés sur les côtés. Utiliser les horizontaux comme base pour refaire les sous-titres et l’habillage. Les scènes 07–09 restent sombres ; le mouvement de caméra vient de la source. Les 01 et 13 conservent une animation d’abonnement YouTube de la source.

## Vérification des fichiers livrés

Les 36 fichiers ont été retranscrits séparément et décodés jusqu’au bout avec `ffmpeg -v error -i fichier -f null -`. **16/18 extraits ont leurs deux formats marqués OK** pour la comparaison des quatre premiers et quatre derniers mots, le décodage, la durée, la résolution, les codecs et la taille. Les éventuels problèmes restants figurent dans le tableau et dans `diagnostic/verification-NN-format.json`.

Audio : loudnorm en deux passes à −14 LUFS, fondus de 30 ms, AAC à débit cible 192 kbit/s. Le gain a été affiné après mesure du fichier AAC quand nécessaire. Niveau final mesuré : **-14.10 à -13.94 LUFS**. Les niveaux et pics vrais figurent dans `diagnostic/controle-final.json`.

Image : H.264 CRF 18, horizontal 1920×1080, vertical 1080×1920, 30 images/s. **Plus gros MP4 : 27.84 Mo** ; tous sont strictement sous 100 000 000 octets. Aucun débit vidéo n’a dû être abaissé pour passer la limite.

La comparaison ignore la ponctuation, les accents et la variation orthographique « important/importants », qui a le même son. En cas d’écart, les 8 premières et dernières secondes ont aussi été retranscrites. Les résultats bruts restent disponibles. Un OK technique aux limites ne certifie pas chaque mot du milieu de la transcription ni une écoute humaine continue.

Les pistes 03, 05, 06 et 16 ont été renormalisées en deux passes depuis la source avec une marge de −6 dBTP avant l’AAC, puis ajustées à −14 LUFS. Cette marge absorbe les pics créés par l’encodage et la conversion. Les images ont été copiées sans réencodage. Les pics vrais mesurés des fichiers finaux sont tous sous 0 dBTP.

Les passages difficiles ont aussi été reconnus sans suppression des silences, avec un vocabulaire de contexte et un silence ajouté uniquement à l’entrée du moteur de transcription. Cette aide ne modifie pas les MP4. Sur 07, la fin est placée dans le silence mesuré 635,407–635,688 s : le texte des derniers mots reste à confirmer si l’ASR ne les restitue pas. Sur 12, les modèles confondent notamment l’instinct et le nom Atlas malgré les sous-titres source ; l’écart reste indiqué.

## Trois idées de compilation

Idées seulement : aucun montage de compilation rendu. Les temps ci-dessous sont les secondes exactes de la source, dans l’ordre proposé. Les jonctions devront être écoutées au moment de l’assemblage.

1. **Défaite, lucidité, réaction** — 374,22–380,33 ; 396,39–407,85 ; 1282,88–1285,19 ; 1312,73–1316,20. Environ 23,35 s. Le renversement de 2–0 à 3–2, la leçon de la défaite, puis l’appel à courir. Les deux dernières pièces viennent du clip 18 et montrent un autre moment du match : présenter cette suite comme un thème, sans fabriquer une chronologie.
2. **Les obligations d’un joueur** — 746,83–754,87 ; 761,35–764,09 ; 770,05–776,62 ; 1166,27–1171,27 ; 1312,73–1316,20. Environ 25,82 s. Responsabilités, contre-pressing, engagement, gestes de remobilisation et courses. Quelques mots intermédiaires restent à confirmer avant de poser de nouveaux sous-titres.
3. **Le prix d’un petit doigt** — 605,00–607,90 ; 619,55–625,07 ; 639,70–647,83 ; 700,75–718,65. Environ 34,45 s. La proposition, l’inutilité supposée du doigt, Marrakech et la chute à quatre cent mille. Débat hypothétique et langage familier ; les gestes et réactions doivent rester visibles. Revoir les jonctions des deux dernières répliques à l’écoute.

## Les cinq premiers à publier

Après confirmation des droits de réutilisation : **18 → 10 → 05 → 13 → 01**. Le 18 porte l’émotion, le 10 un conseil concret, le 05 le renversement de score, le 13 la pression de l’entraîneur, puis le 01 une réussite collective. Le 13 et le 01 gardent l’animation d’abonnement de la source : à traiter lors de la session d’habillage.

## Corrections consignées

Les corrections ci-dessous s’appuient sur les sous-titres, logos et tableaux visibles dans la vidéo. Elles corrigent une transcription ; elles ne vérifient pas les affirmations sportives. « Sussargue » reprend l’orthographe incrustée dans la source. Les expressions remplacées gardent un intervalle temporel estimé.

| Temps source | Avant | Après | Appui |
|---|---|---|---|
| 03:56.380 | bokehrois | Beaucairois | Sous-titres, logos ou tableau incrustés dans la source |
| 04:05.640 | Rivera. | Riviera. | Sous-titres, logos ou tableau incrustés dans la source |
| 04:17.620 | Espali | Espaly | Sous-titres, logos ou tableau incrustés dans la source |
| 04:19.700 | Luciana | Lucciana | Sous-titres, logos ou tableau incrustés dans la source |
| 04:33.560 | Payad | Paillade | Sous-titres, logos ou tableau incrustés dans la source |
| 04:35.480 | Espagie | Espaly | Sous-titres, logos ou tableau incrustés dans la source |
| 07:03.520 | Suissard | Sussargue | Sous-titres, logos ou tableau incrustés dans la source |
| 13:00.100 | 'espectre | 'instinct | Sous-titres, logos ou tableau incrustés dans la source |
| 13:06.920 | 'espectre, | 'instinct, | Sous-titres, logos ou tableau incrustés dans la source |
| 13:15.560 | 'espectre, | 'instinct, | Sous-titres, logos ou tableau incrustés dans la source |
| 13:18.560 | 'espectre, | 'instinct, | Sous-titres, logos ou tableau incrustés dans la source |
| 13:01.900 | enfance, | force | Sous-titre visible vers 13:01 |
| 02:11.240 | canne qu | CAN qu | Trophée africain visible et mention du Maroc à 02:11 |
| 03:27.150 | mhc qui | MHSC qui | Logo de Montpellier visible à 03:27 |
| 03:46.550 | la s saint etienne qui | l’AS Saint-Étienne qui | Logo de Saint-Étienne visible à 03:47 |
| 04:03.080 | 'US Monde de Lieux, | US Mandelieu, | Logo et tableau des adversaires visibles à 04:03 |
| 04:04.340 | Canet Rocheville | Cannet-Rocheville | Logo du Cannet-Rocheville visible à 04:05 |
| 04:36.540 | 'US Mondelieu Donc | US Mandelieu Donc | Même nom que le logo présenté à 04:03 |
| 10:24.580 | procédé. | posé. | Sous-titre incrusté vers 10:24 |
| 13:08.300 | le matin d'aujourd'hui, | un match à domicile, | Sous-titre incrusté à 13:09 |
| 13:13.640 | les mots derrière, | encore les noms derrière, | Sous-titre incrusté à 13:14 |
| 13:30.080 | la face. | l’Atlas. | Sous-titre incrusté vers 13:30, nom du club déjà présenté |
| 19:02.120 | bien dedans, | pas dedans, | Sous-titre à 19:02 : on est pas dedans |
| 19:07.940 | C'est fini, | T’es puni, | Sous-titre incrusté vers 19:08 |
| 19:09.340 | c'est fini. | t’es puni. | Même répétition à 19:09 |
| 19:37.680 | court, | fou, | Sous-titre incrusté vers 19:38 : rendez ce match fou |
| 21:16.520 | marcha, on | en marchant, on | Sous-titre incrusté à 21:16 |
| 21:49.560 | te ramener des étoiles les | demander des efforts les | Sous-titre incrusté vers 21:50 |
| 10:45.480 | une barre à | une dar à | Sous-titre source à 10:46 : une dar à Marrakech |
| 13:46.720 | la face, | à Atlas, | Sous-titre source à 13:47 : il est à Atlas |
| 19:07.940 | T’es puni, | C’est puni, | Sous-titre source à 19:08, première occurrence |
| 05:14.910 | fédéral | amateur | Sous-titre visible dans le clip 04 : reclassé amateur |
| 12:59.160 | de : début estimé à 779.16 s | de : début estimé à 779.82 s | La retranscription du fichier 11 reconnaît de l’instinct ; sous-titre source visible dans sa première image |
| 20:18.820 | ne | [retiré] | Sous-titre source et retranscription du fichier 16 : On peut pas dire, négation orale sans ne |

Les faux mots « Sous-titrage ST’501 » produits par la reconnaissance ont été supprimés. Aucun « FoundClub » ou « Ergysport » intelligible n’a été repéré dans la transcription ; ces exemples du brief n’ont pas été ajoutés artificiellement.

## Fichiers et reproduction

- `horizontal/clip-NN.mp4` : 18 coupes au format source.
- `vertical/clip-NN-9x16.mp4` : 18 brouillons 9:16.
- `planches/clip-NN.jpg` : 18 planches de 8 images, avec 18 planches verticales supplémentaires.
- `planches/source/` : repérage de toute la vidéo à 5 secondes d’intervalle.
- `transcription/transcription.srt`, `transcription-mots.json`, `transcription.txt`, `corrections.json` : transcription et corrections.
- `extraits.json` : sélection, textes, risques, recadrage, vérification et tailles.
- `diagnostic/` : silences, détection des visages, mesures sonores et retranscriptions des exports.
- `source/provenance.json`, `source/ffprobe.json` : identification de la source.

La source de 534 Mo, les modèles, l’environnement local et les fichiers de travail sont exclus de Git par `youtube-clips/.gitignore`. Ils restent sur ce PC. Le dépôt reçoit les coupes et les livrables ; les autres dossiers de vidéos ne sont pas modifiés.

Pour relancer sur ce PC depuis la racine du dépôt :

```powershell
ffprobe -v error -show_format -show_streams -of json youtube-clips/source/ach10-source.mp4
& .\youtube-clips\.cache\venv\Scripts\python.exe youtube-clips/outils/exporter.py
& .\youtube-clips\.cache\venv\Scripts\python.exe youtube-clips/outils/limiter-pics.py
& .\youtube-clips\.cache\venv\Scripts\python.exe youtube-clips/outils/ajuster-son.py
& .\youtube-clips\.cache\venv\Scripts\python.exe youtube-clips/outils/verifier.py
& .\youtube-clips\.cache\venv\Scripts\python.exe youtube-clips/outils/finaliser.py
```

## CE QUE JE N’AI PAS PU TRANCHER

- Plusieurs paroles secondaires de 07–12 et 14–18 restent difficiles à distinguer, malgré les deux modèles et la relecture des sous-titres d’origine. Il faut une écoute humaine avant d’en faire des citations ou des sous-titres définitifs.
- L’orthographe des surnoms ou prénoms Napsou, Nassim/Souley et Naïf/Naït n’est pas suffisamment établie. Ils ne servent pas d’accroches.
- L’orthographe administrative du lieu transcrit « Sussargue », les explications de qualification et la réforme des divisions ne sont pas confirmées indépendamment.
- Les autorisations de réutilisation et de droit à l’image ainsi que les licences de musique éventuelle ne sont pas connues. La présence d’un logo ne prouve pas un partenariat rémunéré. Si un passage relève effectivement d’une collaboration commerciale, prévoir la mention « Collaboration commerciale » lors de l’habillage.
- Les sous-titres incrustés dans 04 et 06 ne peuvent pas être récupérés proprement par le recadrage sur le visage ; les versions horizontales sont conservées pour la prochaine session.
