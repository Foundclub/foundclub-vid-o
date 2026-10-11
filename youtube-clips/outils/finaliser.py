"""Relie le rapport aux vérifications des fichiers réellement livrés."""
import hashlib
import json
from pathlib import Path
from transcrire import stamp,write

root=Path(__file__).resolve().parents[1]
clips=json.loads((root/'extraits.json').read_text(encoding='utf-8'))
rows=[]
stale=[]
for c in clips:
    details={}
    issues=[]
    sizes={}
    for kind in ('horizontal','vertical'):
        path=root/kind/f"clip-{c['numero']:02}{'-9x16' if kind=='vertical' else ''}.mp4"
        v=json.loads((root/'diagnostic'/f"verification-{c['numero']:02}-{kind}.json").read_text(encoding='utf-8'))
        sha=hashlib.sha256(path.read_bytes()).hexdigest()
        planned=hashlib.sha256(c['texte_complet'].encode('utf-8')).hexdigest()
        if sha!=v['sha256'] or planned!=v['texte_prevu_sha256']:
            stale.append((c['numero'],kind))
        sizes[kind]=path.stat().st_size
        if sizes[kind]>=100_000_000: raise RuntimeError(f'Fichier trop volumineux : {path}')
        if v['verification']!='OK':issues.append(f"{kind} : {v['verification']}")
        details[kind]={k:v[k] for k in ['verification','decodage_integral','debut_correspond','fin_correspond','lufs','pic_vrai_db','duree','taille_octets','sha256']}
        details[kind]['modele']=v.get('modele_verification','turbo')
        rows.append({'numero':c['numero'],'format':kind,**details[kind]})
    c['tailles_octets']=sizes
    c['verification']='OK' if not issues else '; '.join(issues)
    c['verification_details']=details
    crop=json.loads((root/'diagnostic'/f"recadrage-{c['numero']:02}.json").read_text(encoding='utf-8'))
    c['recadrage']=crop['mode']
    c['raison_recadrage']=crop['raison']
if stale:
    print('Vérifications à actualiser :',stale)
    raise SystemExit(2)
write(root/'extraits.json',clips)

# Régénération des trois sorties textuelles à partir du JSON mot à mot corrigé.
out=root/'transcription'
words=json.loads((out/'transcription-mots.json').read_text(encoding='utf-8'))
segments,group=[],[]
for w in words:
    if group and (w['debut']-group[-1]['fin']>1.2 or w['fin']-group[0]['debut']>10):
        segments.append({'debut':group[0]['debut'],'fin':group[-1]['fin'],'texte':''.join(x['mot'] for x in group).strip(),'mots':group})
        group=[]
    group.append(w)
if group:segments.append({'debut':group[0]['debut'],'fin':group[-1]['fin'],'texte':''.join(x['mot'] for x in group).strip(),'mots':group})
write(out/'transcription-segments.json',segments)
(out/'transcription.srt').write_text('\n'.join(f"{i}\n{stamp(s['debut'])} --> {stamp(s['fin'])}\n{s['texte']}\n" for i,s in enumerate(segments,1)),encoding='utf-8')
(out/'transcription.txt').write_text('\n'.join(f"[{s['debut']:.2f}–{s['fin']:.2f}] {s['texte']}" for s in segments)+'\n',encoding='utf-8')
write(out/'transcription-consolidee-mesures.json',{'mots':len(words),'segments':len(segments),'source_duree':1566.975420,
    'modele_integral':'large-v3-turbo, CPU int8, français, horodatage par mot',
    'relectures':'large-v3-turbo puis large-v3 sur les dialogues et vestiaires difficiles',
    'horodatages_manuels':'Temps de l’expression initiale conservés et répartis lors des corrections ; alignement estimé',
    'limite':'Plusieurs phrases secondaires restent incertaines ; ne pas utiliser le SRT comme sous-titrage final sans écoute'})

write(root/'diagnostic/controle-final.json',{'fichiers':rows,'nombre':len(rows),'limite_taille_octets':100_000_000,
    'source_sha256':hashlib.sha256((root/'source/ach10-source.mp4').read_bytes()).hexdigest(),
    'source_originale_camera':False})
