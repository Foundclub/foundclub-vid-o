# Clips « Match bourbier » — sélection et découpes

Épisode : « Match bourbier contre cette R3 » (AchhLife, chaîne Achh10, https://www.youtube.com/watch?v=1lt7P7i2enI), 22:39, 1920×1080, 30 i/s. Téléchargé par Adel sur son PC le 23/10/2026, poussé en 12 morceaux dans `a-monter/bourbier/`.
Le match : Montpellier Atlas Paillade (N2, l'équipe d'Achraf, maillot noir DGL Groupe) bat Saint-Orens (R3, en rouge) 3-0, au 3ᵉ tour de la Coupe de France, sur un terrain pelé.

## Méthode

- Transcription complète avec Whisper turbo en local (sherpa-onnx, `ach10/outils/transcrire.py`) : 148 passages, `transcription.srt`. C'est une base de travail : sous la musique et dans le vestiaire, beaucoup de mots sont mal reconnus.
- Tout l'épisode parcouru en planches (une image toutes les 4 s, puis une par seconde sur la 2ᵉ mi-temps pour trouver les buts).
- Bornes calées sur les passages de voix ; mots de fin vérifiés avec `ach10/outils/caler_mots.py` (« finale » à 726,46 s, « rêver » à 368,32 s). Fondu audio de 30 ms aux deux bouts, son à -14 LUFS en deux passes.
- Écartés : le résumé de l'épisode précédent (7:00-10:00, déjà découpé dans `youtube-clips/`), la causerie « leçon de sacrifice » (6:08-6:58, images France 3 d'une autre équipe), l'entraînement en musique, la bande-annonce du prochain épisode.

## Classement

