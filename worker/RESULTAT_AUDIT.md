# Audit MVP 0.2 — verdict BLOQUÉ

## Cible et intégrité

- Dépôt : `noobstrade/sentinelles-content-factory`, branche `develop`.
- Commit audité : `4dbbbd0517259f3771023551889b2238b0aeca06`.
- Arbre de base : `51d87108160ba39d7911452c44167369a6880fa3`.
- Blob exact de `app/app.py` exécuté : `7c73193877304783c0dde33073829b08fd54b4a5` (7 755 octets ; empreinte Git recalculée avant/après les essais).
- Lecture intégrale préalable de `worker/A_AUDITER.md`, `docs/PRODUCT_SPEC.md`, `docs/AUDIT_BASELINE.md`, `docs/WORKFLOW.md`, puis de tous les fichiers de `app/`. Les quatre documents ont été revérifiés au SHA audité. Aucun `AGENTS.md` ni test préexistant dans l'arbre complet de ce commit.
- Aucun fichier de l'application modifié sur GitHub. Seul ce rapport doit être committé. Les fixtures, scripts et exports d'audit sont hors application.

## Environnement et méthode

Audit du 7 octobre 2026, UTC. Linux 6.18.44, Python 3.12.14, Tk 9.0, FFmpeg/ffprobe 7.1.5 Debian ; encodeurs libx264/AAC et filtres drawtext/crop réellement utilisés. Aucun abonnement ou service IA utilisé.

Le clone Git a échoué (`Failed to connect to proxy port 8080`). Les fichiers ont été obtenus via le connecteur GitHub au commit immuable ci-dessus. L'empreinte Git du fichier testé correspond exactement à celle du dépôt.

Pas de serveur graphique ni Xvfb : `tkinter.Tk()` renvoie `TclError: no display name and no $DISPLAY environment variable`. Les essais exécutent les méthodes originales `duration`, `build_candidates`, `select_candidates`, `new_run_dir`, `process`, avec uniquement les variables/widgets et boîtes de dialogue remplacés par des doubles de test. FFmpeg, ffprobe, les fichiers et le système de fichiers sont réels. Les tests ne valident donc pas les interactions GUI ni le comportement de Tk depuis le thread de production. Aucun correctif apporté ou déclaré.

Fixtures synthétiques MP4 H.264 + AAC, couleurs distinctes, 2 images/s, afin de rendre les tests rapides et déterministes. Ce choix valide les propriétés techniques contrôlées, pas la qualité sur un événement hockey réel. Scripts complets reproductibles en annexe. Sorties JSON détaillées et médias conservés localement dans `/workspace/audit-evidence-exact` et `/workspace/audit-evidence-extra` pendant cette session ; ces chemins ne sont pas des artefacts persistants GitHub.

## Tests et résultats