write(root/'diagnostic/controle-visuel.json',{'planches_source_relues':13,'intervalle_source_secondes':5,
    'planches_horizontal_relues':18,'planches_vertical_relues':18,'images_par_extrait':8,
    'constats':['Cadre entier conservé dans les discussions, vestiaires, photos et inserts',
        'Suivi du visage lissé dans les clips 04 et 06 ; sous-titres source coupés sur les côtés',
        'Scènes nocturnes 07–09 sombres et caméra mobile dans la source',
        'Animations d’abonnement déjà présentes dans la source conservées dans 01 et 13'],
    'limite':'Relecture par images échantillonnées ; pas une vision humaine continue de toutes les images'})

def tc(t):
    m,s=divmod(t,60)
    return f'{int(m):02}:{s:06.3f}'

def cell(s):return s.replace('|','/').replace('\n',' ')

all_lufs=[r['lufs'] for r in rows]
max_size=max(r['taille_octets'] for r in rows)
good=sum(c['verification']=='OK' for c in clips)
short=sum(c['duree']>=20 for c in clips)
corrections=json.loads((out/'corrections.json').read_text(encoding='utf-8'))
silences=json.loads((root/'diagnostic/silences.json').read_text(encoding='utf-8'))
report=[
"NON VÉRIFIÉ : fidélité mot à mot de plusieurs phrases secondaires dans les échanges nocturnes et le vestiaire — commande de relecture : `ffplay -autoexit youtube-clips/horizontal/clip-07.mp4` (à répéter pour 08–12 et 14–18, avec contrôle à l’écoute).",
"",
"NON VÉRIFIÉ : droits de réutilisation, accord des personnes visibles, droits sur les musiques éventuelles et statut commercial des marques — aucune commande ne prouve ces autorisations ; il faut les documents du détenteur des droits.",
"",
"NON VÉRIFIÉ : explication de la réforme des divisions dans le clip 02 et certains noms de joueurs — pas de confirmation indépendante. Les propos sont ceux de la vidéo.",
"",
"# Achh10 — sélection et découpes",
"",
f"Livraison du 12 octobre 2026 : **{len(clips)} extraits**, dont **{short} de 20 à 60 secondes et un micro-extrait de 14,90 secondes**. Chaque extrait existe en horizontal et en brouillon vertical, soit 36 MP4. Aucun titre, bruitage, musique ou motion design ajouté. Les sous-titres, inserts et animations déjà incrustés dans la vidéo restent présents.",
"",
"## Source et méthode",
"",
"Vidéo : [#41 Des DEBUTS en N2 TRÈS COMPLIQUÉ ! AchhLife Saison 3 épisode 3](https://www.youtube.com/watch?v=8T0INMoppoY), chaîne Achh10. Téléchargement effectué après l’autorisation explicite « si telecharge ». Il s’agit de la version YouTube recompressée, pas de l’original caméra.",
"",
"| Élément | Résultat ffprobe |",
"|---|---|",
"| Durée | 1 566,975 s — 26 min 06,975 s |",
"| Image | 1 920 × 1 080, 16:9, H.264, 30 images/s |",
"| Couleur | SDR, 8 bits, yuv420p, BT.709 ; aucune métadonnée HDR détectée |",
"| Audio | Une piste AAC, stéréo, 44 100 Hz, environ 128 kbit/s |",
"| Taille source | 534 150 612 octets — conservée uniquement sur ce PC |",
"",
f"Transcription intégrale avec faster-whisper large-v3-turbo, français, CPU int8 et temps par mot ; relectures ciblées avec large-v3 pour les passages difficiles. Aucun recours au modèle medium. La version consolidée contient {len(words)} mots. Les estimations temporelles corrigées manuellement sont signalées dans le JSON. Le SRT reste une base de travail, surtout dans les passages avec des voix superposées.",
"",
"Toute la vidéo a été parcourue par 13 planches, une image toutes les 5 secondes. Les 18 planches horizontales et les 18 planches verticales de 8 images ont été relues. Le récapitulatif initial, les longs passages de jeu et les montages musicaux ont été écartés de la sélection parlée.",
"",
"Les silences ont été repérés avec `silencedetect=noise=-32dB:d=0.12` ; les coupes visent environ 0,15 s autour de la parole. Certaines répliques se suivent sans silence exploitable : les limites suivent alors la phrase, avec un fondu audio de 30 ms. Les temps par mot sont des estimations ; les écarts de reconnaissance aux limites sont indiqués, pas masqués.",
"",
"## Classement",
"",
"La note évalue l’intérêt éditorial, pas les droits de publication. Pour tous les extraits : droits vidéo, accord des tiers, musique éventuelle et statut commercial des marques non confirmés. Les risques particuliers sont indiqués dans le tableau ; le JSON contient le détail.",
"",
"| N° | Début–fin source | Durée | Titre proposé | Accroche transcrite des 3 premières secondes | Note /10 | Risque particulier | Vérification H / V |",
"|---|---|---:|---|---|---:|---|---|",
]
unchecked=[f"{c['numero']:02}" for c in clips if c['verification']!='OK']
if unchecked:
    report[0:0]=["NON VÉRIFIÉ : correspondance automatique exacte des mots aux limites pour les clips "+', '.join(unchecked)+" — commande de relecture : `ffplay -autoexit youtube-clips/horizontal/clip-NN.mp4` ; remplacer NN par le numéro concerné, écouter le début et la fin. Les fichiers sont décodables intégralement ; les écarts ASR restent signalés.",""]