| N° | Source | Durée | Titre | Note /10 | Ce qui fait l'intérêt | Risques |
|---|---|---:|---|---:|---|---|
| 10 | 20:23.60-20:53.00 | 29.4 s | « Un champ de patate ! » | 9.2 | La phrase de la miniature, dite par le président du club, puis les enfants qui fêtent la qualification | Accord du président et des enfants visibles (mineurs : accord des parents) |
| 04 | 04:55.25-05:43.45 | 48.2 s | 10 000 personnes à la Mosson | 9.0 | Le stade devant lequel on passe tous les jours, et cette fois on est dedans | Images d'archives de diffuseurs télé (France 3, Eurosport, beIN…) : droits non détenus, la voix est celle d'Achraf |
| 08 | 15:58.70-16:54.40 | 55.7 s | « L'état du terrain, pas de risque » | 8.8 | 0-0 à la pause sur un terrain pelé : le coach adapte le plan au champ de patate, en lien direct avec la miniature | Plusieurs consignes peu intelligibles (« coufras », « poétilleux ») : sous-titres à relire à l'écoute ; Accord des joueurs visibles dans le vestiaire |
| 07 | 12:20.30-12:57.95 | 37.6 s | Je saute, je combats, j'agresse | 8.7 | Le vestiaire, l'intensité du coach : le genre de passage qui marche le mieux (clips 18 et 10 du #41) | Plusieurs mots du coach peu intelligibles (musique et écho) ; Accord des joueurs visibles dans le vestiaire |
| 09 | 17:19.50-17:34.00 + 17:50.00-18:09.00 + 19:13.00-19:27.50 | 48.0 s | Les 3 buts | 8.5 | Les trois buts d'Atlas Paillade avec leurs célébrations, en moins d'une minute | Musique éventuelle sous les images de match : droits à vérifier ; Pas de parole : il faudra une accroche écrite |
| 02 | 01:24.95-02:01.40 | 36.5 s | Face à Dijon, la meilleure prestation de ma carrière | 8.4 | Un amateur face aux joueurs de Ligue 1 qu'il voyait à la télé | Images d'archives de diffuseurs télé (France 3, Eurosport, beIN…) : droits non détenus, la voix est celle d'Achraf ; Noms des joueurs de Dijon mal reconnus par la transcription (Lees-Melou, Marvin Martin, Balmont) : à vérifier si on les écrit |
| 15 | 14:34.00-15:14.00 | 40.0 s | Le champ de patate vu du drone | 8.2 | La preuve en images du « champ de patate » : à coupler avec la phrase du président (clip 10) ou la miniature | Pas de parole, musique de montage sous les images : droits de la musique à vérifier, il faudra une accroche écrite |
| 03 | 04:13.10-04:55.35 | 42.2 s | Éliminé par Bergerac… qui tire l'OL au tour d'après | 8.0 | Le coup du sort : perdre, et voir l'adversaire tirer le club qu'on supporte | Images d'archives de diffuseurs télé (France 3, Eurosport, beIN…) : droits non détenus, la voix est celle d'Achraf ; Nom du club (« jurado law football ») mal reconnu : à vérifier |
| 06 | 11:37.30-12:06.60 | 29.3 s | Comment marche la Coupe de France | 7.9 | Explique qui entre à quel tour : utile pour les joueurs amateurs, et cite l'adversaire R3 | « Ligue 3 » au 5e tour : à vérifier avec le règlement 2026-2027 |
| 20 | 15:58.70-16:19.30 | 20.6 s | « Pas de panique, 0-0 » | 7.9 | Les 20 premières secondes de la causerie : format court pour TikTok et Shorts | Chevauche le clip 08 : choisir l'un ou l'autre ; Accord des joueurs visibles dans le vestiaire |
| 05 | 05:43.50-06:08.45 | 24.9 s | On a toujours le droit de rêver | 7.8 | Conclusion courte et partageable | Images d'archives de diffuseurs télé (France 3, Eurosport, beIN…) : droits non détenus, la voix est celle d'Achraf |
| 16 | 17:16.00-17:40.50 | 24.5 s | Le premier but | 7.8 | Le 1-0 de Naït Imaghran avec sa célébration et son ralenti | Pas de parole, musique de montage sous les images : droits de la musique à vérifier, il faudra une accroche écrite ; Chevauche le clip 09 (les 3 buts) : ne pas publier les deux ensemble |
| 17 | 17:46.00-18:19.50 | 33.5 s | Le deuxième but | 7.8 | Le 2-0 avec sa célébration et son ralenti | Pas de parole, musique de montage sous les images : droits de la musique à vérifier, il faudra une accroche écrite ; Chevauche le clip 09 (les 3 buts) : ne pas publier les deux ensemble |
| 18 | 19:10.00-19:41.50 | 31.5 s | Le troisième but | 7.8 | Le 3-0 de Camara qui tue le match, avec son ralenti | Pas de parole, musique de montage sous les images : droits de la musique à vérifier, il faudra une accroche écrite ; Chevauche le clip 09 (les 3 buts) : ne pas publier les deux ensemble |
| 01 | 00:28.90-01:24.85 | 56.0 s | La Coupe de France, ce n'est pas qu'une compétition | 7.6 | Texte écrit et posé, qui donne le ton de toute la saison de Coupe | Images d'archives de diffuseurs télé (France 3, Eurosport, beIN…) : droits non détenus, la voix est celle d'Achraf |
| 14 | 12:59.00-13:51.00 | 52.0 s | L'entrée des joueurs | 7.4 | Le couloir avec les arbitres, l'entrée avec les enfants, la composition, le coup d'envoi vu du drone | Pas de parole, musique de montage sous les images : droits de la musique à vérifier, il faudra une accroche écrite ; Enfants visibles : accord des parents |
| 12 | 00:00.00-00:28.85 | 28.9 s | « Unique. Magique. Exceptionnel. » | 7.0 | Une suite de mots forts sur des images de légende de la Coupe : bonne accroche visuelle | Images d'archives de diffuseurs télé (France 3, Eurosport, beIN…) : droits non détenus, la voix est celle d'Achraf |
| 19 | 19:59.00-20:23.40 | 24.4 s | Le coup de sifflet final | 7.0 | La qualification pour le 4e tour, les joueurs avec les enfants du club | Pas de parole, musique de montage sous les images : droits de la musique à vérifier, il faudra une accroche écrite ; Enfants visibles : accord des parents |
| 11 | 21:07.10-21:23.20 | 16.1 s | Victoire 3-0, direction le 4e tour | 6.9 | Micro-extrait de 16 s qui annonce la suite (derby contre la réserve du MHSC) | Extrait court : plutôt en fin de compilation ou en story |
| 21 | 21:23.00-21:56.00 | 33.0 s | Dans le prochain épisode : le derby | 6.5 | Annonce le derby contre la réserve du MHSC : à publier juste avant l'épisode suivant | Images du prochain épisode, pas de celui-ci ; Plusieurs phrases peu intelligibles sous la musique |
| 13 | 10:12.20-11:04.80 | 52.6 s | L'entraînement du vendredi | 6.0 | Vue de drone de la séquence de jeu de la veille, puis le groupe réuni | Pas de parole, musique de montage sous les images : droits de la musique à vérifier, il faudra une accroche écrite |

Tous les extraits : accord des personnes visibles et droits de réutilisation non confirmés.

Vérifié sur les planches le 23/10/2026 : les extraits 01 à 05 sont faits d'images de diffuseurs (Eurosport, France 3, panneaux KFC et Coupe de France ; le 02 montre le vrai Louhans-Cuiseaux - Dijon filmé par Eurosport). Le 12 aussi (l'ouverture). Les extraits 06 à 11 et 13 à 21 sont des images de la chaîne d'Achraf (vestiaire, match avec le tableau d'affichage 0-1, 0-2, 0-3, le président, les enfants). Les 42 fichiers se décodent sans erreur, tous sous 100 Mo ; son mesuré entre -14,5 et -13,7 LUFS, crête au plus haut à -0,4 dBFS (clip 09).

Chevauchements : 16, 17 et 18 (chaque but seul) reprennent des images du 09 (les 3 buts) ; le 20 est le début du 08. Ne pas publier les deux d'une même paire le même jour.

## Fichiers

- `horizontal/clip-NN.mp4` : 1920×1080, l'extrait tel quel.
- `vertical/clip-NN-9x16.mp4` : brouillon 1080×1920, l'image entière centrée sur un fond flou (à habiller ensuite avec le gabarit de `youtube-clips/habillage/`).
- `planches/clip-NN.jpg` : 8 images de l'extrait.
- Refaire : `outils/recoller.sh ; python3 -I outils/exporter.py [numéros]`.
