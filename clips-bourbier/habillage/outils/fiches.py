"""Écrit clips/NN.json (les 21 clips) : accroche, format, cadrage, coupes de plan, phrases sous-titrées.
Les phrases viennent de la transcription par clip (Whisper), corrigées à la main : noms propres, et dans les causeries du coach
on ne garde que les phrases reconnues avec certitude (le reste est couvert par la musique et l'écho).
Une phrase écrite « a | b » est coupée en deux sous-titres, le temps partagé au nombre de lettres.
Usage : python3 -I outils/fiches.py   (depuis clips-bourbier/habillage/)"""
import json, os

COMMUN = {"emission": "AchhLife · S3 · Ép. 4", "chaine": "Achh10", "titre_episode": "Match bourbier contre cette R3 !",
          "duree_episode": "22:39", "emission_longue": "AchhLife · Saison 3 · Épisode 4", "partie": None}
COUPES = {  # changements de plan détectés (ffmpeg, scene > 0,32), utiles au cadrage et aux bruitages
 1: [1.5, 3.93, 6.1, 8.87, 11.9, 15.97, 21.3, 23.33, 26.3, 28.33, 30.2, 31.9, 33.17, 34.83, 35.9, 37.37, 38.87, 43.1, 47.9, 49.9],
 2: [2.97, 12.57], 3: [3.6, 8.17, 10.0, 23.43, 27.2, 30.6, 32.1, 35.07, 37.93], 4: [3.83, 6.23, 8.1, 10.17, 13.27, 15.63, 24.97, 26.87, 31.77, 34.67, 36.8, 39.63, 47.37],
 5: [1.33, 2.73, 4.57, 5.77, 6.57, 9.87, 11.13, 13.73, 15.4, 21.97], 6: [13.0, 16.93], 7: [9.83, 20.13, 25.0, 37.47],
 8: [2.87, 10.5, 15.87, 17.57, 22.17, 35.77, 45.37, 50.63], 9: [14.37, 14.5, 33.5], 10: [19.9, 23.97, 28.27], 11: [5.93, 10.5],
 12: [2.4, 4.43, 7.33, 12.47, 15.3, 19.5, 27.6], 13: [47.13], 14: [14.6, 17.17, 28.33, 36.1, 45.13], 15: [], 16: [17.87], 17: [],
 18: [30.17], 19: [9.6, 15.6], 20: [2.87, 10.5, 15.87, 17.57], 21: [2.03, 3.77, 5.37, 27.8],
}
CADRAGE = {  # [t, centre_x] : là où se tient celui qui parle (lu sur des planches à 1 image/s, règle tous les 240 px)
 7: [[0, 750], [1, 750], [2, 560], [3, 560], [4, 600], [6, 780], [8, 850], [9.5, 880], [10, 900], [11, 930], [12, 1080], [13, 1170],
     [15, 1170], [17, 1150], [19, 1080], [20.5, 1200], [24, 1200], [25.3, 780], [27, 780], [29, 690], [30, 660], [31, 620],
     [32.5, 1080], [35, 1100], [37, 1100], [37.6, 900]],
 8: [[0, 960], [2.5, 960], [3, 780], [5, 780], [6, 1030], [8, 1000], [9, 900], [10, 960], [11, 300], [13, 300], [14, 1100],
     [15.5, 1020], [16.2, 500], [17.3, 500], [18, 960], [20, 1080], [22, 1050], [22.5, 810], [24, 1000], [26, 950], [27, 780],
     [28, 870], [29, 840], [30, 1080], [31, 1230], [32, 1200], [33, 990], [34, 900], [35.5, 930], [36, 900], [41, 950], [42, 400],
     [44, 450], [45.5, 900], [46, 990], [47, 930], [48, 990], [50, 990], [51, 700], [53, 650], [54, 400], [55.5, 450]],
 10: [[0, 1200], [1, 1200], [2, 1320], [3, 1410], [4, 1380], [5, 1350], [6, 1050], [7, 1050], [8, 990], [9, 1020], [10, 870],
      [11, 810], [12, 630], [13, 1080], [14, 1170], [15, 1170], [16, 1230], [17, 1290], [18, 1230], [19.5, 990], [20, 900],
      [23.5, 900], [24.2, 630], [26, 630], [27, 1020], [28, 1000], [28.4, 810], [29.4, 810]],
}
CADRAGE[20] = [p for p in CADRAGE[8] if p[0] <= 21]
FICHES = {
 1: ("La Coupe de France", "c'est pas qu'un match", [
   (0.2, 1.39, "Parce que la Coupe de France,"), (1.51, 3.69, "ce n'est pas simplement | une compétition de football."),
   (4.04, 4.91, "C'est une histoire,"), (5.16, 6.06, "une tradition,"), (6.28, 6.9, "un rêve."),
   (7.08, 9.13, "C'est cette compétition où, | le temps d'un match,"), (9.35, 10.92, "les différences de niveau s'effacent."),
   (11.17, 13.55, "Où les amateurs | peuvent défier les professionnels."), (13.89, 15.82, "Où des joueurs | qui travaillent toute la semaine"),
   (16.04, 18.12, "peuvent se retrouver | le temps de 90 minutes"), (18.44, 20.91, "face à ceux qu'ils ont l'habitude | de regarder à la télévision."),
   (21.35, 23.08, "C'est l'excitation du tirage au sort,"), (23.46, 26.09, "quand tout un vestiaire attend | de connaître son prochain adversaire,"),
   (26.37, 28.39, "avec cette même question | qui revient chaque année :"), (28.77, 30.06, "« Et si on tirait un gros ? »"),
   (30.31, 31.82, "C'est l'espoir de vivre une épopée,"), (32.01, 34.6, "de représenter son club, | sa ville, son quartier,"),
   (35.01, 36.49, "de voir ses proches dans les tribunes,"), (36.81, 38.79, "de jouer devant | des milliers de spectateurs"),
   (38.98, 40.27, "et de vivre des émotions"), (40.55, 42.44, "qu'on n'aurait peut-être | jamais imaginées."),
   (42.92, 44.14, "Mais la Coupe de France,"), (44.36, 45.9, "c'est aussi son lot de désillusions,"),
   (46.31, 47.79, "des rêves qui s'arrêtent brutalement,"), (48.07, 49.83, "des éliminations difficiles à digérer."),
   (50.09, 53.42, "Et c'est justement ce qui rend | cette compétition aussi particulière."), (53.57, 54.57, "Parce qu'en Coupe de France,"),
   (54.92, 55.72, "tout peut arriver.")]),
 2: ("Face à la Ligue 1", "le match de ma vie", [
   (0.07, 2.89, "Et croyez-moi, des émotions, | cette compétition m'en a fait vivre."),
   (3.14, 8.12, "Je me souviens notamment | de la saison 2016-2017. | À l'époque, je portais | les couleurs de Louhans-Cuiseaux."),
   (8.49, 12.32, "On réalise un beau parcours | qui nous emmène | jusqu'en 32e de finale,"),
   (12.55, 15.43, "face à la Ligue 1 de Dijon. | Un match particulier pour moi,"),
   (15.78, 18.09, "parce que ce jour-là, | face à des professionnels,"), (18.41, 21.67, "je réalise certainement | l'une des meilleures prestations | de ma carrière."),
   (21.8, 23.75, "Lees-Melou, Marvin Martin,"), (25.09, 25.87, "Balmont,"), (26.25, 27.24, "plein d'autres encore."),
   (27.62, 29.19, "Tous ces joueurs | que je voyais à la télé,"), (29.41, 30.44, "ils étaient en face de moi."),
   (30.73, 32.23, "Ce sont des rencontres | comme celle-là"), (32.61, 36.16, "qui te rappellent | pourquoi tu joues au football | depuis tout petit.")]),
 3: ("Éliminé en 32e…", "et eux tirent l'OL", [
   (0.2, 1.29, "Quelques années plus tard,"), (1.45, 3.5, "lors de la saison 2022-2023,"),
   (3.69, 10.84, "vous avez tous suivi notre parcours | avec le Jura Sud Foot | et une élimination au 7e tour | face à la National 2 de Haguenau."),
   (10.98, 12.49, "L'année d'après, en 2023-2024,"), (12.74, 14.99, "je retrouve une nouvelle fois | les 32es de finale."),
   (15.24, 17.19, "Cette fois-ci avec le FC Les Bournes,"), (17.38, 20.39, "face à Bergerac, | équipe de notre poule en National 2."),
   (20.55, 23.34, "Un autre club, un autre maillot, | une autre aventure,"), (23.59, 26.99, "mais toujours cette même excitation, | cette même envie | d'aller encore plus loin."),
   (27.11, 29.32, "Malheureusement, | une défaite 2 buts à 1,"), (29.67, 31.05, "ce qui m'a fait très, très mal."),
   (31.24, 34.22, "Car le tour d'après, | Bergerac a eu la chance de tirer…"), (35.24, 36.27, "l'Olympique Lyonnais,"),
   (36.49, 38.51, "l'équipe que je supporte | depuis tout petit."), (38.66, 39.91, "Ils ont failli faire l'exploit."),
   (40.2, 42.09, "Mais bon… on est quand même | l'Olympique Lyonnais.")]),
 4: ("10 000 personnes", "à la Mosson", [
   (0.13, 1.55, "Et puis plus récemment,"), (1.67, 3.85, "lors de la saison 2025-2026,"), (4.07, 6.06, "j'ai eu la chance | de vivre une nouvelle aventure"),
   (6.34, 7.82, "avec Montpellier Atlas Paillade."), (8.17, 10.03, "Un club de quartier, une équipe,"),
   (10.25, 13.23, "une famille, qui s'est retrouvée | au 7e tour de la Coupe de France"), (13.45, 15.47, "face à Bourg-en-Bresse, | une équipe de National."),
   (15.75, 18.12, "Mais ce qui rendait cette rencontre | encore plus particulière,"), (18.31, 20.55, "c'était le lieu : | le stade de la Mosson."),
   (20.77, 23.05, "Ce stade où on passe | tous les jours devant"), (23.21, 24.91, "pour aller à l'entraînement | ou aller à nos matchs."),
   (25.06, 26.79, "Mais cette fois-ci, on était dedans."),
   (27.05, 32.99, "Près de 10 000 personnes | dans les tribunes. | Pour beaucoup d'entre nous, | c'était un rêve de gosse | qui devenait réalité."),
   (33.0, 34.6, "Quand tu sors du tunnel, | que tu découvres les tribunes,"), (34.79, 36.65, "que tu entends | les supporters chanter"),
   (36.9, 39.47, "et que tu réalises que tout ce monde | est venu pour ton équipe,"), (39.94, 41.99, "ce sont des sensations | difficiles à expliquer."),
   (42.37, 45.19, "Ce jour-là, le résultat | n'a pas été celui qu'on espérait."), (45.51, 47.98, "Mais les souvenirs, eux, | resteront gravés à jamais.")]),
 5: ("En Coupe de France", "on a le droit de rêver", [
   (0.2, 2.63, "Et c'est ça finalement | la magie de la Coupe de France."), (2.92, 6.51, "Ce ne sont pas uniquement | les victoires, les qualifications | ou les exploits."),
   (6.82, 8.78, "Ce sont les histoires | qu'elle nous permet d'écrire,"), (9.06, 10.99, "les émotions | qu'elle nous fait traverser"),
   (11.3, 13.55, "et les souvenirs qu'elle nous laisse | pour toute une vie."), (13.8, 16.39, "Et chaque année, | quand cette compétition revient,"),
   (16.81, 17.8, "c'est toujours la même chose."), (18.09, 19.11, "On se remet à rêver."), (19.33, 21.87, "Parce qu'au fond, | peu importe le niveau auquel on joue,"),
   (22.21, 24.96, "tant qu'on est en Coupe de France, | on a toujours le droit de rêver.")]),
 6: ("La Coupe de France", "expliquée en 30 s", [
   (0.13, 6.2, "La Coupe de France a déjà commencé | avec l'entrée des clubs de district | au premier tour, | puis des clubs régionaux au deuxième."),
   (6.31, 11.0, "De notre côté, étant en National 2, | on fait notre entrée | directement au 3e tour."),
   (11.0, 16.76, "Pour ce match, on est tombé | face à la R3 de Saint-Orens, | club qui se situe | juste à côté de Toulouse."),
   (17.0, 20.41, "Ensuite, pour le 4e tour, | ce sera au tour des National 1 d'entrer."), (20.58, 22.67, "Au 5e tour, aux Ligue 3 d'entrer,"),
   (23.08, 26.35, "puis directement les Ligue 2 | au 7e tour,"), (26.57, 29.31, "et enfin les Ligue 1, | seulement en 32e de finale.")]),
 7: ("Le discours d'avant-match", "« J'agresse ! »", [
   (0.2, 0.81, "Allez !"), (4.17, 7.21, "Zéro but, aucune erreur."), (7.43, 10.06, "Concentration, | c'est ça qu'on travaille aujourd'hui."),
   (10.31, 11.6, "Personne passif, les gars !"), (13.93, 17.47, "Non, non, non ! | Je suis proche du duel, | je saute, je combats !"),
   (18.79, 20.01, "J'agresse !"), (33.25, 36.2, "Aujourd'hui, | c'est un match comme ça.")]),
 8: ("0-0 à la mi-temps", "sur un champ de patate", [
   (2.98, 5.99, "Ça va passer. | Pas de panique, pas de panique."), (8.23, 9.4, "Toujours en équipe !"), (14.63, 17.48, "On retourne chez eux. | Derrière, 0-0."),
   (21.0, 24.54, "Allez, au combat ! | Aucun relâchement derrière !"), (25.0, 28.5, "Avec l'état du terrain, | pas de risque !"),
   (40.5, 43.13, "Tout de suite, on reste | et on agresse ! Allez !"), (45.0, 48.6, "Du monde dans la surface !"), (48.68, 52.22, "Allez, allez, allez !")]),
 9: ("N2 contre R3", "les 3 buts du match", [(7.0, 9.5, "BUT ! 1-0"), (20.5, 23.0, "BUT ! 2-0"), (43.0, 45.5, "BUT ! 3-0")]),
 10: ("Le président a tranché", "« Un champ de patate ! »", [
   (1.06, 7.16, "On a fait un match sérieux | sur une pelouse un peu difficile."), (7.62, 9.0, "Un champ de patate !"),
   (9.0, 10.6, "Mais bon, voilà, | ils ont été sérieux."), (10.6, 13.92, "On a raté beaucoup en première mi-temps, | mais en deuxième mi-temps, | ils étaient sérieux."),
   (14.28, 15.24, "3-0 !"), (15.69, 19.23, "L'aventure continue, les amis, | l'aventure continue, allez !"), (21.3, 23.9, "C'est parti, c'est parti !")]),
 11: ("Victoire 3-0", "direction le 4e tour", [
   (0.2, 3.08, "Pour notre part, | victoire assez facile, 3 buts à 0."), (3.24, 5.71, "Direction le 4e tour | de la Coupe de France."),
   (6.02, 7.31, "Et la semaine prochaine,"), (7.49, 10.41, "gros derby | face à la réserve du MHSC."), (10.73, 12.39, "Après deux défaites en championnat,"),
   (12.58, 14.22, "victoire obligatoire pour nous."), (14.6, 16.1, "À suivre au prochain épisode.")]),
 12: ("Unique. Magique.", "La Coupe de France", [
   (0.13, 1.2, "Unique."), (2.53, 3.5, "Magique."), (4.45, 5.9, "Exceptionnelle."), (7.49, 8.46, "Émouvante."), (10.05, 10.99, "Vibrante."),
   (12.52, 13.83, "Bouleversante."), (16.39, 17.5, "Grandiose."), (19.69, 22.47, "Voilà quelques mots | qui pourraient définir | la Coupe de France."),
   (22.6, 26.28, "Mais en réalité, je crois | qu'aucun mot ne suffit à décrire"), (26.47, 28.68, "ce que cette compétition | peut nous faire ressentir.")]),
 13: ("Veille de match", "l'entraînement du vendredi", []),
 14: ("Coupe de France", "l'entrée des joueurs", []),
 15: ("Vu du drone", "un vrai champ de patate", []),
 16: ("Le premier but", "Atlas Paillade ouvre", [(11.0, 13.5, "BUT ! 1-0")]),
 17: ("Le deuxième but", "et de deux !", [(9.5, 12.0, "BUT ! 2-0")]),
 18: ("Le but du 3-0", "le match est plié", [(12.5, 15.0, "BUT ! 3-0")]),
 19: ("Coup de sifflet final", "qualifiés pour le 4e tour !", [(15.6, 18.0, "Qualifiés !")]),
 20: ("0-0 à la pause", "« Pas de panique ! »", None),
 21: ("Dans le prochain épisode", "le derby face au MHSC", [(8.58, 10.3, "On l'attendait depuis longtemps."), (13.13, 14.8, "Il faut tout donner !")]),
}
FORMAT = {n: ("carre" if n in CADRAGE else "large") for n in FICHES}
def couper(phrases):
    out = []
    for d, f, t in phrases:
        morceaux = [m.strip() for m in t.split("|")]
        total = sum(len(m) for m in morceaux); x = d
        for m in morceaux:
            y = round(x + (f - d) * len(m) / total, 2); out.append([round(x, 2), y, m]); x = y
    return out
os.makedirs("clips", exist_ok=True)
for n, (l1, l2, phrases) in FICHES.items():
    if phrases is None:  # le 20 : le début du 08
        phrases = [p for p in FICHES[8][2] if p[1] <= 20.6]
    c = {"numero": n, "source": f"../horizontal/clip-{n:02d}.mp4", **COMMUN, "titre": [l1, l2], "format": FORMAT[n],
         "coupes": COUPES[n], "phrases": couper(phrases)}
    if n in CADRAGE: c["cadrage"] = CADRAGE[n]
    if n == 10: c["cote"] = 860   # le bandeau « BEN ALI Mahfoud, Président » (y > 880) reste dehors
    json.dump(c, open(f"clips/{n:02d}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    longues = [p[2] for p in c["phrases"] if len(p[2]) > 44]
    print(f"{n:02d} {c['format']:5} {len(c['phrases']):2d} sous-titres" + (f"  TROP LONGS : {longues}" if longues else ""))