| Test | Entrée / contrôle | Résultat constaté |
| --- | --- | --- |
| T01 | 3 rushs de 60 s, rouge/vert/bleu ; traitement réel | 3 exports vidéo 1080×1920 + audio de 18 s ; sources distinctes, starts 6/6/6 s ; 3 sources inventoriées. |
| T02 | 4 rushs exploitables de 60 s | 4 sources inventoriées, 3 exports des 3 premières sources. La quatrième alimente le pool mais n'est pas exportée dans cette génération limitée à 3. |
| T03 | 1 rush de 60 s | 3 exports, starts 6/21/36 s ; écart 15 s, donc >= 12 s. Les clips de 18 s se chevauchent encore de 3 s : conforme au seuil de la mission, pas une déduplication de contenu. |
| T04 | 2 rushs de 60 s | Starts source1=6, source2=6, source1=21 ; aucun écart < 12 s pour un même chemin source. |
| T05 | Deux générations successives du même événement | Deux dossiers `run_*`, six exports ; SHA-256 de tous les fichiers de la première génération inchangés. |
| T06 | Rushs de 0,5 / 1 / 2 / 10 s | Respectivement 0 / 1 / 1 / 1 export ; JSON présent dans les quatre cas, sources inventoriées. 0,5 s est ignoré par le seuil de 1 s mais annoncé comme succès à zéro Short (MIN-01). |
| T07 | Nom vide, `../../hors/dossier`, `Été 🏒 / CON:*?`, `..` | Générations réussies ; slugs `evenement`, `hors_dossier`, `t_CON`, `evenement`. Aucun chemin sortant du dossier d'export. |
| T07 long | Nom `a` répété 300 fois | `OSError(36, 'File name too long')` non interceptée ; progression laissée active, aucun rapport (MAJ-03). |
| T08 | Portrait 90×160, 2 s (9:16) | Un export 1080×1920 + audio réussi. |
| T09 | Portrait 80×160, 2 s (1:2) | Échec FFmpeg sur crop trop large ; aucun rapport (MAJ-02, MAJ-04). |
| T10 | Rush valide, fichier MP4 corrompu, autre rush valide | Échec ffprobe au second fichier ; aucun export, aucun JSON et troisième rush non analysé (MAJ-04). |
| T11/T16 | Même fichier importé sous son chemin et un lien symbolique | Sélection du même intervalle sous deux chemins ; deux MP4 strictement identiques en T16 (MAJ-05). |
| T12 | Dossier de sortie devenu un fichier | `NotADirectoryError` non interceptée, progression active (MAJ-03). |
| T13 | 66 429 combinaisons : 1 à 5 sources, durées 0,5/1/2/10/18/24/48/60/120 s | Zéro violation du seuil temporel de 12 s, des bornes temporelles et de la diversité des 3 premières sources quand >=3 durées >=1 s ; chemins distincts. Test du sélecteur, pas 66 429 encodages vidéo. |
| T14 | Horloge figée à la même microseconde pour deux créations | `FileExistsError`, fichier sentinelle préservé : aucun écrasement ; collision non récupérée, progression active. Injection explicite, aucune fréquence naturelle de collision mesurée (MAJ-03). |
| T15 | Rush valide puis portrait étroit, suivi d'un rush valide | Premier MP4 valide de 36 859 octets, second fichier de 0 octet ; aucun JSON malgré l'export existant (MAJ-04). |
| T17 | Vidéo de 2 s et audio de 60 s dans le même MP4 | Succès annoncé : 3 Shorts ; starts 6/21/36 s ; les 3 exports de 18 s ne contiennent qu'une piste audio (MAJ-01). |

Contrôle supplémentaire réel : les 37 MP4 issus des rapports de la suite principale ont tous été décodés intégralement par `ffmpeg -v error -i EXPORT -f null -` : code 0 et stderr vide pour chacun. Pour T01, échantillonnage RGB de la zone hors bandeau via `crop=1080:1500:0:400,scale=1:1` : rouge `[255,0,0]`, vert `[1,128,1]`, bleu `[3,0,255]`, correspondant aux trois rushs. Cela vérifie aussi le contenu source, au-delà des chemins JSON. Ce contrôle ne concerne pas les sorties volontairement défectueuses de la suite supplémentaire.

Les rapports des générations réussies comportent `schema_version`, événement, partenaires, dossier, inventaire des sources avec durées, candidats sélectionnés et exports avec `source`, `start`, `duration`. Ces champs ont été confrontés aux entrées et à ffprobe. La liste `candidates` contient uniquement les candidats retenus, pas le pool complet. La traçabilité fonctionne sur le chemin nominal ; elle n'est pas garantie en cas d'erreur.

## CRITIQUES

Aucun défaut critique de destruction/écrasement de générations antérieures reproduit. Cela ne constitue pas une preuve universelle d'absence de défaut critique. Le blocage ci-dessous repose sur les défauts majeurs reproduits.

## MAJEURS

### MAJ-01 — Faux succès : fichiers « Shorts » sans vidéo

