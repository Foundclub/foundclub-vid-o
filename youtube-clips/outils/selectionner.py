"""Sélection éditoriale manuelle, reliée aux mots de la transcription."""
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
words = json.loads((root / "transcription/transcription-mots.json").read_text(encoding="utf-8"))
specs = [
 (1,137.45,159.80,"Premier match officiel et premier trophée","Réussite collective",8.1,"Une réussite immédiate puis une gratitude envers ceux qui ont rendu la montée possible.",True,"Photos de groupe et inserts dans la source",[]),
 (2,165.34,193.66,"La poule la plus dure","Ambition et niveau",8.2,"Une opinion forte sur la poule, puis une chute personnelle sur la proximité du football professionnel.",True,"Tableau des divisions à préserver",["Présentation des divisions et de leur réforme : exactitude sportive non vérifiée"]),
 (3,203.20,229.83,"La réserve du MHSC","Adversaires professionnels",6.8,"Trois réserves professionnelles connues rendent le niveau du championnat concret.",True,"Photos, logos et inserts à préserver",["Accroche progressive ; ouvre par Pour commencer"]),
 (4,308.74,323.64,"Je ne vais pas pouvoir jouer","Coulisses administratives",7.9,"Une absence au premier match expliquée par une date de contrat et de qualification, sans le renvoi au résumé.",False,"",["Micro-extrait de 14,90 s, en complément des 17 extraits de 20 à 60 s"]),
 (5,374.22,407.85,"Chaque erreur compte","Défaite et lucidité",8.9,"L'équipe mène deux à zéro et perd trois à deux : renversement clair, émotion et leçon.",True,"Insertion d'images du match à garder entière",[]),
 (6,410.33,442.70,"Pas encore aux normes","Coulisses du club",8.0,"Un match à domicile déplacé parce que le terrain n'est pas aux normes, puis un objectif concret.",False,"",[]),
 (7,605.00,635.56,"200 patates mon frère","Humour entre joueurs",8.4,"Un débat absurde sur le prix d'un doigt, conclu sur deux cents patates ; amorce et réponse finale brouillées retirées.",True,"Plusieurs interlocuteurs et caméra mobile",["Débat hypothétique sur la perte d'un doigt", "Gros mot : putain", "Paroles familières et certaines réponses difficiles à distinguer"]),
 (8,639.70,673.60,"Tu fais quoi avec 200000","Humour et argent",7.8,"Une question concrète sur l'argent mène à Marrakech puis à l'utilité du petit doigt.",True,"Plusieurs interlocuteurs et caméra mobile",["Contexte du débat hypothétique sur la perte d'un doigt", "Voix et rires superposés"]),
 (9,675.15,718.65,"Presque un demi-million","Humour et chute",8.3,"Une démonstration des doigts utiles au quotidien se termine sur le calcul de quatre cent mille euros.",True,"Plusieurs interlocuteurs et caméra mobile",["Débat hypothétique sur la perte d'un doigt", "Référence au débat précédent : comprendre la proposition nécessite le contexte visuel"]),
 (10,746.83,776.62,"C'est une obligation","Tactique et responsabilités",9.0,"Un conseil directement réutilisable : attaquer, défendre et contre-presser concernent tout le monde.",True,"Vestiaire avec entraîneur et joueurs",["Quelques mots du milieu du discours restent incertains"]),
 (11,779.81,809.14,"L'instinct et l'intuition","Confiance et instinct",8.0,"Un appel à faire confiance à l'instinct, conclu par la formule sur la tête et le cœur ; introduction molle retirée.",True,"Plusieurs personnes dans le vestiaire",["Plusieurs formulations du milieu du discours sont peu intelligibles"]),
 (12,805.48,828.15,"C'est le cœur","Identité du club",8.8,"La tête et le cœur opposés, puis un rappel de l'identité et de l'engagement du club.",True,"Plusieurs personnes dans le vestiaire",["Chevauchement de 3,66 s avec le clip 11 : choisir l'un des deux dans une même compilation", "Quelques réponses et noms de joueurs restent incertains"]),
 (13,1139.83,1165.48,"Je vous laisse 10 minutes","Pression à la mi-temps",8.9,"Un entraîneur fixe un délai très concret avant de changer l'équipe, tout en rappelant le temps restant.",True,"Entraîneur, staff et joueurs visibles",[]),
 (14,1166.27,1191.78,"Faites-vous violence","Remobilisation",8.7,"Des mots, des regards et de petits gestes pour remettre de l'énergie dans une équipe menée.",True,"Plusieurs membres du vestiaire visibles",["Gros mot final : putain", "Une formulation à la fin reste incertaine"]),
 (15,1192.68,1218.23,"On est trop gentil","Agressivité et duels",7.7,"Un joueur réclame des duels et de l'impact ; la répétition rend la frustration immédiate.",True,"Plusieurs membres du vestiaire visibles",["Gros mot : couilles", "Propos : mettez des coups, rentrez-leur dedans, cassez le jeu ; risque d'être perçu comme une promotion des fautes", "Quelques formulations peu intelligibles"]),
 (16,1218.40,1244.33,"On va les faire trembler","Renverser un match",8.8,"Le groupe se fixe un objectif simple : gagner la seconde mi-temps et marquer rapidement.",True,"Plusieurs membres du vestiaire visibles",["Références aux occasions déjà vécues dans le match", "Quelques formulations peu intelligibles"]),
 (17,1249.38,1278.22,"C'est fini les discours","Efforts et deuxième ballon",8.5,"Des reproches précis sur les deuxièmes ballons et les efforts débouchent sur l'idée de passer à l'action.",True,"Plusieurs membres du vestiaire visibles",["Gros mot : couilles"]),
 (18,1282.88,1316.20,"Est-ce que vous y croyez","Foi et réaction collective",9.3,"Marquer pour changer le match, demander si le groupe y croit, puis appeler à faire les courses : une montée émotionnelle complète.",True,"Plusieurs membres du vestiaire visibles",["Quelques formulations secondaires restent difficiles à distinguer"]),
]
clips = []
previous = json.loads((root / "extraits.json").read_text(encoding="utf-8"))
last_words = {1:"championnat",2:"gars",3:"aussi",4:"jouer",5:"rousset",6:"importants",
              7:"frère",8:"doigt",9:"ça",10:"physique",11:"cœur",12:"allez",13:"minutes",
              14:"putain",15:"oui",16:"gars",17:"efforts",18:"enfants"}
