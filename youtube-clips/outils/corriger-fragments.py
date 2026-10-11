"""Préserve les mots voisins dans les intervalles remplacés manuellement."""
import json
from pathlib import Path

p=Path(__file__).resolve().parents[1]/'transcription'
words=json.loads((p/'transcription-mots.json').read_text(encoding='utf-8'))
corrections=json.loads((p/'corrections.json').read_text(encoding='utf-8'))
restored=[
 (131.24,131.52, [(' CAN',131.24,131.44),(' qu',131.44,131.52)]),
 (207.15,208.03, [(' MHSC',207.15,207.69),(' qui',207.69,208.03)]),
 (226.55,228.33, [(' l’AS',226.55,227.09),(' Saint-Étienne',227.09,227.91),(' qui',227.91,228.33)]),
 (244.34,245.16, [(' Cannet-Rocheville',244.34,245.16)]),
 (276.54,277.52, [("'US",276.54,276.74),(' Mandelieu',276.74,277.24),(' Donc',277.24,277.52)]),
 (315.31,315.55, [(' cette',315.31,315.55)]),
 (645.48,645.92, [(' une',645.48,645.64),(' dar',645.64,645.76),(' à',645.76,645.92)]),
 (793.64,794.16, [(' encore',793.64,793.70),(' les',793.70,793.86),(' noms',793.86,793.96),(' derrière,',793.96,794.16)]),
 (1142.12,1142.46,[(' pas',1142.12,1142.28),(' dedans,',1142.28,1142.46)]),
 (1276.52,1277.38,[(' en',1276.52,1276.60),(' marchant,',1276.60,1277.00),(' on',1277.00,1277.38)]),
 (1309.56,1310.30,[(' demander',1309.56,1309.82),(' des',1309.82,1309.88),(' efforts',1309.88,1310.18),(' les',1310.18,1310.30)]),
]
for a,b,tokens in restored:
    words=[w for w in words if not a<=w['debut']<b]
    words.extend({'mot':t,'debut':s,'fin':e,'probabilite':None,'correction_manuelle':True,'horodatage_estime':True} for t,s,e in tokens)
words.sort(key=lambda w:(w['debut'],w['fin']))
for w in words:
    if w['debut']==243.08:w['mot']="'US"
# Le journal décrit la correction définitive, avec les mots conservés.
after={131.24:'CAN qu',207.15:'MHSC qui',226.55:'l’AS Saint-Étienne qui',
       244.34:'Cannet-Rocheville',276.54:'US Mandelieu Donc',645.48:'une dar à',
       793.64:'encore les noms derrière,',1142.12:'pas dedans,',1276.52:'en marchant, on',
       1309.56:'demander des efforts les'}
corrections=[c for c in corrections if c['debut']!=315.31]
for c in corrections:
    if c['debut'] in after:c['apres']=after[c['debut']]
for filename,data in [('transcription-mots.json',words),('corrections.json',corrections)]:
    (p/filename).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'{len(words)} mots avec les fragments voisins restaurés')
