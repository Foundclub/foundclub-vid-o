NON VÉRIFIÉ : la vidéo longue correspondant à https://www.youtube.com/watch?v=8T0INMoppoY n'a pas été identifiée localement. Le brief contient encore `<CHEMIN DE LA VIDÉO ORIGINALE>`. Commande qui caractériserait le fichier une fois son chemin renseigné : `ffprobe -v error -show_format -show_streams -of json "CHEMIN_ORIGINAL_A_RENSEIGNER"`. Il faudra également regarder le fichier pour confirmer qu'il s'agit de la bonne vidéo ; ffprobe seul ne prouve pas son identité.

# Rapport de recherche de la source — ach10

Date : 11 octobre 2026. Dépôt : `D:\App\video\foundclub-vid-o`, branche `main`.

**Résultat : 0 extrait produit sur les 14 minimum demandés. Le travail de découpe reste à faire.** La source longue manque : aucune citation, aucun minutage et aucune note n'ont été inventés. Aucun média ni sous-titre n'a été téléchargé depuis YouTube.

## Recherche effectuée

- `D:\Vidéos\ach` est vide.
- Recherche des fichiers vidéo dans le dépôt, `D:\Vidéos`, `D:\Telechargement`, `D:\Vidéo`, `D:\LocalSend`, `D:\Foundclub média`, `D:\foundclub pub`, `D:\FoundClub`, ainsi que les dossiers Téléchargements, Bureau, Vidéos et Documents du profil `C:\Users\adelf`.
- Recherche élargie des extensions `.mp4`, `.mov`, `.mkv`, `.webm`, `.avi`, `.m4v`, `.mts` et `.m2ts` sur `D:\` et dans le profil utilisateur, avec exclusion de dossiers de dépendances, de jeux et de caches. Cela ne garantit pas l'absence d'un fichier ailleurs, sur un autre support, dans une archive ou sous une autre extension.
- Lecture des informations ffprobe des candidats au nom ambigu. Inspection de planches de trois images pour `Dessin ytb.mov` et `V4.4.mp4`.
- La consultation de la page YouTube a échoué (accès limité). Son contenu et sa durée n'ont donc pas pu être confirmés.

| Fichier examiné | Durée mesurée | Résolution | Conclusion |
| --- | ---: | --- | --- |
| `ach10/medias/video/ach10-original.mov` | 54,834 s | 1080 × 1920 | Vidéo courte FoundClub déjà utilisée dans le dépôt ; ce n'est pas une source longue. |
| `C:\Users\adelf\Downloads\ach vidéo brut.mov` | 54,834 s | 1080 × 1920 | Même durée et même taille que le candidat précédent ; aucun fichier long identifié. |
| `C:\Users\adelf\Downloads\IMG_1968.mov` | 25,833 s | 3840 × 2160 | Prise courte ; aucune source longue identifiée. |
| `D:\Telechargement\Dessin ytb.mov` | 252,775 s | 3840 × 2160 | Les images montrent une animation de présentation FoundClub. |
| `D:\Telechargement\V4.4.mp4` | 303,640 s | 3840 × 2160 | Les images montrent un film de présentation FoundClub avec scènes de terrain et écrans de l'application. Pas retenu comme source ach10. |
| `D:\Telechargement\V4.4 (1).mp4` | 303,640 s | 3840 × 2160 | Même durée et même taille que V4.4 ; identité octet par octet non vérifiée. |
| `D:\Telechargement\Duc.mp4` | 30,016 s | 1080 × 1920 | Fichier court ; aucune source longue identifiée. |

## Informations ffprobe du candidat « ach10-original »

Ces informations concernent **le candidat écarté**, pas la source YouTube demandée. La sortie complète est conservée dans `diagnostic/ach10-candidat-ffprobe.json`.

- Durée du conteneur : 54,834 s ; taille : 103 736 347 octets.
- Vidéo : H.264 High, 1080 × 1920, progressif, pixels `yuv420p` sur 8 bits.
- Cadence nominale : 30 images/s ; cadence moyenne : `822500/27417`, soit environ 30 images/s.
- Couleur : primaires, transfert et matrice BT.709, plage limitée. Les métadonnées indiquent du SDR, sans signalisation HDR PQ ou HLG.
- Audio : une piste AAC LC, stéréo, 44 100 Hz, environ 126 kbit/s.

## Transcription et corrections

La transcription entière et les horodatages mot par mot n'ont pas été produits, faute de source identifiée. Aucun fichier SRT vide n'a été créé pour simuler une transcription. Corrections de noms propres : aucune, car aucune transcription de la vidéo demandée n'a été effectuée.

FFmpeg, ffprobe et Python 3.13 sont disponibles. `faster-whisper` est installé ; OpenCV et MediaPipe ne sont pas disponibles dans le Python contrôlé. Aucun paquet ni modèle supplémentaire n'a été installé pendant cette recherche. Le modèle à utiliser pour la suite reste `large-v3-turbo`, en français, int8 sur CPU et avec horodatage des mots, conformément au brief.

## Extraits classés du meilleur au moins bon

| N° | Début–fin | Durée | Titre | Accroche exacte | Note | Risque | Vérification |
| --- | --- | --- | --- | --- | --- | --- | --- |
| — | — | — | Aucun extrait sélectionné | — | — | Non évalué | Impossible sans source |

`extraits.json` contient la liste vide `[]`. Il ne représente pas une sélection terminée.

## Compilations

Aucune compilation proposée : des thèmes ou des listes exactes de morceaux nécessitent d'abord la transcription et l'inspection de la bonne source.

## Ordre de publication conseillé

Les cinq premiers extraits à poster ne peuvent pas être déterminés sans contenu analysé.

## Exports et vérifications obligatoires

| Contrôle demandé | Résultat |
| --- | --- |
| Lecture de toute la transcription et planches toutes les 5 s | Non réalisé : source manquante. |
| Au moins 14 extraits autonomes, avec phrases complètes | Non réalisé : source manquante. |
| Limites de coupe dans les silences et marges de 0,15 s | Non réalisé : source manquante. |
| H.264 CRF 18, format d'origine, 1080p maximum, AAC 192 kbit/s | Aucun export. |
| Brouillons verticaux 1080 × 1920, suivi lissé ou fond flou | Aucun export. |
| Normalisation -14 LUFS en deux passes et fondus de 30 ms | Aucun export. |
| Planche de huit images par extrait | Aucun extrait à contrôler. |
| Retranscription de chaque export et comparaison des mots de début et de fin | Non réalisé : aucun export. |
| Décodage complet de chaque export | Non réalisé : aucun export. |
| Sponsors, musique, tiers, gros mots | Non évalués : source manquante. |
| Fichiers livrés inférieurs à 100 Mo | Seuls le rapport, la liste vide et le diagnostic texte sont livrés. |

Pour un futur export, le contrôle de lecture demandé sera : `ffmpeg -v error -i "youtube-clips/horizontal/clip-01.mp4" -f null -`, puis la même commande pour sa version verticale. Ce contrôle ne remplace pas la retranscription et la comparaison des premiers et derniers mots.

## Git et portée des changements

Les seuls fichiers ajoutés sont sous `youtube-clips/`. Les dossiers `ach10/`, `matchs-amicaux/`, `world-cup/` et `ergysport/` n'ont pas été modifiés. Le commit demandé porte sur **0 extrait** : il conserve ce diagnostic de source manquante, sans prétendre livrer les découpes.

## CE QUE JE N'AI PAS PU TRANCHER

- **Quel est le chemin exact du fichier original de la vidéo longue `8T0INMoppoY` ?** Le placeholder du brief n'a pas été remplacé et aucun candidat n'a été identifié avec certitude.
- L'identité, la durée, les pistes et l'éventuel HDR de cette source restent inconnus.
- La sélection des extraits, leurs risques et leur vérification restent intégralement à réaliser à partir de cette source.
