# Épisode AchhLife « Moussa » — ce qu'il y a dans les rushs

Inventaire du 27/10/2026. Les chiffres viennent de `inventaire.json` (`outils/inventaire.py`) et de `outils/mesurer_son.py`.
Les instants sont en min:s **dans chaque rush**.

- **Rushs d'origine** : `D:\Foundclub média\ACh\` (27 fichiers, 13,5 Go, 66,8 min). Ils ne vont jamais dans git.
- **Copies de travail** : `D:\App\video\rushs\interview\travail\`, avec `proxies/` (720p), `son48/`, `son16/`, `planches/` (une image toutes les 5 s) et `transcriptions/` (faster-whisper large-v3-turbo, 11 059 mots).
  - `outils/preparer_rushs.py` puis `outils/transcrire_rushs.py` les refont.

## Les caméras

- **DJI Mini 5 Pro (drone)** : 13 plans du 09/09/2026, 4K à 59,94 i/s, sans son, 5,2 min en tout. Ils montrent les immeubles de la Paillade, le stade de la Mosson et le terrain d'entraînement d'à côté.
- **DJI Osmo Pocket 3** : 14 fichiers du 26/10/2026, 1080p à 29,97 i/s, son stéréo à 48 kHz.
  - `1`, `2` et `3` sont des fichiers de cette caméra, renommés : **ce n'est pas un téléphone**.
  - Aucun fichier n'en chevauche un autre dans le temps : il n'y a qu'**une caméra à la fois** et pas de micro séparé, donc rien à synchroniser.
  - La personne qui filme est appelée « Jib » ou « Gilles » (nom à vérifier).

## Rush par rush (Osmo, dans l'ordre du tournage)

| Rush | Durée | Où | Ce qui s'y passe | Son |
|---|---|---|---|---|
| `1` | 0:21 | parking, face caméra | **Ouverture** : « Aujourd'hui dans AchhLife, je vais vous faire la présentation d'un joueur qui joue avec moi à l'Atlas Paillade… de la 5ᵉ division de district à la National 2… le meilleur 6 d'Occitanie… je vais vous présenter Moussa, c'est parti. » | propre, un peu faible (-23,5 LUFS) |
| `2` | 5:54 | boulangerie-pizzeria, galerie, voiture | « Tu nous emmènes où ? » ; la pizza « capricciosa » ; les rencontres du quartier ; Ryan, un camarade du CP ; « on va au stade » (5:20) | saturé par endroits (4:00–5:05, dans la voiture) |
| `3` | 10:17 | entrée du stade, bureau du club, trophées | La blague du PSG à l'entrée ; la coupe d'Occitanie ; les vieilles photos d'équipe ; « il était en D5 » (6:12) ; **l'histoire des passes contre le mur en équipe 3 : « vous allez voir, dans quelques mois je jouerai en une »** (8:50–9:45) | saturé vers 9:13 |
| `0006` | 7:19 | parking près du terrain | Discussion tactique (3-5-2) avec un homme plus âgé, éducateur en district ; puis « viens voir la tribune » | brouhaha, passages saturés |
| `0007`, `0008` | 0:06, 0:30 | — | presque rien (80 % de silence) | — |
| `0009` | 2:40 | **tribune, assis, coucher de soleil** | **Début de l'interview** : sa présentation (25 ans, Atlas Paillade, créateur TikTok, 129 000 abonnés) ; « meilleur 6 d'Occitanie » ; la pique au « meilleur défenseur d'Île-de-France » ; ses débuts sur TikTok au retour du Portugal | **propre** |
| `0010` | 8:18 | tribune, la nuit tombe | **Sa carrière** : gardien à 7 ans, les petits clubs, la Suisse (2019), le Portugal (essais, réserve), **l'Algérie** (l'agent, le président qui ne vient jamais, l'intoxication), la D5, l'équipe 3, **viré de l'équipe 1 (« trop frêle »)**, la prépa où il s'incruste, titulaire, deux montées, National 2 ; « le foot, ça peut aller très vite » ; remplaçant en D1 à la 89ᵉ | **propre** |
| `0011` | 1:34 | stade la nuit, face caméra d'Achraf | Le terrain de son premier club, « toujours plein » ; le stade du MHSC collé au leur | propre |
| `0012` | 0:19 | — | rien (Whisper a inventé « Sous-titrage Société Radio-Canada ») | — |
| `0013` | 6:01 | clubhouse | Le thé marocain ; « c'est ça la beauté de l'Atlas » ; les figures du club ; long souvenir de la CAN au Maroc (hors sujet) | quelques saturations |
| `0014` | 6:35 | devant un snack, le soir | Bavardage de groupe : le dernier match, **le carton rouge de Moussa (« t'as pleuré ? »)**, la Coupe de France | **le plus abîmé : 83 s sur 394 touchées par la saturation** |
| `0015` | 0:05 | — | rien | — |
| `0016` | 11:39 | la Paillade la nuit, galerie de la Mosson | « La Paillade, 50 000 habitants » ; le « Brekna » ; les anciens coéquipiers : **« il était toujours remplaçant avec nous… vaut mieux commencer nul et être bon à la fin »** (5:44–7:35) ; **les deux dernières questions** : « au Moussa de 10 ans » et « aux jeunes de D5 », les passes et les frappes le matin quand les autres partaient à l'intérim (8:46–11:12) ; la conclusion d'Achraf (11:12–11:38) | saturé par endroits (3:46, 6:07) |

## Ce qui manque ou pose problème

- **Son** : l'interview assise (`0009`, `0010`) est propre.
  - Les scènes en marchant et en groupe saturent par moments (cris, rires, portières).
  - `0014` est le plus touché.
  - C'est à **écouter avant de garder un passage** ; un écrêtage ne se répare qu'en partie.
- **Promis à l'écran, absent des rushs** :
  - les anciennes vidéos TikTok de Moussa (« on vous mettra ça ») ;
  - ses réseaux « juste en dessous » ;
  - une photo de lui en gardien (il dit ne pas en avoir).
- **Personnes qui ne veulent pas apparaître** :
  - « On n'est pas dans la vidéo » (`2`, vers 4:44) ;
  - « tu vas pas passer, t'inquiète » (`0016`, vers 1:53) ;
  - « le boss de l'Atlas… il ne va jamais parler à la caméra » (`3`, vers 2:26).
- **À couper** : la plaisanterie sur un vendeur « à la sauvette » et l'Urssaf (`3`, 4:31–4:39).
- **Vides** : `0007`, `0008`, `0012` et `0015` sont inutilisables.

## Noms propres à vérifier (entendus par Whisper, non confirmés)

- **Personnes** :
  - Moussa « Arim » (nom de famille) ;
  - ses comptes « MoussalDZ » (TikTok, 129 000 abonnés) et « MousselDZ34 » (Instagram, « 1 500 » ?) ;
  - Slimane (vice-président, ancien entraîneur de l'équipe 3) et Ilyes (préparateur physique) ;
  - les entraîneurs « Sandrick » et « Geoffrey Dernis » ;
  - les figures du club « Suleyman Lella », « Mohamed Taoubi » et « Khalid Fekraoui » ;
  - les coéquipiers Nate, Samir, Bakhti, Adri ou Adriano, « Wahsin » ou « Mohsin », Malik, « Zahman » et Ryan ;
  - le gardien « Chaouchi ».
- **Clubs et lieux** :
  - « Paillade Mercure », Saint-Jean-de-Védas, Lattes, Pignan, les Arceaux, « Clermont-Est » et « Saint-Martin » (D5) ;
  - Urania Genève Sport et l'Olympique de Genève ;
  - « Estrella Madora » (Estrela da Amadora ?) et « Uniao Desimbrou » ;
  - Annaba ;
  - « essai du Rassud » et un « barrage en Père-Comte-Tarbe » ;
  - le « Brekna ».
- **Déjà confirmé** par l'épisode #42 : Montpellier Atlas Paillade (Whisper entend « Atlas Payad »), et BEN ALI Mahfoud, président du club.