Localisation : `app/app.py:52-54`, `:69-70`, `:114-125`.

Reproduction T17 : générer une piste vidéo couleur de 2 s et une piste audio de 60 s sans `-shortest`, puis importer ce MP4 et lancer le traitement. `ffprobe format=duration` mesure 60 s. Le sélecteur choisit les starts 6, 21 et 36 s, après la fin des images. FFmpeg sort avec code 0 ; l'application annonce « Terminé : 3 Shorts prêts à valider » et écrit trois entrées d'exports. `ffprobe -show_entries stream=codec_type,width,height:format=duration -of json` sur chacun des exports donne uniquement `codec_type: audio`, durée `18.000000`, sans flux vidéo ni dimensions.

Impact : résultats inutilisables présentés comme réussis ; la seule durée du conteneur ne suffit pas à garantir une portion vidéo exploitable. Condition de levée : sélectionner sur la durée vidéo réelle et vérifier la présence/dimensions/durée des images de sortie ; rejouer T17 et un cas audio absent, puis contrôler les sorties.

### MAJ-02 — Une vidéo verticale valide plus étroite que 9:16 bloque l'export

Localisation : `app/app.py:113-116`.

Reproduction T09 : importer le MP4 H.264/AAC 80×160 de 2 s. `scale=-2:1920` produit une largeur de 960, puis `crop=1080:1920` demande une zone plus large que l'image. Exécution originale : état « Erreur », aucun rapport. Réexécution indépendante du filtre avec stderr conservé : `Invalid too big or non positive size for width '1080' or height '1920'`, code non nul. Le portrait 90×160 (T08) passe, ce qui délimite le défaut.

Impact : rush importable et décodable rejeté par le pipeline. Condition de levée : stratégie scale/crop/pad adaptée aux ratios avec preuve d'export vidéo valide pour 1:2, 9:16 et paysage.

### MAJ-03 — Création du dossier hors du bloc de gestion d'erreur

Localisation : `app/app.py:89-102`, `:128-129`.

Reproductions T07-long, T12, T14 : nom de 300 caractères ; destination devenue un fichier ; ou horloge injectée constante provoquant une collision. `new_run_dir()` est appelée avant `try`. Respectivement `OSError`, `NotADirectoryError`, `FileExistsError` sortent de `process()`, sans boîte d'erreur ni passage dans `finally`. Le double de progression conserve `running=True` et le statut « Analyse en cours... ». Dans le thread réel, cela constitue une exception non gérée ; le rendu GUI n'a pas été exercé.

Impact : traitement interrompu et état de progression non rétabli pour une saisie atypique légitime ou une erreur de destination. Collision protégée contre l'écrasement mais non récupérée. Condition de levée : noms bornés, création englobée dans la gestion d'erreur, état restauré, stratégie de collision sûre ; rejouer les trois cas. La fixture de collision ne prouve pas une collision fréquente en production.

### MAJ-04 — Rapport absent en cas d'erreur, même après un export réussi

Localisation : `app/app.py:103-105`, `:116-127`.

Reproduction T10 : placer un fichier contenant `invalid video` entre deux rushs valides. L'analyse s'arrête au deuxième fichier : aucun inventaire final ni diagnostic par rush. Reproduction T15 : valide 2 s, étroit 1:2 2 s, valide 2 s. Le premier export existe et se décode ; l'échec du deuxième laisse un MP4 de zéro octet. `rapport.json` et `publication_proposee.txt` sont absents, car leur écriture intervient seulement après toute la boucle.

Impact : un fichier inutilisable empêche le traitement des autres ; surtout, un export existant peut perdre toute traçabilité persistante. Non-conformité à l'exigence d'inventaire de tous les rushs et de traçabilité de chaque sortie. Condition de levée : inventaire avec erreurs par source, rapport durable même pour une exécution partielle, identification des sorties échouées et aucune sortie invalide présentée comme prête ; rejouer T10/T15.