for n,s,e,title,theme,score,why,blur,reason,risks in specs:
    ww = [w for w in words if s-.25 <= w["debut"] < e]
    if n == 3:
        first = next(i for i,w in enumerate(ww) if w["mot"].strip().lower()=="pour")
        ww = ww[first:]
    if n in last_words:
        matches = [i for i,w in enumerate(ww) if w["mot"].strip().lower().strip(".,!?")==last_words[n]]
        if matches: ww=ww[:matches[-1]+1]
    text = "".join(w["mot"] for w in ww).strip()
    hook = "".join(w["mot"] for w in ww if w["fin"] <= s+3).strip()
    c = {"numero":n,"debut":s,"fin":e,"duree":round(e-s,3),"titre_propose":title,
         "accroche":hook,"theme":theme,"pourquoi_ca_marche":why,"note_sur_10":score,
         "texte_complet":text,"risques":risks,"fond_flou_impose":blur,"raison_fond_flou":reason,
         "recadrage":"fond flou" if blur else "visage","verification":"À effectuer"}
    c["type"]="micro-extrait" if e-s<20 else "extrait court"
    if n in (1,13):
        c["risques"].append("Animation d'abonnement YouTube déjà incrustée dans la source et conservée")
    if n in (4,6):
        c["risques"].append("Le recadrage sur le visage coupe une partie des sous-titres déjà incrustés dans la source ; utiliser l'horizontal pour refaire l'habillage")
    c["risques"].append("Autorisation des personnes visibles et droits de réutilisation de la vidéo non confirmés")
    c["risques"].append("Droits sur la musique éventuelle et statut commercial des marques visibles non confirmés")
    for old in previous:
        if old["numero"]==n:
            for key in ["tailles_octets","debit_reduit","raison_recadrage","duree_calcul"]:
                if key in old: c[key]=old[key]
    clips.append(c)
(root / "extraits.json").write_text(json.dumps(clips,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(f"{len(clips)} extraits sélectionnés")
