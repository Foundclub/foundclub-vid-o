# Prompt à coller dans la session locale (Claude Code sur le PC d'Adel)

Réglage : Opus · effort `high` · sans ultracode — un long travail en plusieurs étapes validées, pas un audit.
Ouvrir la session dans `D:\App\video\foundclub-vid-o` (faire `git pull` avant).

```
Tu vas monter un épisode AchhLife (la série YouTube d'Achraf Berriss, chaîne Achh10) : une interview avec beaucoup de
plans de coupe, 2 à 3 h de rushs. Tu travailles en local sur mon PC (Windows, PowerShell, RTX 3070 Ti).

AVANT TOUT GESTE, lis en entier :
1. D:\App\video\foundclub-vid-o\METHODE_MONTAGE.md — comment je travaille, les outils du dépôt, le style validé,
   les pièges déjà payés, la marche à suivre pour un épisode long. C'est la mémoire de la session précédente.
2. D:\App\video\foundclub-vid-o\README.md — les projets déjà faits et leurs outils.

LES RUSHS : dans <DOSSIER_DES_RUSHS> (je te le donne si ce n'est pas rempli). Environ 30 fichiers :
- DJI_20260909…_D : des vues de drone (ville, immeubles, stade), tournées le 9 septembre ;
- DJI_20261026…_D : l'interview et les plans du 26 octobre (Achraf avec un autre homme, en marchant, au restaurant,
  le soir au stade) ;
- 1, 2, 3 : sans doute filmés au téléphone.
Ils ne vont JAMAIS dans git (100 Mo maximum par fichier sur GitHub) : tout ce qui est lourd reste hors du dépôt.

CE QUE TU FAIS, DANS CET ORDRE, ET TU T'ARRÊTES À CHAQUE VALIDATION :
0. Vérifie l'outillage et dis-moi ce qui manque : ffmpeg avec h264_nvenc, Python avec faster-whisper sur CUDA,
   Node et npx hyperframes, un Chrome pour le rendu. N'installe rien sans me le dire.
1. L'INVENTAIRE (étape 1 du §6 de METHODE_MONTAGE.md) : durée, caméra, son, copies légères, planches, transcription
   de tout ce qui parle. Puis tu me racontes en mots simples ce qu'il y a dans les rushs : qui parle, de quoi, les moments forts.
2. LE PAPIER DE MONTAGE : l'histoire de l'épisode en phrases de l'interview, dans l'ordre, avec les plans de coupe et la
   durée visée. Tu imites le style des épisodes d'Achraf (§3 de METHODE_MONTAGE.md, regarde l'épisode #42).
   → Je valide le papier avant que tu montes quoi que ce soit.
3. LE PREMIER MONTAGE, par séquences, avec un aperçu par séquence. → Mes retours.
4. LA FINITION : habillage, sous-titres, musique, son à -14 LUFS, rendu final depuis les rushs d'origine, vérifié.

À chaque message de fond, termine par « ⚖️ CE QUE TU DOIS DÉCIDER » (numéroté, avec ta recommandation et le format de
réponse). Les noms propres que tu n'as pas pu vérifier, tu me les listes au lieu de les inventer.
```