### MAJ-05 — Déduplication contournée par des chemins différents vers le même rush

Localisation : `app/app.py:39-40`, `:79-80`.

Reproduction T16 : importer `valid.mp4` et `alias.mp4`, lien symbolique vers le même fichier. Les deux chaînes de chemin diffèrent et sont retenues ; starts 0/0 s et durées 2/2 s. L'application annonce 2 Shorts. SHA-256 des deux MP4 : `6e6a70eac31f0b4ecddb52859f6840c61130114272152e6250ad82e4b1ca018a` pour chacun. T11 reproduit aussi des doublons avec un rush de 60 s.

Impact : réapparition de clips identiques si une même source est importée via plusieurs chemins. Le sélecteur passe tous les tests pour des chemins réellement distincts (T13), mais compare seulement des chaînes, pas l'identité du fichier. Condition de levée : normalisation/identité de source puis test alias ; la détection de copies de contenu sous d'autres fichiers demanderait une stratégie supplémentaire, non testée ici.

## MINEURS

### MIN-01 — Zéro résultat présenté comme une génération terminée

Localisation : `app/app.py:71`, `:124-125`. T06 à 0,5 s : aucune exception, source inventoriée, zéro candidat/export, message « 0 Shorts générés » et statut « 0 Shorts prêts à valider ». L'exclusion respecte le seuil de 1 s du code mais sa raison n'est pas explicitée à l'utilisateur. Une sortie nulle devrait être identifiée comme sans segment exploitable. Les vidéos de 1/2/10 s produisent bien un seul Short, sans duplication forcée pour atteindre 3.

## Limites et fonctions absentes

- Non présents : sous-titres/transcription, scoring hockey intelligent, sélection multimodale, Sponsor Manager, reporting partenaire. La présence de `faster-whisper`/`scenedetect` dans `requirements.txt` ne prouve pas leur intégration : aucun appel dans `app.py`. Le champ partenaires alimente du texte et le JSON, pas un moteur de règles ou un reporting.
- La sélection utilise seulement 25/50/75 % de la durée ; aucun découpage en scènes ni analyse audio. Recadrage central fixe et bandeau fixe ; aucun suivi intelligent ni Brand Kit paramétrable. Ces limites sont annoncées dans README/ROADMAP et ne sont pas assimilées à des fonctionnalités corrigées.
- Le rappel de validation humaine est présent et aucune publication automatique n'existe. Il n'y a pas de workflow persistant d'approbation testé.
- Comportement de Tk dans le thread, clics simultanés, modification des champs/imports pendant traitement, Windows/macOS (dont noms réservés), codecs variés, vidéos tournées via métadonnées et événement pilote réel : non validés. Le code lance un thread sans verrou et manipule Tk depuis ce thread ; risque relevé statiquement, non classé comme panne reproduite.
- Pas de preuve de qualité hockey, de performance à cadence réelle, de temps bénévole économisé ni d'efficacité commerciale. Ces affirmations restent « à mesurer ».

## Verdict et suite

**BLOQUÉ**. Les trois défauts historiques (premier rush seul, trois clips temporellement identiques sur chemins distincts, écrasement entre générations successives) ne se reproduisent pas sur les cas nominaux testés. Leurs protections sont démontrées dans ce périmètre, sans valider toutes les entrées. Les cinq défauts majeurs ci-dessus restent présents et reproduits. Aucun défaut n'est déclaré corrigé par cet audit.

Corriger d'abord MAJ-01 et la traçabilité des exécutions partielles, puis les ratios, erreurs de dossier et alias. Exiger les relectures ffprobe/décodage et rejouer l'ensemble des régressions avant nouvel audit. Ne pas promouvoir ce commit vers `main` comme version validée.

## Annexe — reproduction autonome

