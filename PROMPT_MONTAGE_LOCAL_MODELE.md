# Prompt modèle — ouvrir une session de montage en local

Réglage : Opus · effort `high` · sans ultracode. Ouvrir la session dans `D:\App\video\foundclub-vid-o` après `git pull`.
Remplir les trois lignes entre crochets, puis coller tout le bloc.

```
Tu montes une vidéo pour FoundClub / AchhLife. Tu travailles en local sur mon PC (Windows, PowerShell, RTX 3070 Ti),
dans D:\App\video\foundclub-vid-o (fais `git pull` d'abord).

LA VIDÉO : [titre, et numéro NN/20 si c'est un script de la bibliothèque]
LES RUSHS : [D:\Foundclub média\ACh\<dossier>]
LE SCRIPT OU LA DEMANDE : [le texte du script, ou ce que je veux]

AVANT TOUT GESTE, lis en entier :
1. METHODE_MONTAGE.md : comment je travaille, les outils, le style validé, les pièges déjà payés, le suivi des scripts (§7).
2. README.md : la section de la vidéo la plus proche (week-end-gache\ est le modèle le plus récent pour une vidéo
   FoundClub face caméra ; clips-bourbier\ pour des clips verticaux tirés d'un épisode). Tu pars de ses outils et de ses
   gabarits, dans un NOUVEAU dossier ; tu ne modifies pas les dossiers des autres vidéos.

COMMENT TU TRAVAILLES :
- Je pilote, je ne relis pas le code. Parle-moi en écrans et en secondes de la vidéo (« à 0:12, le sticker arrive »),
  jamais en chemins de fichiers.
- Tu t'arrêtes à chaque validation : 1) l'inventaire des rushs (chaque prise transcrite, comparée au script, la
  meilleure prise par phrase), 2) le découpage (ce qui s'affiche, seconde par seconde), 3) un aperçu court avant le
  rendu entier, 4) la vidéo finie. Jamais un long rendu sans aperçu avant.
- Style : pas d'intro en motion ; stickers façon story (fond blanc, texte noir, penchés, sans icône ni halo) ; peu de
  sons, des bruits réels (week-end-gache\outils\sons.py), rien sur les titres ; jamais d'étiquette posée sur l'écran de
  l'appli ; rien qui fasse « IA » (pas de faux logos, visages, maillots) ; aucun spoil de score sur les clips de match.
- Noms propres : jamais sous-titrer un nom non vérifié sans me le signaler.
- Tu finis sur une preuve, pas sur « c'est fait » : décodage complet (ffmpeg -v error -i x.mp4 -f null -), son mesuré
  APRÈS encodage (-14 LUFS, crête sous -1 dBFS, chaîne de limiteur du §4), planche d'images. Ce que tu n'as pas pu
  vérifier, tu l'écris en tête : « NON VÉRIFIÉ : <quoi> — commande qui le prouverait : <cmd> ».
- Git : les rushs et les fichiers de plus de 100 Mo ne vont jamais dans le dépôt (.gitignore avant le premier add).
  Commit par chemins explicites (git commit -m "…" -- chemin1 chemin2), message en français, puis push.

QUAND J'AI VALIDÉ LA VIDÉO :
1. Coche-la dans le suivi des 20 scripts : sa ligne dans scripts-foundclub\suivi.json passe à "fait" (date, détail,
   chemin du rendu), puis `python scripts-foundclub\outils\suivi.py`.
2. Range-la dans la prochaine case FoundClub vide du calendrier (FOUNDCLUB dans publications\calendrier.py), puis
   `python publications\calendrier.py` et `node publications\pdf.mjs publications\CALENDRIER.html publications\CALENDRIER.pdf`.
3. Ajoute une section à README.md (ce que montre la vidéo, ses fichiers, comment la refaire), et dans METHODE_MONTAGE.md
   tout nouveau piège ou toute règle de style que je t'ai donnée.
4. Commit et push de tout ça.

À CHAQUE MESSAGE DE FOND, termine par « ⚖️ CE QUE TU DOIS DÉCIDER » : numéroté, avec ta recommandation, les options
et le format de réponse (`1- A 2- ok`). S'il n'y a rien à décider, écris-le. Ne me pose que les vraies questions
(contenu, goût, droits, argent) : le technique réversible et vérifiable, tu le tranches et tu me le rapportes.
```
