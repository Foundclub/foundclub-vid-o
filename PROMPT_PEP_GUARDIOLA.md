# Prompt à coller dans une session locale — vidéo FoundClub 02/20 « Les Pep Guardiola du dimanche »

Réglage : Opus · effort `high` · sans ultracode. Ouvrir la session dans `D:\App\video\foundclub-vid-o` après `git pull`.

```
Tu vas monter une vidéo FoundClub verticale (1080×1920) avec Achraf (ach10, ambassadeur FoundClub) face caméra :
la vidéo 02/20 de notre bibliothèque de scripts, « Les Pep Guardiola du dimanche ». C'est le même genre de vidéo que
celles déjà faites dans ce dépôt : la voix et le visage d'Achraf, l'habillage FoundClub en motion par-dessus, l'appli
dans un téléphone animé, un carton final. Tu travailles en local sur mon PC (Windows, PowerShell, RTX 3070 Ti).

AVANT TOUT GESTE, lis en entier :
1. D:\App\video\foundclub-vid-o\METHODE_MONTAGE.md — comment je travaille, les outils, le style, les pièges déjà payés.
2. D:\App\video\foundclub-vid-o\README.md — en particulier les sections matchs-amicaux-2 (ach10 face caméra : cartes
   de presse, calendrier, téléphone avec l'appli, « Envoie-la à ton coach », carton final) et matchs-amicaux-4 (le plus
   récent : pastilles, logo, appli en motion). Ce sont tes deux modèles : tu pars de leurs gabarits et de leurs outils
   (assembler.py, calage.json par caler_mots.py, sons.py avec GAIN_SONS réglé sur la voix, rendre.sh, preparer-video.sh),
   dans un nouveau dossier pep-guardiola\. Tu ne modifies pas les dossiers des autres vidéos.

LES RUSHS : D:\Foundclub média\ACh\Les Pep Guardiola du dimanche\ (ce qu'Achraf a tourné, sans doute plusieurs prises).
Ils ne vont pas dans git (100 Mo maximum par fichier sur GitHub) : seuls les outils, le calage, les gabarits et les
rendus de moins de 100 Mo entrent dans le dépôt. Commit par chemins explicites, message en français.

LE SCRIPT (durée visée 1 min 25 – 1 min 40, cible : les joueurs, qui partagent à leur coach) :
« Les gars, faut vraiment qu'on parle d'un truc dans le foot amateur. Les coachs qui se prennent pour Pep Guardiola, là.
Déjà, ils t'envoient les convocations le samedi à 23 h alors que tu joues dimanche. Frérot, on a une vie ! On a un
travail, une famille, des trucs à prévoir le week-end ! Et toi t'attends ton petit message WhatsApp pour savoir si tu
peux organiser ta vie ou pas.
Et encore, quand t'es convoqué, t'es content… mais tu sais même pas où tu vas jouer ! Parce que monsieur garde sa
composition secrète jusqu'à dix minutes avant le match ! Un dimanche t'es numéro 9, le dimanche d'après t'es arrière
gauche, et la semaine suivante t'es défenseur central ! Mais frérot, tu crois qu'on est tous Camavinga ou quoi ?!
Bon, les coachs, on vous aime hein… mais faut qu'on arrête ça. Regardez ce que vous pouvez faire sur FoundClub. Tu
ajoutes ton match, tu sélectionnes tes joueurs, tu les glisses directement à leur poste sur le terrain et tu prépares
ta composition. Tu peux envoyer tes convocations à l'avance, voir qui est présent, qui est absent, et adapter ton équipe
si quelqu'un se désiste. Et en plus, si t'as pas de match ce week-end, tu peux directement trouver un match amical sur
l'application.
Alors coach, garde tes tactiques de Guardiola, mais arrête de nous organiser le week-end à la dernière minute ! Et les
joueurs, envoyez ça à votre coach. Vous savez très bien de qui je parle. »

CE QUE TU FAIS, DANS CET ORDRE, ET TU T'ARRÊTES À CHAQUE VALIDATION :
0. Vérifie l'outillage (ffmpeg avec h264_nvenc, faster-whisper sur CUDA, Node et npx hyperframes, un Chrome pour le
   rendu) et dis-moi ce qui manque. N'installe rien sans me le dire.
1. L'INVENTAIRE DES RUSHS : chaque fichier (durée, format, son), transcrit mot à mot, comparé au script phrase par
   phrase. Pour chaque phrase, la meilleure prise (diction, énergie, cadre, pas de faute), et ce qui manque ou est raté.
   S'il y a un enregistrement d'écran de l'appli dans le dossier, dis-moi ce qu'il montre. Sinon, dis-moi exactement
   quels écrans il faut que je filme : la composition (glisser un joueur à son poste sur le terrain), l'envoi des
   convocations, la liste présents / absents, la recherche d'un match amical.
2. LE DÉCOUPAGE : la vidéo en temps, phrase par phrase, avec ce qui s'affiche à l'écran. Mes idées de départ, à
   améliorer :
   - l'accroche « Les Pep Guardiola du dimanche » en gros titre dès la première phrase ;
   - « le samedi à 23 h » : une notification de message qui tombe à 23:04 (une bulle de discussion générique, pas une
     copie de l'interface WhatsApp ni de son logo) ;
   - « un travail, une famille, des trucs à prévoir » : trois pastilles qui tombent ;
   - « numéro 9, arrière gauche, défenseur central » : un petit terrain où le même joueur change de poste à chaque mot ;
     « Camavinga » en mot-choc ;
   - « Regardez ce que vous pouvez faire sur FoundClub » : Achraf s'efface, le téléphone avec l'appli prend l'écran,
     une étiquette par fonction (composition, convocations, présents / absents, match amical), appuis animés ;
   - « envoyez ça à votre coach » : la pastille « Envoie-la à ton coach », puis le carton final FoundClub
     (Télécharge FoundClub, badges App Store et Google Play, foundclub.app).
   Rien qui fasse « IA » : pas de faux logos, pas de visages inventés. Pas de photo de Guardiola ni de Camavinga sans
   que j'aie validé les droits : du texte et de la typographie à la place.
   → Je valide le découpage avant que tu montes.
3. LE MONTAGE de la voix d'Achraf (les coupes entre prises, sans couper un mot : réécoute chaque coupe), puis
   l'habillage. Montre-moi d'abord un aperçu court (les 15 premières secondes), puis la vidéo entière.
4. LA FINITION : sous-titres corrigés à la main (typographie française, insécables), bruitages réglés sur la voix,
   son à -14 LUFS avec la chaîne de limiteur du §4 de METHODE_MONTAGE.md, rendu vérifié : décodage complet, mesure du
   son après encodage, planche d'images.

Je pilote et je ne relis pas le code : parle-moi en écrans et en secondes de la vidéo, pas en fichiers. À chaque
message de fond, termine par « ⚖️ CE QUE TU DOIS DÉCIDER » (numéroté, avec ta recommandation et le format de réponse).
Avant un long rendu, montre-moi d'abord un aperçu court.
Quand j'ai validé la vidéo, coche-la dans le suivi des 20 scripts (METHODE_MONTAGE.md §7 : la ligne "02" de
scripts-foundclub\suivi.json passe à "fait" avec le chemin du rendu, puis tu refais le PDF de suivi et tu le commites).
```