Les scripts ci-dessous restent dans ce rapport afin de ne modifier aucun fichier applicatif. Copier le `app/app.py` du commit audité dans `/workspace/audit-source/app.py`, enregistrer le premier script en `audit.py` et le second en `extra.py` dans ce dossier. Utiliser des dossiers d'évidence vides : relancer sans nettoyer crée de nouveaux runs et modifie les comptages. Exécuter `python /workspace/audit-source/audit.py`, puis `python /workspace/audit-source/extra.py`. Ils invoquent le code original sans modifier sa logique. Les fixtures sont créées avec FFmpeg, les résultats sont sauvegardés en JSON. Une autre machine peut adapter uniquement les chemins `/workspace/...`.

### audit.py

```python
import importlib.util, json, subprocess, hashlib, itertools, traceback
from pathlib import Path
from types import SimpleNamespace
from datetime import datetime
spec=importlib.util.spec_from_file_location('mvp','/workspace/audit-source/app.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
root=Path('/workspace/audit-evidence-exact'); root.mkdir(exist_ok=True)
class Var:
    def __init__(self,v): self.v=v
    def get(self): return self.v
    def set(self,v): self.v=v
class Progress:
    def __init__(self): self.running=False
    def start(self,*a): self.running=True
    def stop(self): self.running=False
messages=[]
m.messagebox=SimpleNamespace(showinfo=lambda *a:messages.append(['info',*a]),showerror=lambda *a:messages.append(['error',*a]))
def app(files,event='Test',output=None):
    a=object.__new__(m.App); a.files=list(map(str,files)); a.output=output or root/'exports'; a.event=Var(event); a.sponsor=Var('Partenaire'); a.status=Var('Prêt'); a.progress=Progress(); return a
def media(name,duration,size='320x180',color='red'):
    p=root/name
    subprocess.run(['ffmpeg','-y','-v','error','-f','lavfi','-i',f'color=c={color}:s={size}:r=2:d={duration}','-f','lavfi','-i',f'sine=frequency=440:duration={duration}','-c:v','libx264','-pix_fmt','yuv420p','-c:a','aac','-shortest',str(p)],check=True)
    return p
def probe(p): return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','stream=codec_type,width,height:format=duration','-of','json',str(p)],text=True))
results=[]
def run(label,a):
    before=len(messages); exception=None
    try: a.process()
    except Exception as e: exception=repr(e)
    reports=list(a.output.rglob('rapport.json')) if a.output.is_dir() else []
    result={'test':label,'status':a.status.get(),'messages':messages[before:],'exception':exception,'progress_running':a.progress.running,'reports':[]}
    for p in reports:
        r=json.loads(p.read_text()); result['reports'].append({'path':str(p),'report':r,'media':[probe(e['file']) for e in r['exports']]})
    results.append(result); print(json.dumps(result,ensure_ascii=False),flush=True); return result
rushes=[media(f'rush_{i}.mp4',60,color=c) for i,c in enumerate(['red','green','blue','yellow'],1)]
run('T01_three_sources',app(rushes[:3],output=root/'T01'))
run('T02_four_sources',app(rushes,output=root/'T02'))
run('T03_one_source',app(rushes[:1],output=root/'T03'))
run('T04_two_sources',app(rushes[:2],output=root/'T04'))
a=app(rushes[:3],event='Même événement',output=root/'T05'); run('T05_first_run',a)
old={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in a.output.rglob('*') if p.is_file()}
run('T05_second_run',a)
results.append({'test':'T05_hashes','unchanged':all(Path(p).exists() and hashlib.sha256(Path(p).read_bytes()).hexdigest()==v for p,v in old.items()),'runs':len(list(a.output.rglob('run_*')))})
for d in [.5,1,2,10]: run(f'T06_short_{d}',app([media(f'short_{d}.mp4',d)],output=root/f'T06_{d}'))
for i,event in enumerate(['','../../hors/dossier','Été 🏒 / CON:*?','..','a'*300]): run(f'T07_event_{i}',app(rushes[:1],event=event,output=root/f'T07_{i}'))
portrait=media('portrait.mp4',2,size='90x160'); run('T08_portrait_9x16',app([portrait],output=root/'T08'))
narrow=media('portrait_narrow.mp4',2,size='80x160'); run('T09_portrait_narrow',app([narrow],output=root/'T09'))
bad=root/'invalid.mp4'; bad.write_text('invalid video'); run('T10_corrupt_middle',app([rushes[0],bad,rushes[1]],output=root/'T10'))
alias=root/'alias.mp4'; alias.symlink_to(rushes[0]); run('T11_same_source_alias',app([rushes[0],alias],output=root/'T11'))
out=root/'not_directory'; out.write_text('sentinel'); run('T12_invalid_output',app(rushes[:1],output=out))
checks=0; violations=[]
for n in range(1,6):
    for ds in itertools.product([.5,1,2,10,18,24,48,60,120],repeat=n):
        sources=[{'file':str(i),'duration':d} for i,d in enumerate(ds)]
        sel=m.App.select_candidates(m.App.build_candidates(sources)); checks+=1
        if any(a['file']==b['file'] and abs(a['start']-b['start'])<12 for a,b in itertools.combinations(sel,2)): violations.append(ds)
        usable=sum(d>=1 for d in ds)
        if usable>=3 and len({c['file'] for c in sel[:3]})!=3: violations.append(ds)
        if any(c['start']<0 or c['duration']<1 or c['start']+c['duration']>ds[int(c['file'])]+1e-9 for c in sel): violations.append(ds)
results.append({'test':'T13_selection_grid','checks':checks,'violations':violations})
class FixedTime:
    @staticmethod
    def now(): return datetime(2026,10,7,12,0,0)
original=m.datetime; m.datetime=FixedTime
a=app(rushes[:1],output=root/'T14'); d=a.new_run_dir(); (d/'sentinel').write_text('preserved'); run('T14_timestamp_collision',a); m.datetime=original
results.append({'test':'T14_preservation','sentinel':(d/'sentinel').read_text()})
(root/'results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
print('FINAL',json.dumps(results[-3:],ensure_ascii=False),flush=True)
```