for c in sorted(clips,key=lambda x:-x['note_sur_10']):
    risks=[r for r in c['risques'] if not r.startswith(('Autorisation des personnes','Droits sur la musique'))]
    risk=' ; '.join(risks) or 'Pas de risque particulier repéré'
    def short_status(s):
        if s=='OK':return 'OK'
        labels=[]
        if 'Premiers mots' in s:labels.append('début ASR')
        if 'Derniers mots' in s:labels.append('fin ASR')
        if any(x in s for x in ['décodage','Durée','Résolution','Codec','Taille','Niveau']):labels.append('problème technique')
        return 'À relire : '+', '.join(labels)
    statuses=' / '.join(short_status(c['verification_details'][k]['verification']) for k in ('horizontal','vertical'))
    report.append(f"| {c['numero']:02} | {tc(c['debut'])}–{tc(c['fin'])} | {c['duree']:.2f} s | {cell(c['titre_propose'])} | {cell(c['accroche'])} | {c['note_sur_10']:.1f} | {cell(risk)} | {cell(statuses)} |")
report += [
"",
"Le clip 03 garde une entrée progressive (« Pour commencer ») : une ouverture sur « la réserve du MHSC » vers 205,47 s serait plus directe, avec moins de respiration avant la phrase. Le 04 est volontairement un micro-extrait : la version longue diluait l’annonce et renvoyait au résumé du match. Le 11 commence sur l’instinct après suppression de l’introduction. Les clips 11 et 12 partagent 3,66 s : éviter de les publier ensemble dans une compilation.",
"",
"## Brouillons verticaux",
"",
"Les clips 04 et 06 suivent le visage à partir d’une détection MediaPipe à 4 images/s, avec médiane sur 5 échantillons, amortissement et interpolation continue. Les 16 autres gardent l’image entière centrée sur un fond flou : plusieurs interlocuteurs, vestiaire, tableau, logos, photos ou images de match.",
"",
"Sur 04 et 06, le visage reste dans le cadre mais les sous-titres déjà incrustés sont coupés sur les côtés. Utiliser les horizontaux comme base pour refaire les sous-titres et l’habillage. Les scènes 07–09 restent sombres ; le mouvement de caméra vient de la source. Les 01 et 13 conservent une animation d’abonnement YouTube de la source.",
"",
"## Vérification des fichiers livrés",
"",
f"Les 36 fichiers ont été retranscrits séparément et décodés jusqu’au bout avec `ffmpeg -v error -i fichier -f null -`. **{good}/{len(clips)} extraits ont leurs deux formats marqués OK** pour la comparaison des quatre premiers et quatre derniers mots, le décodage, la durée, la résolution, les codecs et la taille. Les éventuels problèmes restants figurent dans le tableau et dans `diagnostic/verification-NN-format.json`.",
"",
f"Audio : loudnorm en deux passes à −14 LUFS, fondus de 30 ms, AAC à débit cible 192 kbit/s. Le gain a été affiné après mesure du fichier AAC quand nécessaire. Niveau final mesuré : **{min(all_lufs):.2f} à {max(all_lufs):.2f} LUFS**. Les niveaux et pics vrais figurent dans `diagnostic/controle-final.json`.",
"",
f"Image : H.264 CRF 18, horizontal 1920×1080, vertical 1080×1920, 30 images/s. **Plus gros MP4 : {max_size/1e6:.2f} Mo** ; tous sont strictement sous 100 000 000 octets. Aucun débit vidéo n’a dû être abaissé pour passer la limite.",
"",
"La comparaison ignore la ponctuation, les accents et la variation orthographique « important/importants », qui a le même son. En cas d’écart, les 8 premières et dernières secondes ont aussi été retranscrites. Les résultats bruts restent disponibles. Un OK technique aux limites ne certifie pas chaque mot du milieu de la transcription ni une écoute humaine continue.",
"",
"Les pistes 03, 05, 06 et 16 ont été renormalisées en deux passes depuis la source avec une marge de −6 dBTP avant l’AAC, puis ajustées à −14 LUFS. Cette marge absorbe les pics créés par l’encodage et la conversion. Les images ont été copiées sans réencodage. Les pics vrais mesurés des fichiers finaux sont tous sous 0 dBTP.",
"",
"Les passages difficiles ont aussi été reconnus sans suppression des silences, avec un vocabulaire de contexte et un silence ajouté uniquement à l’entrée du moteur de transcription. Cette aide ne modifie pas les MP4. Sur 07, la fin est placée dans le silence mesuré 635,407–635,688 s : le texte des derniers mots reste à confirmer si l’ASR ne les restitue pas. Sur 12, les modèles confondent notamment l’instinct et le nom Atlas malgré les sous-titres source ; l’écart reste indiqué.",
"",
"## Trois idées de compilation",
"",
"Idées seulement : aucun montage de compilation rendu. Les temps ci-dessous sont les secondes exactes de la source, dans l’ordre proposé. Les jonctions devront être écoutées au moment de l’assemblage.",
"",
"1. **Défaite, lucidité, réaction** — 374,22–380,33 ; 396,39–407,85 ; 1282,88–1285,19 ; 1312,73–1316,20. Environ 23,35 s. Le renversement de 2–0 à 3–2, la leçon de la défaite, puis l’appel à courir. Les deux dernières pièces viennent du clip 18 et montrent un autre moment du match : présenter cette suite comme un thème, sans fabriquer une chronologie.",
"2. **Les obligations d’un joueur** — 746,83–754,87 ; 761,35–764,09 ; 770,05–776,62 ; 1166,27–1171,27 ; 1312,73–1316,20. Environ 25,82 s. Responsabilités, contre-pressing, engagement, gestes de remobilisation et courses. Quelques mots intermédiaires restent à confirmer avant de poser de nouveaux sous-titres.",
"3. **Le prix d’un petit doigt** — 605,00–607,90 ; 619,55–625,07 ; 639,70–647,83 ; 700,75–718,65. Environ 34,45 s. La proposition, l’inutilité supposée du doigt, Marrakech et la chute à quatre cent mille. Débat hypothétique et langage familier ; les gestes et réactions doivent rester visibles. Revoir les jonctions des deux dernières répliques à l’écoute.",
"",
"## Les cinq premiers à publier",
"",
"Après confirmation des droits de réutilisation : **18 → 10 → 05 → 13 → 01**. Le 18 porte l’émotion, le 10 un conseil concret, le 05 le renversement de score, le 13 la pression de l’entraîneur, puis le 01 une réussite collective. Le 13 et le 01 gardent l’animation d’abonnement de la source : à traiter lors de la session d’habillage.",
"",
"## Corrections consignées",
"",
"Les corrections ci-dessous s’appuient sur les sous-titres, logos et tableaux visibles dans la vidéo. Elles corrigent une transcription ; elles ne vérifient pas les affirmations sportives. « Sussargue » reprend l’orthographe incrustée dans la source. Les expressions remplacées gardent un intervalle temporel estimé.",
"",
"| Temps source | Avant | Après | Appui |",
"|---|---|---|---|",
]
for c in corrections:report.append(f"| {tc(c['debut'])} | {cell(c['avant'])} | {cell(c['apres'])} | {cell(c['preuve'])} |")
report += [
"",
"Les faux mots « Sous-titrage ST’501 » produits par la reconnaissance ont été supprimés. Aucun « FoundClub » ou « Ergysport » intelligible n’a été repéré dans la transcription ; ces exemples du brief n’ont pas été ajoutés artificiellement.",
"",
"## Fichiers et reproduction",
"",
"- `horizontal/clip-NN.mp4` : 18 coupes au format source.",
"- `vertical/clip-NN-9x16.mp4` : 18 brouillons 9:16.",
"- `planches/clip-NN.jpg` : 18 planches de 8 images, avec 18 planches verticales supplémentaires.",
"- `planches/source/` : repérage de toute la vidéo à 5 secondes d’intervalle.",
"- `transcription/transcription.srt`, `transcription-mots.json`, `transcription.txt`, `corrections.json` : transcription et corrections.",
"- `extraits.json` : sélection, textes, risques, recadrage, vérification et tailles.",
"- `diagnostic/` : silences, détection des visages, mesures sonores et retranscriptions des exports.",
"- `source/provenance.json`, `source/ffprobe.json` : identification de la source.",
"",
"La source de 534 Mo, les modèles, l’environnement local et les fichiers de travail sont exclus de Git par `youtube-clips/.gitignore`. Ils restent sur ce PC. Le dépôt reçoit les coupes et les livrables ; les autres dossiers de vidéos ne sont pas modifiés.",
"",
"Pour relancer sur ce PC depuis la racine du dépôt :",
"",
"```powershell",
"ffprobe -v error -show_format -show_streams -of json youtube-clips/source/ach10-source.mp4",
"& .\\youtube-clips\\.cache\\venv\\Scripts\\python.exe youtube-clips/outils/exporter.py",
"& .\\youtube-clips\\.cache\\venv\\Scripts\\python.exe youtube-clips/outils/limiter-pics.py",
"& .\\youtube-clips\\.cache\\venv\\Scripts\\python.exe youtube-clips/outils/ajuster-son.py",
"& .\\youtube-clips\\.cache\\venv\\Scripts\\python.exe youtube-clips/outils/verifier.py",
"& .\\youtube-clips\\.cache\\venv\\Scripts\\python.exe youtube-clips/outils/finaliser.py",
"```",
"",
"## CE QUE JE N’AI PAS PU TRANCHER",
"",
"- Plusieurs paroles secondaires de 07–12 et 14–18 restent difficiles à distinguer, malgré les deux modèles et la relecture des sous-titres d’origine. Il faut une écoute humaine avant d’en faire des citations ou des sous-titres définitifs.",
"- L’orthographe des surnoms ou prénoms Napsou, Nassim/Souley et Naïf/Naït n’est pas suffisamment établie. Ils ne servent pas d’accroches.",
"- L’orthographe administrative du lieu transcrit « Sussargue », les explications de qualification et la réforme des divisions ne sont pas confirmées indépendamment.",
"- Les autorisations de réutilisation et de droit à l’image ainsi que les licences de musique éventuelle ne sont pas connues. La présence d’un logo ne prouve pas un partenariat rémunéré. Si un passage relève effectivement d’une collaboration commerciale, prévoir la mention « Collaboration commerciale » lors de l’habillage.",
"- Les sous-titres incrustés dans 04 et 06 ne peuvent pas être récupérés proprement par le recadrage sur le visage ; les versions horizontales sont conservées pour la prochaine session.",
"",
]
(root/'RAPPORT.md').write_text('\n'.join(report),encoding='utf-8')
print(f'Rapport final : {len(clips)} extraits, {good} OK, {len(rows)} fichiers, maximum {max_size/1e6:.2f} Mo')