### extra.py

```python
from pathlib import Path
exec(Path('/workspace/audit-source/audit.py').read_text().split('rushes=')[0].replace("audit-evidence-exact","audit-evidence-extra"))
r=media('valid.mp4',2)
narrow=media('narrow.mp4',2,size='80x160')
run('T15_partial_export',app([r,narrow,r],output=root/'T15'))
p=root/'alias.mp4'; p.symlink_to(r); run('T16_alias_short',app([r,p],output=root/'T16'))
a=app([],output=root/'T17')
long_audio=root/'long_audio.mp4'
subprocess.run(['ffmpeg','-y','-v','error','-f','lavfi','-i','color=c=red:s=320x180:r=2:d=2','-f','lavfi','-i','sine=frequency=440:duration=60','-c:v','libx264','-c:a','aac',str(long_audio)],check=True)
run('T17_audio_longer_video',app([long_audio],output=root/'T17'))
for folder in ['T09','T15']:
    for f in root.rglob('short*.mp4'):
        if folder in f.parts: print('PARTIAL_FILE',str(f),f.stat().st_size)
cmd=['ffmpeg','-y','-ss','0','-i',str(narrow),'-t','2','-vf','scale=-2:1920,crop=1080:1920:(iw-1080)/2:0','-c:v','libx264',str(root/'diagnostic.mp4')]
p=subprocess.run(cmd,capture_output=True,text=True); print('NARROW_STDERR',p.returncode,p.stderr[-1700:])
exports=list((root/'T16').rglob('short*.mp4')); print('ALIAS_SHA256',[(p.name,hashlib.sha256(p.read_bytes()).hexdigest()) for p in exports])
(root/'results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
```
