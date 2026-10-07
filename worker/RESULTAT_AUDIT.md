# Audit indépendant — Sentinelles Content Factory MVP 0.3

**Verdict final : BLOQUÉ.**

Le correctif passe les cas historiques obligatoires en MP4, les portraits, les erreurs de création de dossier, les erreurs isolées de rush/export, les alias et le message à zéro export. La règle de durée vidéo reste toutefois violée avec un MKV pris en charge par l’import. Deux autres défauts majeurs sont reproduits : acceptation d’un export dont les images ne se décodent pas, et divergence événement/partenaire entre le texte proposé et le rapport lorsque le formulaire change pendant le rendu.

**Cible et références**

- Dépôt : [noobstrade/sentinelles-content-factory](https://github.com/noobstrade/sentinelles-content-factory).
- Branche auditée : `develop`.
- Commit audité exact : [`a318dde642e6ab542ae602b6b0b83a70876631c9`](https://github.com/noobstrade/sentinelles-content-factory/commit/a318dde642e6ab542ae602b6b0b83a70876631c9).
- Date de l’audit : 7 octobre 2026, UTC.
- Arbre racine audité : `6d16c2641d0b155f642ed4589a9cdf14d7447236`.
- Arbre `app/` audité : `e0a91a0242c9a751f1e3d041ef52e28e0819c87f`.
- Blob Git de `app/app.py` : `c0596fe814fef4a6b69a9c4c4e122c2b2d4a4173`.
- Lectures intégrales avant l’audit de l’application : `worker/A_AUDITER.md` (MVP 0.3), `docs/PRODUCT_SPEC.md`, `docs/AUDIT_BASELINE.md`, `docs/WORKFLOW.md`, puis les six fichiers de `app/`. Aucun `AGENTS.md` dans l’arbre du dépôt.
- Les 12 blobs du snapshot ont été contrôlés par taille et SHA Git avant exécution. Les six fichiers de l’application restent identiques après la suite et les confirmations ; empreintes en annexe.
- Livrable demandé : remplacement de ce seul fichier sur `develop`. Aucun changement de `app/`, aucun correctif d’application, aucune mise à jour de `main`.

La baseline décrit des défauts anciens ; elle n’est pas une preuve de leur persistance. Chaque conclusion ci-dessous s’appuie sur des exécutions de ce commit MVP 0.3.

**Environnement, méthode et portée des preuves**

Linux x86_64, noyau 6.18.44, glibc 2.39 ; Python 3.12.14 ; Tk/Tcl 9.0 ; FFmpeg et ffprobe 6.1.1-3ubuntu5. Import de l’application et analyse syntaxique réussis. Aucune dépendance IA nécessaire pour exécuter le moteur actuel.

Les fonctions originales de `app/app.py` sont chargées sans réécriture. Les médias de test sont réellement générés par FFmpeg. Le probing, les encodages et les décodages sont réels. Les variables de formulaire, la progression et les boîtes de dialogue sont remplacées par des doubles, car cet environnement n’a ni `DISPLAY` ni Xvfb ; l’ouverture de `tk.Tk()` échoue avec `TclError: no display name and no $DISPLAY environment variable`. Cet empêchement d’environnement n’est pas classé comme défaut de l’application.

Les injections sont explicites : horloge/UUID pour les collisions ; retour d’échec d’un encodage ; altération du fichier de sortie après FFmpeg ; erreur d’écriture du texte ; modification du formulaire au point précis suivant l’encodage. Elles éprouvent les garde-fous, sans prétendre mesurer la fréquence naturelle de ces incidents. Le test du rush corrompu et le cas MKV utilisent des entrées réellement présentes sur disque sans remplacement du probing ou du rendu.

Résultat de la suite : **43 tests, 39 réussis, 4 assertions échouées, aucune erreur de harnais**, durée unittest 51,493 s. Les quatre assertions échouées correspondent à **trois défauts distincts** : T24, T36, T37 ; T99 retrouve le même export corrompu que T37. Les tests d’observation T27/T28/T42 peuvent réussir tout en établissant un comportement indésirable ou une limite.

Compléments indépendants C01/C02/C03 :

- C01 : **46 dossiers de génération créés, 46 rapports JSON présents et parseables**, y compris le run de traçage de thread T42. Les échecs de destination/collision épuisée ne créent aucun nouveau run ; il n’y a donc pas de rapport de nouveau run à exiger dans ces cas.
- C02 : le MKV de T36 se décode intégralement sans erreur. La même commande de rendu, avec seulement le début ramené à 0 s et la durée à 2 s dans un fichier de contrôle extérieur au pipeline, produit un H.264/AAC 1080×1920 de 2 s entièrement décodable.
- C03 : appel direct à `App.verify_export()` sur la sortie corrompue de T37 : `True`, alors qu’un décodage indépendant échoue avec le code 69.

La suite contrôle **les 60 fichiers MP4 laissés par le pipeline**, y compris les sorties rejetées, avec ffprobe et décodage FFmpeg complet ; le contrôle positif C02 ajoute un 61e fichier vérifié. Dans la suite, 54 entrées sont marquées `ok` : **53 vidéos 1080×1920 se décodent sans erreur et 1 est invalide**. Parmi les six fichiers exclus du JSON des exports, quatre sont audio-only, un a de mauvaises dimensions et un est du texte invalide. Un décodage audio-only réussi ne prouve pas l’existence d’un Short vidéo.

**Rejeu obligatoire des constats du MVP 0.2**

Les identifiants T ci-dessous sont ceux du présent harnais ; la colonne « ancienne référence » évite de confondre les numérotations des deux audits.

| Constat antérieur / ancienne référence | Tests MVP 0.3 | Conclusion étayée |
|---|---|---|
| Multi-rush historique | T04, T05, T06, T20 | Corrigé dans les cas testés : toutes les sources sont inventoriées et les sources suivantes peuvent alimenter les exports. Maximum 3 exports par run. |
| Déduplication temporelle historique | T02, T03, T07–T10, T30, T31 | Conforme à l’écart minimal de 12 s par `source_id` dans les grilles et rendus testés. |
| Générations successives sans écrasement | T11, T23 | Corrigé dans les scénarios testés : hashes de toute la génération précédente conservés ; collision retry/épuisement gérés. |
| MAJ-01 / ancien T17 : vidéo 2 s, audio 60 s | T29, puis T36/C02 | **Cas MP4 corrigé par T29** : un vrai export vidéo de 2 s. **Règle de durée vidéo non entièrement corrigée** : fallback à la durée conteneur en MKV, T36. Aucun faux succès audio-only en T36 grâce au nouveau contrôle de présence vidéo. |
| MAJ-02 / ancien T09 : portrait 80×160 ; 9:16 et paysage | T18, T15, T04 ; complément T16 | Corrigé dans ces formats : vidéo 1080×1920 présente et décodage intégral sans erreur. |
| MAJ-03 : nom 300 caractères, destination invalide, collision | T22, T21, T23 | Corrigé dans les scénarios injectés : aucune exception échappée, progression arrêtée ; précédente génération conservée. La progression d’un widget Tk réel n’a pas été observée. |
| MAJ-04 / anciens T10–T15 : corruption et export partiel | T20, T19, T33, T38, T41, C01 | Corrigé pour ces erreurs : poursuite des autres sources/candidats, erreurs et sorties valides dans le JSON ; rapport présent après création du run ; fichiers de zéro octet supprimés. |
| MAJ-05 / anciens T11–T16 : chemin réel et symlink | T26, T30, T31, T03 | Corrigé sur Linux pour les alias testés, y compris hardlink : identité physique commune ; pas de doublon du même intervalle. |
| MIN-01 : zéro export annoncé comme prêt | T14, T32, T34, T35, T41 | Corrigé dans ces cas : `no_usable_segment`, message « Aucun segment vidéo exploitable », warning ; aucune annonce de Shorts prêts. |

À 48 s, les trois extraits de 18 s commencent à 3/15/27 s et se chevauchent de 6 s. Ils respectent le seuil demandé de 12 s entre débuts ; ce résultat ne prouve ni l’absence de tout chevauchement ni une déduplication visuelle. L’identification physique testée ne détecte pas nécessairement deux copies de contenu sous des fichiers/inodes différents.

**Grille complète des tests**

| Test | Scénario | Résultat observé |
|---|---|---|
| T01 | Syntaxe AST et import original | OK — APP_NAME = MVP 0.3. |
| T02 | Grille combinatoire 1 à 5 sources, 9 durées, source_id distincts | OK — 66 429 configurations, 0 violation : bornes, limite 3, écart >=12 s, diversité et pool de toutes les sources exploitables. |
| T03 | Grille avec alias de source_id et source en erreur | OK — 120 configurations ; pas de doublon temporel pour la même identité, source en erreur exclue. |
| T04 | Trois rushs distincts, rendu réel et provenance | OK — 3 H.264 1080×1920 ; sources et paramètres FFmpeg concordent avec le JSON ; 3 SHA-256 différents. |
| T05 | Premier rush de 0,5 s, puis trois exploitables | OK — les 4 sources sont inventoriées ; 3 exports des sources suivantes. |
| T06 | Quatre rushs exploitables | OK — 4 sources inventoriées ; 3 exports des trois premières. La limite reste 3 par génération. |
| T07 | Un rush de 2 s | OK — 1 export, aucun triplement artificiel. |
| T08 | Deux rushs de 2 s | OK — 2 exports différents. |
| T09 | Une source de 48 s | OK — starts 3/15/27 s, durées 18 s, 3 hashes différents. |
| T10 | Deux sources de 48 s | OK — sources 1/2/1, starts 3/3/15 s. |
| T11 | Deux générations du même événement | OK — dossiers distincts ; tous les octets MP4/TXT/JSON de la première génération préservés. |
| T12 | Huit noms atypiques : vide, espaces, traversal, Unicode, caractères réservés | OK — noms originaux dans le JSON, chemins contenus dans la destination. |
| T13 | Source de exactement 1 s | OK — 1 export vidéo de 1 s. |
| T14 | Sources de 0,5 s et une seule image | OK — zéro export, no_usable_segment, statut et boîte warning sans annonce de Shorts prêts. |
| T15 | Portrait 90×160, ratio 9:16 | OK — 1 H.264 1080×1920 décodable. |
| T16 | Carré 180×180 | OK — 1 H.264 1080×1920 décodable. |
| T17 | Vidéo avec audio de même durée | OK — audio AAC conservé, vidéo décodable. |
| T18 | Portraits 80×160 (1:2) et 120×320 | OK — 1 export vidéo 1080×1920 pour chacun, décodages complets sans erreur. |
| T19 | Échec injecté au deuxième encodage sur trois | OK — sources inventoriées, erreur export tracée ; exports 1 et 3 valides ; fichier de 0 octet supprimé. |
| T20 | MP4 corrompu au milieu de deux sources valides | OK — les deux autres rushs sont exportés ; troisième rush analysé ; sources et erreur probe dans le JSON. |
| T21 | Destination devenue un fichier | OK — Erreur signalée, aucune exception échappée, progression arrêtée ; aucun run_dir créé. |
| T22 | Événement ASCII de 300 caractères | OK — génération réussie, slug limité à 80 caractères, nom complet dans le JSON. |
| T23 | Horloge et UUID injectés pour une collision puis cinq collisions | OK — retry au deuxième UUID ; épuisement de 5 tentatives géré ; fichiers précédents inchangés ; progression arrêtée. |
| T24 | Modification événement/partenaire après FFmpeg, avant les textes | ÉCHEC — texte du nouvel événement/partenaire, JSON et dossier de l’événement initial ; MAJ-07. |
| T25 | Précontrôles sans fichiers et FFmpeg absent | OK — warning et error respectivement, sans lancement de traitement. |
| T26 | Import réel + doublon de chemin + symlink + hardlink | OK — deux imports uniques sur cinq chemins ; trois alias ignorés. |
| T27 | Lanceur Linux/macOS direct et depuis la racine | OBSERVATION CONFIRMÉE — mode 0644 : PermissionError ; sh app/run_linux_mac.sh depuis la racine : code 2 ; MIN-02. Le test réussit en vérifiant ces défauts. |
| T28 | Deux demandes run_thread avec double de Thread | OBSERVATION — deux workers démarrés, aucun verrou de lancement observé. Concurrence de widgets Tk réels non testée. |
| T29 | MP4 : vidéo 2 s, audio 60 s | OK — durée sélectionnée 2 s, start 0, un export vidéo+audio de 2 s ; aucun faux succès audio-only. |
| T30 | Même rush court par chemin réel, symlink et hardlink | OK — 3 chemins inventoriés, 1 source_id, 1 export ; alias identifiés. |
| T31 | Rush de 48 s et son symlink | OK — 1 identité, starts 3/15/27 s ; pas de répétition du même intervalle sous deux chemins. |
| T32 | FFmpeg réussi, sortie tronquée à 0 octet avant vérification | OK — fichier rejeté et supprimé, zéro status: ok, JSON présent, warning. |
| T33 | Sortie 2 remplacée par un MP4 valide de mauvaises dimensions | OK — rejet 320×180, erreur Dimensions export invalides ; exports 1 et 3 maintenus. |
| T34 | Sortie remplacée par un MP4 audio-only | OK — rejet Export sans flux vidéo ; aucune entrée ok. |
| T35 | Sortie non nulle remplacée par du texte invalide | OK — échec ffprobe, aucune entrée ok ; erreur export enregistrée. |
| T36 | Même vidéo 2 s/audio 60 s remuxée en MKV | ÉCHEC — duration=60.023, starts après la fin des images ; zéro Short valide malgré une vidéo exploitable ; MAJ-01 résiduel. |
| T37 | Payloads H.264 corrompus après rendu, structure MP4 conservée | ÉCHEC — ffprobe code 0, 1080×1920, mais décodage code 69 ; export enregistré ok et annoncé prêt ; MAJ-06. |
| T38 | Échec injecté lors de l’écriture du texte de publication | OK — status failed, erreur run, JSON de secours présent, export valide et traçabilité conservés. |
| T39 | Rush valide, chemin absent et source audio-only | OK — 1 export valide, 3 sources inventoriées, 2 erreurs probe ; poursuite du traitement. |
| T40 | Sources sans audio, MP4 et MKV | OK — un export vidéo sans audio pour chaque source. |
| T41 | Trois sorties de 0 octet après trois encodages réussis | OK — trois tentatives, trois erreurs, zéro export ok, rapport conservé, warning. |
| T42 | process original dans un vrai thread avec doubles d’UI tracés | OBSERVATION — get/set, start/stop et messagebox appelés depuis le worker ; arrêt observé dans les doubles ; sûreté des widgets Tk réels non démontrée. |
| T99 | Contrôle transversal de tous les fichiers MP4 produits | ÉCHEC — 60 fichiers contrôlés, 1 export invalide enregistré ok (T37). Aucun rapport manquant parmi les runs de execute ; couverture complète des 46 runs par C01. |

**Défauts critiques**

Aucun défaut critique reproduit dans ce périmètre. Cette conclusion ne vaut pas validation générale du produit ou de toutes ses plateformes.

**Défauts majeurs ouverts**

**MAJ-01 résiduel — la durée de repli peut encore provenir de l’audio/du conteneur**

Localisation : `app/app.py`, lignes 65–78, particulièrement 73–75 ; sélection lignes 88–105. Preuves : **T36, C02**, avec T29 comme contrôle positif MP4.

Reproduction :

1. Générer un MP4 H.264 avec 2 s de vidéo et 60 s d’AAC, sans `-shortest` à la création de l’entrée.
2. Le remuxer en MKV : `ffmpeg -i long_audio.mp4 -c copy long_audio.mkv`.
3. Importer ce MKV et appeler le pipeline original.
4. Contrôler les paquets vidéo, la durée enregistrée dans `sources` et les starts sélectionnés.

Mesure réelle : le MKV ne renseigne pas `stream.duration`. Son tag vidéo donne `00:00:02.023000000`, son conteneur `60.023000`. Les quatre paquets vidéo ont des PTS 0,023 / 0,523 / 1,523 / 1,023 s, chacun de 0,5 s : la dernière image finit à 2,023 s. `probe_source()` renvoie pourtant `duration: 60.023`.

Résultat : trois starts **6,00575 / 21,0115 / 36,01725 s**, tous après les images. Trois fichiers audio-only subsistent ; chacun est rejeté avec `Export sans flux vidéo`. Le JSON indique `no_usable_segment`, zéro export valide et trois erreurs export, alors que le contrôle C02 produit bien une vidéo de 2 s à partir du même rush.

Attendu : utiliser la durée du flux vidéo pour la sélection, même lorsque le champ `stream.duration` manque, et conserver au moins le segment vidéo exploitable. Le rejet des sorties audio-only est efficace ; il ne répare pas la sélection erronée. Impact : un format explicitement accepté par le sélecteur de fichiers perd tout son contenu vidéo et donne à tort « aucun segment exploitable ».

Condition de levée : rejouer T29 et T36, vérifier la durée vidéo par une mesure indépendante des images/paquets et obtenir des sorties vidéo 1080×1920 décodables sans audio-only enregistré `ok`. **MAJ-01 n’est levé que pour le cas MP4 historique.**

**MAJ-06 — un export aux dimensions correctes peut être déclaré `ok` avec des images indécodables**

Localisation : `app/app.py`, lignes 117–125 (`verify_export`) et 158–160 (acceptation dans le rapport). Preuves : **T37, T99, C03** ; contrôles négatifs complémentaires T32–T35.

Reproduction par injection documentée : encoder normalement le rush de 2 s ; après le retour réussi de FFmpeg, avant `verify_export`, remplacer par des zéros les payloads des quatre paquets H.264 aux positions/taille trouvées par `ffprobe -show_packets`. La structure MP4 et ses métadonnées restent intactes. Le harnais exécute ensuite le vérificateur original et le reste du pipeline sans modification.

Fichier mesuré : **69 596 octets**, SHA-256 `3cfba810b966dc6fff304265c0367917678922f21fbb6db1ec978ad9919f4fca`. ffprobe retourne le code **0** avec une piste vidéo déclarée **1080×1920**, durée **2.000000**, quatre images annoncées dans les métadonnées. Le décodage réel retourne le code **69** et des erreurs `Invalid NAL unit size`, `Error splitting the input into NAL units`, `Decoding error: Invalid data found when processing input`. Aucun décodage vidéo correct n’est établi.

Le vérificateur original retourne pourtant `True`. Le rapport contient une entrée `status: ok`, `status: completed`, `errors: []`, et le statut annonce « Terminé : 1 Shorts prêts à valider ». Le nouvel anti-audio-only et les vérifications de dimensions passent leurs cas de T32–T35, mais ne suffisent pas contre cette corruption.

Attendu : un export invalide ne doit jamais être enregistré `ok`. Impact : la validation proposée à l’utilisateur repose sur un contrôle de métadonnées qui accepte un fichier sans images décodables. La corruption a été provoquée pour tester ce garde-fou ; **aucune fréquence de corruption spontanée ni défaut spontané d’encodage FFmpeg n’est affirmé**.

Condition de levée : rejouer T37 et le contrôle global T99 ; exclure cette sortie de `exports` et tracer l’erreur de validation, tout en conservant les exports valides. Contrôler les images/durée réellement exploitables et le décodage avant acceptation.

**MAJ-07 — une modification du formulaire désynchronise le texte de publication et la génération**

Localisation : `app/app.py`, lignes 23–24 (champs éditables), 130–133 (rapport/dossier initial), 166–167 (nouvelle lecture des champs). Preuve : **T24**.

Reproduction : démarrer avec `Événement initial` et `Partenaire test` ; après l’encodage, modifier les variables en `Autre événement` et `Autre partenaire` avant la création du texte. Ce changement est injecté de façon déterministe ; il ne dépend pas d’un timing manuel dans une fenêtre.

Résultat observé :

- dossier : `v_nement_initial/run_*` ;
- `rapport.json` : `event = Événement initial`, `sponsors = Partenaire test`, un export valide, aucune erreur ;
- `publication_proposee.txt` : titre `Autre événement | Les Sentinelles`, description contenant `Autre événement` et `Autre partenaire` ;
- statut : génération terminée avec un Short prêt à valider.

Attendu : le texte et le rapport d’une même génération doivent employer les mêmes paramètres événement/partenaires. Impact : texte destiné à un autre événement ou à un autre partenaire, alors que la traçabilité du run reste liée aux valeurs initiales. La validation humaine est toujours demandée, mais elle reçoit des éléments contradictoires.

Condition de levée : figer les entrées d’une génération ou empêcher leur modification pendant le run, puis rejouer T24 en vérifiant JSON, dossier, titre et partenaires. Ce défaut est reproduit dans les fonctions originales avec doubles de variables ; la saisie physique dans l’interface Tk n’a pas été testée.

**Défauts mineurs et observations**

**MIN-02 — lanceur Linux/macOS dépendant du répertoire courant et non exécutable.** Preuve T27 ; fichier `app/run_linux_mac.sh`, mode Git `100644`, contenu `python3 app.py`. Exécution directe depuis `app/` : `PermissionError`. Depuis la racine : `sh app/run_linux_mac.sh` retourne 2, car Python cherche `app.py` à la racine. Le README donne une alternative `python app.py` lorsque l’utilisateur se place dans `app/`. Condition de levée : rejouer les deux modes de lancement depuis des répertoires pertinents ; sur une session graphique, vérifier le démarrage réel. macOS n’a pas été exécuté.

**MIN-03 — documentation de version décalée.** Lecture intégrale de `app/README.md` : titre et capacités décrites comme MVP 0.2 ; T01 établit que l’application est MVP 0.3. `app/ROADMAP.md` place encore tests automatisés et séparation moteur/UI dans la version 0.3 ; le snapshot contient seulement les six fichiers listés, sans suite de tests livrée ni moteur séparé. La roadmap est un plan, pas la preuve qu’une fonctionnalité existe. Condition de levée du décalage : aligner la documentation sur le périmètre réellement livré. Aucun fichier n’a été changé pour cela.

Les erreurs partielles de T19/T20 sont conservées dans `rapport.json`, mais l’UI simulée reçoit seulement l’annonce finale du nombre d’exports. Le statut JSON reste `completed` dès qu’un export existe. Cette observation ne remet pas en cause la poursuite et la traçabilité démontrées ; elle indique que l’affichage d’un résumé d’erreurs n’a pas été livré.

**Tk/thread — risque examiné, sûreté non validée.** T28 observe deux appels à `run_thread()` qui lancent deux workers, sans garde observée. T42 exécute le vrai `process` dans un thread Python et trace des appels aux interfaces de variables, progression et messagebox depuis ce worker. Le code n’effectue pas de transfert explicite vers la boucle UI. Les appels `progress.start`, `status.set` et les lectures initiales de formulaire se trouvent avant le `try` principal. Avec les doubles, l’arrêt de progression fonctionne dans les cas testés ; cela ne démontre pas le comportement des widgets Tk réels. Aucun crash Tk, blocage graphique ou absence de crash n’est déclaré reproduit. Windows, macOS, fermeture de fenêtre en cours de traitement et double lancement avec widgets réels restent à exercer dans une session graphique.

**Périmètre fonctionnel réellement constaté**

Le pipeline actuel importe/inventorie plusieurs rushs, génère des candidats aux fractions temporelles fixes 25/50/75 %, sélectionne au maximum trois extraits avec écart minimal de début par identité, recadre au centre et dessine un bandeau fixe « LES SENTINELLES ». Il produit des fichiers locaux versionnés, un texte social générique et un rapport de provenance. Le champ partenaires alimente ce texte ; il ne constitue pas un Sponsor Manager ou une intégration de règles partenaires.

La présence de dépendances `faster-whisper`/`scenedetect` dans `requirements.txt` ne prouve aucune intégration : aucune transcription, aucun sous-titre, aucun scoring hockey intelligent, aucune sélection multimodale, aucun suivi intelligent 9:16, aucun Sponsor Manager et aucun reporting partenaire ne sont déclarés présents. Aucune mesure de pertinence hockey, de qualité du cadrage en action réelle, de gain de temps bénévole ou d’audience commerciale n’a été réalisée. L’application rappelle la validation humaine ; un circuit de validation éditoriale complet n’est pas démontré.

**Décision et conditions du prochain audit**

**BLOQUÉ** sur le commit `a318dde642e6ab542ae602b6b0b83a70876631c9` : MAJ-01 résiduel, MAJ-06 et MAJ-07 reproduits. Les progrès prouvés ne suffisent pas à déclarer ce commit `CANDIDAT` ou `VALIDÉ`. Lever ces trois constats avec les retests indiqués, conserver les réussites historiques et refaire les essais Tk dans un environnement graphique avant une déclaration de sûreté UI. Aucun passage vers `main` effectué.

**Annexe — contrôle individuel des sorties**

Pour chaque fichier laissé par le pipeline : ffprobe réel, présence/dimensions de la vidéo, durée vidéo déclarée lorsqu’elle est disponible, puis décodage complet `ffmpeg -v error -i FICHIER -f null -`. « ok » ci-dessous est la valeur du rapport de l’application, pas le verdict de l’auditeur. Le code 0 avec stderr vide signifie décodage réussi ; il ne transforme pas un fichier audio-only en vidéo. Les sorties de zéro octet T19/T32/T41 ont été supprimées par l’application et ne figurent pas comme fichiers laissés.

| Test | Fichier | Octets | Vidéo selon ffprobe | Durée vidéo (s) | Décodage FFmpeg | Rapport exports |
|---|---|---:|---|---|---|---|
| T04 | short_01_9x16.mp4 | 69596 | 1080×1920 | 2.000000 | 0 / stderr vide | ok |
| T04 | short_02_9x16.mp4 | 70385 | 1080×1920 | 2.000000 | 0 / stderr vide | ok |
| T04 | short_03_9x16.mp4 | 69540 | 1080×1920 | 2.000000 | 0 / stderr vide | ok |
| T05 | short_01_9x16.mp4 | 69596 | 1080×1920 | 2.000000 | 0 / stderr vide | ok |
| T05 | short_02_9x16.mp4 | 70385 | 1080×1920 | 2.000000 | 0 / stderr vide | ok |
| T05 | short_03_9x16.mp4 | 69540 | 1080×1920 | 2.000000 | 0 / stderr vide | ok |
| T06 | short_01_9x16.mp4 | 69596 | 1080×1920 | 2.000000 | 0 / stderr vide | ok |
| T06 | short_02_9x16.mp4 | 70385 | 1080×1920 | 2.000000 | 0 / stderr vide | ok |
| T06 | short_03_9x16.mp4 | 69540 | 1080×1920 | 2.000000 | 0 / stderr vide | ok |
| T07 | short_01_9x16.mp4 | 69596 | 1080×1920 | 2.000000 | 0 / stderr vide | ok |
| T08 | short_01_9x16.mp4 | 69596 | 1080×1920 | 2.000000 | 0 / stderr vide | ok |
| T08 | short_02_9x16.mp4 | 70385 | 1080×1920 | 2.000000 | 0 / stderr vide | ok |
| T09 | short_01_9x16.mp4 | 635774 | 1080×1920 | 18.000000 | 0 / stderr vide | ok |
| T09 | short_02_9x16.mp4 | 636015 | 1080×1920 | 18.000000 | 0 / stderr vide | ok |
| T09 | short_03_9x16.mp4 | 635995 | 1080×1920 | 18.000000 | 0 / stderr vide | ok |
| T10 | short_01_9x16.mp4 | 635774 | 1080×1920 | 18.000000 | 0 / stderr vide | ok |
| T10 | short_02_9x16.mp4 | 631601 | 1080×1920 | 18.000000 | 0 / stderr vide | ok |
| T10 | short_03_9x16.mp4 | 636015 | 1080×1920 | 18.000000 | 0 / stderr vide | ok |
| T11_a | short_01_9x16.mp4 | 69596 | 1080×1920 | 2.000000 | 0 / stderr vide | ok |
| T11_b | short_01_9x16.mp4 | 70385 | 1080×1920 | 2.000000 | 0 / stderr vide | ok |
| T12_0 | short_01_9x16.mp4 | 69596 | 1080×1920 | 2.000000 | 0 / stderr vide | ok |
| T12_1 | short_01_9x16.mp4 | 69596 | 1080×1920 | 2.000000 | 0 / stderr vide | ok |
| T12_2 | short_01_9x16.mp4 | 69596 | 1080×1920 | 2.000000 | 0 / stderr vide | ok |
| T12_3 | short_01_9x16.mp4 | 69596 | 1080×1920 | 2.000000 | 0 / stderr vide | ok |
| T12_4 | short_01_9x16.mp4 | 69596 | 1080×1920 | 2.000000 | 0 / stderr vide | ok |
| T12_5 | short_01_9x16.mp4 | 69596 | 1080×1920 | 2.000000 | 0 / stderr vide | ok |
| T12_6 | short_01_9x16.mp4 | 69596 | 1080×1920 | 2.000000 | 0 / stderr vide | ok |
| T12_7 | short_01_9x16.mp4 | 69596 | 1080×1920 | 2.000000 | 0 / stderr vide | ok |
| T13 | short_01_9x16.mp4 | 158338 | 1080×1920 | 1.000000 | 0 / stderr vide | ok |
| T15 | short_01_9x16.mp4 | 148442 | 1080×1920 | 2.000000 | 0 / stderr vide | ok |
| T16 | short_01_9x16.mp4 | 135631 | 1080×1920 | 2.000000 | 0 / stderr vide | ok |
| T17 | short_01_9x16.mp4 | 99151 | 1080×1920 | 2.000000 | 0 / stderr vide | ok |
| T18_narrow | short_01_9x16.mp4 | 140894 | 1080×1920 | 2.000000 | 0 / stderr vide | ok |
| T18_extra_narrow | short_01_9x16.mp4 | 120274 | 1080×1920 | 2.000000 | 0 / stderr vide | ok |
| T19 | short_01_9x16.mp4 | 69596 | 1080×1920 | 2.000000 | 0 / stderr vide | ok |
| T19 | short_03_9x16.mp4 | 69540 | 1080×1920 | 2.000000 | 0 / stderr vide | ok |
| T20 | short_01_9x16.mp4 | 69596 | 1080×1920 | 2.000000 | 0 / stderr vide | ok |
| T20 | short_02_9x16.mp4 | 69540 | 1080×1920 | 2.000000 | 0 / stderr vide | ok |
| T22 | short_01_9x16.mp4 | 69596 | 1080×1920 | 2.000000 | 0 / stderr vide | ok |
| T23_a | short_01_9x16.mp4 | 69596 | 1080×1920 | 2.000000 | 0 / stderr vide | ok |
| T23_retry | short_01_9x16.mp4 | 70385 | 1080×1920 | 2.000000 | 0 / stderr vide | ok |
| T24 | short_01_9x16.mp4 | 69596 | 1080×1920 | 2.000000 | 0 / stderr vide | ok |
| T29 | short_01_9x16.mp4 | 99380 | 1080×1920 | 2.000000 | 0 / stderr vide | ok |
| T30 | short_01_9x16.mp4 | 69596 | 1080×1920 | 2.000000 | 0 / stderr vide | ok |
| T31 | short_01_9x16.mp4 | 635774 | 1080×1920 | 18.000000 | 0 / stderr vide | ok |
| T31 | short_02_9x16.mp4 | 636015 | 1080×1920 | 18.000000 | 0 / stderr vide | ok |
| T31 | short_03_9x16.mp4 | 635995 | 1080×1920 | 18.000000 | 0 / stderr vide | ok |
| T33 | short_01_9x16.mp4 | 69596 | 1080×1920 | 2.000000 | 0 / stderr vide | ok |
| T33 | short_02_9x16.mp4 | 16907 | 320×180 | 2.000000 | 0 / stderr vide | exclu |
| T33 | short_03_9x16.mp4 | 69540 | 1080×1920 | 2.000000 | 0 / stderr vide | ok |
| T34 | short_01_9x16.mp4 | 18785 | aucune vidéo | — | 0 / stderr vide | exclu |
| T35 | short_01_9x16.mp4 | 26 | ffprobe en échec | — | 183 / erreurs | exclu |
| T36 | short_01_9x16.mp4 | 100708 | aucune vidéo | — | 0 / stderr vide | exclu |
| T36 | short_02_9x16.mp4 | 34298 | aucune vidéo | — | 0 / stderr vide | exclu |
| T36 | short_03_9x16.mp4 | 131679 | aucune vidéo | — | 0 / stderr vide | exclu |
| T37 | short_01_9x16.mp4 | 69596 | 1080×1920 | 2.000000 | 69 / erreurs | ok |
| T38 | short_01_9x16.mp4 | 69596 | 1080×1920 | 2.000000 | 0 / stderr vide | ok |
| T39 | short_01_9x16.mp4 | 69596 | 1080×1920 | 2.000000 | 0 / stderr vide | ok |
| T40_r1 | short_01_9x16.mp4 | 69596 | 1080×1920 | 2.000000 | 0 / stderr vide | ok |
| T40_silent_mkv | short_01_9x16.mp4 | 69596 | 1080×1920 | 2.000000 | 0 / stderr vide | ok |

Contrôle C02 extérieur au pipeline : `mkv_at_actual_video_start.mp4`, vidéo 1080×1920 de 2 s, AAC 2 s ; rendu code 0, ffprobe code 0, décodage code 0, stderr vide. Il prouve que les images de la source MKV sont exploitables et ne constitue pas une correction de l’application.

**Annexe — intégrité de l’application**

SHA-256 des octets avant/après ; comparaison exacte, mêmes chemins et mêmes six fichiers. Aucun `__pycache__` ajouté dans `app/`.

| Fichier | SHA-256 identique avant/après |
|---|---|
| app/README.md | `9a6fd2e07bfa16230b0ecb425d83dde33e91024a0573a3e8cc10a168a1952412` |
| app/ROADMAP.md | `e98b00f8ec9dc508fb675f01aa96bef1a86f181c465e8b760e66cae4e0fcd25b` |
| app/app.py | `2f9ee1bcfdd03c390a846fad652e605f31465901c2f71efaa80a60ff3c611b78` |
| app/requirements.txt | `be654442659daf5deace60880d5b13bda39c702793ff78a0e6ea2ddd2e7ef64b` |
| app/run_linux_mac.sh | `1a1032a1498d3370155a0ff2952d26bfcc88a68cad53c9f1a473189e5f8fca16` |
| app/run_windows.bat | `92f53ecbc23b49cf50624c8de78dc5dbbb119237c1ac45fc03e0ff2dd3e76f5e` |

**Annexe — reproductions autonomes**

Copier les deux blocs Python ci-dessous dans `/tmp/audit_v03.py` et `/tmp/confirm_v03.py`. Ils doivent être exécutés hors du dépôt. Utiliser un répertoire de résultats **neuf**, car les fixtures contiennent des liens créés au lancement. Les dimensions, codes et statuts sont les preuves portables ; les timestamps, identités inode et hashes d’encodage peuvent varier selon la machine/version de FFmpeg.

```sh
git clone --branch develop https://github.com/noobstrade/sentinelles-content-factory.git /tmp/sentinelles-mvp03
git -C /tmp/sentinelles-mvp03 checkout --detach a318dde642e6ab542ae602b6b0b83a70876631c9
PYTHONDONTWRITEBYTECODE=1 python3 /tmp/audit_v03.py /tmp/sentinelles-mvp03 /tmp/sentinelles-audit03-resultats-neufs
PYTHONDONTWRITEBYTECODE=1 python3 /tmp/confirm_v03.py /tmp/sentinelles-mvp03 /tmp/sentinelles-audit03-resultats-neufs
```

Le premier script retourne **1 attendu sur ce commit**, car les quatre assertions T24/T36/T37/T99 échouent ; il écrit néanmoins `evidence.json` avec tous les résultats. Le second script doit être lancé ensuite, séparément ; il écrit `confirmations.json` et retourne 0 lorsque les trois confirmations sont établies. Python standard, Tk importable, FFmpeg/ffprobe avec libx264 et drawtext suffisent. Aucune installation d’un service IA n’est utilisée.

| Script exécuté et reproduit ci-dessous | SHA-256 |
|---|---|
| audit_v03.py | `e6b0d6808b006c1dcb1cb09e5a3ebcba8995d0bf60069461a30e434ebc1e1f75` |
| confirm_v03.py | `10d87ced6ee33d5239692aba64469cecebc0c3ab3ac421630bac7ba73daeb568` |

Empreintes des traces d’exécution originales ; ces traces sont résumées dans ce rapport et peuvent être régénérées par les scripts :

| Trace | SHA-256 de cette exécution |
|---|---|
| test_run_v03.log | `6ae974d9a4a6c634fd04ff49f2f1eb302779ef623f1b9826233477c32f0c08b8` |
| confirm_run_v03.log | `e8d137f38502db9f81bcd178885e7843b0a3d8ff31d63630b089865668cf038e` |
| execution_v03/evidence.json | `591a454e729997b507ddae7c68f927abfda2ec439c7ca38903a5a505bb0c242d` |
| execution_v03/confirmations.json | `4dbe3c332c31e237ba202b897faeeb0034337e4c37715f77ba3cda2a438b5de2` |

**Code de `audit_v03.py`**

```python
"""Independent MVP 0.3 audit. No application file is modified.
Usage: PYTHONDONTWRITEBYTECODE=1 python3 audit_v03.py /path/to/repo /new/output/dir
"""
import ast
import hashlib
import importlib.util
import itertools
import json
import os
import platform
import shutil
import subprocess
import sys
import time
import unittest
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

sys.dont_write_bytecode = True
REPO = Path(sys.argv[1]).resolve()
ROOT = Path(sys.argv[2]).resolve()
sys.argv = [sys.argv[0]]
ROOT.mkdir(parents=True, exist_ok=True)
spec = importlib.util.spec_from_file_location('sentinelles_audited_app', REPO/'app/app.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
App = module.App
REAL_RUN = subprocess.run
REAL_CHECK = subprocess.check_output
EVIDENCE = {}
FIXTURES = ROOT/'fixtures'
FIXTURES.mkdir(exist_ok=True)
APP_BEFORE = {str(p.relative_to(REPO)): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in (REPO/'app').rglob('*') if p.is_file()}

def probe(path):
    p = REAL_RUN(['ffprobe','-v','error','-show_entries',
                  'stream=codec_name,codec_type,width,height,duration,nb_frames,start_time:stream_tags=DURATION:format=duration',
                  '-of','json',str(path)],capture_output=True,text=True)
    if p.returncode: raise subprocess.CalledProcessError(p.returncode,p.args,output=p.stdout,stderr=p.stderr)
    return json.loads(p.stdout)

def decode(path):
    p = REAL_RUN(['ffmpeg','-v','error','-i',str(path),'-f','null','-'],
                 stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,text=True)
    return {'returncode':p.returncode,'stderr':p.stderr}

def generate(name,size,duration,fps=2,hue=0,audio=False):
    target=FIXTURES/(name+'.mp4')
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','lavfi','-i',
         f'testsrc2=size={size}:rate={fps}:duration={duration}']
    if audio:
        cmd+=['-f','lavfi','-i',f'sine=frequency=440:sample_rate=44100:duration={duration}','-c:a','aac']
    cmd+=['-vf',f'hue=h={hue}','-c:v','libx264','-pix_fmt','yuv420p',str(target)]
    REAL_RUN(cmd,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
    return target

FILES={}
for name,size,dur,fps,hue,audio in [
    ('r1','320x180',2,2,0,False),('r2','320x180',2,2,90,False),
    ('r3','320x180',2,2,180,False),('r4','320x180',2,2,270,False),
    ('long1','320x180',48,2,0,False),('long2','320x180',48,2,90,False),
    ('one_second','320x180',1,30,0,False),('half_second','320x180',.5,30,0,False),
    ('one_frame','320x180',1/30,30,0,False),('vertical','90x160',2,2,0,False),
    ('square','180x180',2,2,0,False),('narrow','80x160',2,2,0,False),
    ('extra_narrow','120x320',2,2,0,False),('audio','320x180',2,2,0,True)]:
    FILES[name]=generate(name,size,dur,fps,hue,audio)
FILES['corrupt']=FIXTURES/'corrupt.mp4'
FILES['corrupt'].write_bytes(b'This is not a video file.\n')
FILES['alias']=FIXTURES/'alias.mp4'
FILES['alias'].symlink_to(FILES['r1'])
FILES['hardlink']=FIXTURES/'hardlink.mp4'
os.link(FILES['r1'],FILES['hardlink'])
FILES['long_alias']=FIXTURES/'long_alias.mp4'
FILES['long_alias'].symlink_to(FILES['long1'])
FILES['long_audio']=FIXTURES/'long_audio.mp4'
REAL_RUN(['ffmpeg','-hide_banner','-loglevel','error','-y',
          '-f','lavfi','-i','testsrc2=size=320x180:rate=2:duration=2',
          '-f','lavfi','-i','sine=frequency=440:sample_rate=44100:duration=60',
          '-c:v','libx264','-pix_fmt','yuv420p','-c:a','aac',str(FILES['long_audio'])],
         check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
FILES['long_audio_mkv']=FIXTURES/'long_audio.mkv'
REAL_RUN(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(FILES['long_audio']),
          '-c','copy',str(FILES['long_audio_mkv'])],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
FILES['silent_mkv']=FIXTURES/'silent.mkv'
REAL_RUN(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(FILES['r1']),
          '-c','copy',str(FILES['silent_mkv'])],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
FILES['audio_only']=FIXTURES/'audio_only.mp4'
REAL_RUN(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(FILES['audio']),
          '-vn','-c:a','copy',str(FILES['audio_only'])],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
FILES['missing']=FIXTURES/'missing.mp4'

class Value:
    def __init__(self,value): self.value=value
    def get(self): return self.value
    def set(self,value): self.value=value

class Progress:
    def __init__(self): self.active=False; self.starts=0; self.stops=0
    def start(self,interval): self.active=True; self.starts+=1
    def stop(self): self.active=False; self.stops+=1

def runner(output,files,event='Événement test',sponsor='Partenaire test'):
    x=SimpleNamespace(output=Path(output),files=[str(FILES.get(f,f)) for f in files],
                      event=Value(event),sponsor=Value(sponsor),status=Value('Prêt'),progress=Progress())
    for name in ['event_slug','source_id','probe_source','build_candidates','select_candidates','verify_export']:
        setattr(x,name,getattr(App,name))
    x.duration=lambda f:App.duration(x,f)
    x.new_run_dir=lambda:App.new_run_dir(x)
    return x

def corrupt_packets(path):
    data=json.loads(REAL_CHECK(['ffprobe','-v','error','-select_streams','v:0','-show_packets',
                               '-show_entries','packet=pos,size','-of','json',str(path)],text=True))
    b=bytearray(path.read_bytes())
    for packet in data['packets']:
        pos=int(packet['pos']);size=int(packet['size'])
        b[pos:pos+size]=b'\0'*size
    path.write_bytes(b)
    return data['packets']

def execute(identifier,files,event='Événement test',output=None,hook=None,
            render_failure=None,publication_failure=False):
    output=Path(output or ROOT/identifier)
    if not output.exists(): output.mkdir(parents=True)
    x=runner(output,files,event)
    messages=[];commands=[];escaped=None
    before_dirs=set(output.rglob('run_*')) if output.is_dir() else set()
    write_text=Path.write_text
    def run(cmd,*args,**kwargs):
        is_render=cmd[0]=='ffmpeg'
        if is_render:
            commands.append(cmd[:])
            if render_failure is not None and len(commands)==render_failure:
                Path(cmd[-1]).write_bytes(b'')
                raise subprocess.CalledProcessError(1,cmd,stderr='audit injection: failed export')
        result=REAL_RUN(cmd,*args,**kwargs)
        if hook and is_render: hook(x,cmd)
        return result
    def write(path,*args,**kwargs):
        if publication_failure and path.name=='publication_proposee.txt':
            raise PermissionError('audit injection: publication write denied')
        return write_text(path,*args,**kwargs)
    with patch.object(module.subprocess,'run',side_effect=run), \
         patch.object(Path,'write_text',write), \
         patch.object(module.messagebox,'showinfo',side_effect=lambda *a:messages.append(['info',*a])), \
         patch.object(module.messagebox,'showwarning',side_effect=lambda *a:messages.append(['warning',*a])), \
         patch.object(module.messagebox,'showerror',side_effect=lambda *a:messages.append(['error',*a])):
        try: App.process(x)
        except Exception as e: escaped={'type':type(e).__name__,'message':str(e)}
    after_dirs=set(output.rglob('run_*')) if output.is_dir() else set()
    created=sorted(after_dirs-before_dirs)
    report=None;copy=None;exports=[];reports=[]
    for folder in created:
        report_path=folder/'rapport.json'
        reports.append({'run_dir':str(folder),'exists':report_path.is_file()})
        if report_path.is_file(): report=json.loads(report_path.read_text())
        if (folder/'publication_proposee.txt').exists(): copy=(folder/'publication_proposee.txt').read_text()
        for path in sorted(folder.glob('*.mp4')):
            item={'name':path.name,'file':str(path),'bytes':path.stat().st_size,
                  'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
            try: item['probe']=probe(path)
            except subprocess.CalledProcessError as e: item['probe_error']={'returncode':e.returncode,'stderr':e.stderr}
            item['decode']=decode(path)
            exports.append(item)
    evidence={'inputs':x.files,'event_input':event,'status':x.status.get(),
              'progress_active':x.progress.active,'progress_starts':x.progress.starts,'progress_stops':x.progress.stops,
              'escaped':escaped,'messages':messages,'run_dirs':[str(p) for p in created],
              'reports':reports,'commands':commands,'report':report,'publication':copy,'outputs':exports}
    EVIDENCE[identifier]=evidence
    return evidence

def source(name,duration,sid=None,error=None):
    r={'file':name,'source_id':sid or name,'duration':duration}
    if error:r['error']=error
    return r

class AuditTests(unittest.TestCase):
    def assert_finished(self,r):
        self.assertIsNone(r['escaped'])
        self.assertFalse(r['progress_active'])
        self.assertEqual(r['progress_stops'],1)
        self.assertIsNotNone(r['report'])
        self.assertTrue(all(item['exists'] for item in r['reports']))
        self.assertEqual(r['report']['schema_version'],'0.3')

    def assert_render_ok(self,r,count):
        self.assert_finished(r)
        self.assertTrue(r['status'].startswith('Terminé :'))
        self.assertEqual(len(r['report']['exports']),count)
        self.assertEqual(r['report']['status'],'completed')
        valid={o['file']:o for o in r['outputs']}
        for e in r['report']['exports']:
            self.assertEqual(e['status'],'ok')
            item=valid[e['file']]
            self.assertGreater(item['bytes'],0)
            stream=next(s for s in item['probe']['streams'] if s['codec_type']=='video')
            self.assertEqual((stream['width'],stream['height'],stream['codec_name']),(1080,1920,'h264'))
            self.assertEqual(item['decode'],{'returncode':0,'stderr':''})

    def assert_no_output(self,r):
        self.assert_finished(r)
        self.assertEqual(r['report']['exports'],[])
        self.assertEqual(r['report']['status'],'no_usable_segment')
        self.assertIn('Aucun segment',r['status'])
        self.assertNotIn('prêts à valider',r['status'])
        self.assertTrue(any(m[0]=='warning' for m in r['messages']))

    def test_T01_syntax_and_import(self):
        ast.parse((REPO/'app/app.py').read_text())
        self.assertEqual(module.APP_NAME,'Sentinelles Content Factory MVP 0.3')
        EVIDENCE['T01']={'syntax':'OK','import':'OK'}

    def test_T02_selection_combinatorial_grid(self):
        durations=(.5,1,2,10,18,24,48,60,120)
        cases=0
        for n in range(1,6):
            for ds in itertools.product(durations,repeat=n):
                sources=[source(str(i),d) for i,d in enumerate(ds)]
                pool=App.build_candidates(sources);selected=App.select_candidates(pool)
                self.assertLessEqual(len(selected),3)
                usable={s['source_id'] for s in sources if s['duration']>=1}
                self.assertEqual({c['source_id'] for c in pool},usable)
                if len(usable)>=3:
                    self.assertEqual(len({c['source_id'] for c in selected}),3)
                for a,b in itertools.combinations(selected,2):
                    if a['source_id']==b['source_id']:
                        self.assertGreaterEqual(abs(a['start']-b['start']),12)
                for c in selected:
                    self.assertGreaterEqual(c['start'],0);self.assertGreaterEqual(c['duration'],1)
                    self.assertLessEqual(c['duration'],18)
                    self.assertLessEqual(c['start']+c['duration'],ds[int(c['source_id'])]+1e-9)
                cases+=1
        self.assertEqual(cases,66429)
        EVIDENCE['T02']={'cases':cases,'violations':0,'source_identity':'source_id',
                         'durations':durations,'source_counts':[1,2,3,4,5]}

    def test_T03_alias_and_error_selector_grid(self):
        cases=0
        for n in range(1,5):
            for ds in itertools.product((.5,2,48),repeat=n):
                sources=[]
                for i,d in enumerate(ds):
                    sources.extend([source(f'r{i}',d,f'id{i}'),source(f'alias{i}',d,f'id{i}')])
                sources.append(source('corrupt',0,'bad','probe error'))
                selected=App.select_candidates(App.build_candidates(sources))
                self.assertFalse(any(c['source_id']=='bad' for c in selected))
                for a,b in itertools.combinations(selected,2):
                    if a['source_id']==b['source_id']:
                        self.assertGreaterEqual(abs(a['start']-b['start']),12)
                cases+=1
        actual=App.select_candidates(App.build_candidates([source('r',48)]))
        self.assertEqual([c['start'] for c in actual],[3,15,27])
        EVIDENCE['T03']={'cases':cases,'boundary_48s':actual,'violations':0}

    def test_T04_three_rushs_real_render_and_provenance(self):
        r=execute('T04',['r1','r2','r3']);self.assert_render_ok(r,3)
        self.assertEqual([e['source'] for e in r['report']['exports']],r['inputs'])
        for e,cmd in zip(r['report']['exports'],r['commands']):
            self.assertEqual(e['source'],cmd[cmd.index('-i')+1])
            self.assertEqual(e['source_id'],App.source_id(e['source']))
            self.assertEqual(e['start'],float(cmd[cmd.index('-ss')+1]))
            self.assertEqual(e['duration'],float(cmd[cmd.index('-t')+1]))
        self.assertEqual(len({o['sha256'] for o in r['outputs']}),3)

    def test_T05_skip_short_first_inventory_all(self):
        r=execute('T05',['half_second','r1','r2','r3']);self.assert_render_ok(r,3)
        self.assertEqual([s['file'] for s in r['report']['sources']],r['inputs'])
        self.assertEqual([e['source'] for e in r['report']['exports']],r['inputs'][1:])

    def test_T06_four_usable_rushs_all_in_inventory(self):
        r=execute('T06',['r1','r2','r3','r4']);self.assert_render_ok(r,3)
        self.assertEqual(len(r['report']['sources']),4)
        self.assertEqual([e['source'] for e in r['report']['exports']],r['inputs'][:3])

    def test_T07_one_short_rush_no_triplicate(self):
        r=execute('T07',['r1']);self.assert_render_ok(r,1)
        self.assertEqual(len(r['report']['candidates']),1)

    def test_T08_two_short_rushs_no_triplicate(self):
        r=execute('T08',['r1','r2']);self.assert_render_ok(r,2)
        self.assertEqual(len({o['sha256'] for o in r['outputs']}),2)

    def test_T09_single_long_rush_exact_gap(self):
        r=execute('T09',['long1']);self.assert_render_ok(r,3)
        self.assertEqual([e['start'] for e in r['report']['exports']],[3,15,27])
        for o in r['outputs']:self.assertAlmostEqual(float(o['probe']['format']['duration']),18,places=2)
        self.assertEqual(len({o['sha256'] for o in r['outputs']}),3)

    def test_T10_two_long_rushs(self):
        r=execute('T10',['long1','long2']);self.assert_render_ok(r,3)
        self.assertEqual([e['source'] for e in r['report']['exports']],r['inputs']+[r['inputs'][0]])
        self.assertEqual([e['start'] for e in r['report']['exports']],[3,3,15])

    def test_T11_two_runs_preserve_previous_bytes(self):
        output=ROOT/'T11';a=execute('T11_a',['r1'],'Même événement',output);self.assert_render_ok(a,1)
        folder=Path(a['run_dirs'][0])
        before={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in folder.iterdir() if p.is_file()}
        b=execute('T11_b',['r2'],'Même événement',output);self.assert_render_ok(b,1)
        after={p:hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in before}
        self.assertEqual(before,after);self.assertNotEqual(a['run_dirs'],b['run_dirs'])
        EVIDENCE['T11']={'first_run':a['run_dirs'],'second_run':b['run_dirs'],'before':before,
                         'after':after,'preserved':True}

    def test_T12_atypical_event_names(self):
        names=['','   ','../../équipe / hockey ? 🏒','日本語🏒','A/B\\C:*?<>|','.','..','été 2026']
        for i,name in enumerate(names):
            r=execute('T12_'+str(i),['r1'],name,ROOT/'T12');self.assert_render_ok(r,1)
            self.assertEqual(r['report']['event'],name)
            self.assertEqual(Path(r['run_dirs'][0]).parent.parent.resolve(),(ROOT/'T12').resolve())
        EVIDENCE['T12']={'names':names,'cases':len(names),'result':'contained paths and original names'}

    def test_T13_one_second_boundary(self):
        r=execute('T13',['one_second']);self.assert_render_ok(r,1)
        self.assertAlmostEqual(float(r['outputs'][0]['probe']['format']['duration']),1,places=2)

    def test_T14_zero_exports_warning(self):
        for name in ['half_second','one_frame']:
            r=execute('T14_'+name,[name]);self.assert_no_output(r)
            self.assertEqual(len(r['report']['sources']),1)
            self.assertEqual(r['report']['candidates'],[])
        EVIDENCE['T14']={'result':'no_usable_segment and warning for both short valid sources'}

    def test_T15_standard_vertical(self):
        r=execute('T15',['vertical']);self.assert_render_ok(r,1)

    def test_T16_square(self):
        r=execute('T16',['square']);self.assert_render_ok(r,1)

    def test_T17_audio_preserved(self):
        r=execute('T17',['audio']);self.assert_render_ok(r,1)
        audio=[s for s in r['outputs'][0]['probe']['streams'] if s['codec_type']=='audio']
        self.assertEqual(audio[0]['codec_name'],'aac')

    def test_T18_portrait_80x160_and_120x320(self):
        for name in ['narrow','extra_narrow']:
            r=execute('T18_'+name,[name]);self.assert_render_ok(r,1)
        EVIDENCE['T18']={'sizes':['80x160','120x320'],'exports_each':1}

    def test_T19_failed_second_export_continues_and_traces(self):
        r=execute('T19',['r1','r2','r3'],render_failure=2);self.assert_render_ok(r,2)
        self.assertEqual([e['source'] for e in r['report']['exports']],[r['inputs'][0],r['inputs'][2]])
        self.assertEqual(len(r['report']['sources']),3)
        self.assertEqual(len(r['report']['errors']),1)
        self.assertEqual(r['report']['errors'][0]['stage'],'export')
        self.assertFalse(Path(r['report']['errors'][0]['output']).exists())

    def test_T20_corrupt_middle_continues_inventory_and_report(self):
        r=execute('T20',['r1','corrupt','r3']);self.assert_render_ok(r,2)
        self.assertEqual([s['file'] for s in r['report']['sources']],r['inputs'])
        self.assertTrue(r['report']['sources'][1]['error'])
        self.assertEqual(r['report']['errors'][0]['stage'],'probe')
        self.assertEqual([e['source'] for e in r['report']['exports']],[r['inputs'][0],r['inputs'][2]])

    def test_T21_invalid_destination_is_handled(self):
        blocked=ROOT/'T21_output_is_file';blocked.write_bytes(b'not a directory')
        r=execute('T21',['r1'],output=blocked)
        self.assertIsNone(r['escaped']);self.assertFalse(r['progress_active'])
        self.assertEqual(r['progress_stops'],1);self.assertEqual(r['status'],'Erreur')
        self.assertEqual(r['run_dirs'],[])

    def test_T22_event_300_characters(self):
        r=execute('T22',['r1'],'A'*300);self.assert_render_ok(r,1)
        self.assertEqual(len(Path(r['run_dirs'][0]).parent.name),80)
        self.assertEqual(r['report']['event'],'A'*300)

    def test_T23_collision_retry_and_exhaustion(self):
        class FixedDateTime:
            @staticmethod
            def now():return datetime(2026,10,7,15,30,0,123456)
        collision=SimpleNamespace(hex='a'*32);next_id=SimpleNamespace(hex='b'*32)
        with patch.object(module,'datetime',FixedDateTime),patch.object(module.uuid,'uuid4',return_value=collision):
            a=execute('T23_a',['r1'],'Collision',ROOT/'T23');self.assert_render_ok(a,1)
        folder=Path(a['run_dirs'][0])
        before={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in folder.iterdir() if p.is_file()}
        with patch.object(module,'datetime',FixedDateTime),patch.object(module.uuid,'uuid4',side_effect=[collision,next_id]) as retries:
            b=execute('T23_retry',['r2'],'Collision',ROOT/'T23');self.assert_render_ok(b,1)
            self.assertEqual(retries.call_count,2)
        with patch.object(module,'datetime',FixedDateTime),patch.object(module.uuid,'uuid4',return_value=collision) as exhausted:
            c=execute('T23_exhausted',['r2'],'Collision',ROOT/'T23')
            self.assertIsNone(c['escaped']);self.assertFalse(c['progress_active'])
            self.assertEqual(c['status'],'Erreur');self.assertEqual(exhausted.call_count,5)
            self.assertEqual(c['run_dirs'],[])
        after={p:hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in before}
        self.assertEqual(before,after)
        EVIDENCE['T23']={'retry_count':2,'exhausted_attempts':5,'first_generation_preserved':True,
                         'before':before,'after':after}

    def test_T24_form_edits_keep_metadata_consistent(self):
        def change_form(x,cmd):
            x.event.set('Autre événement');x.sponsor.set('Autre partenaire')
        r=execute('T24',['r1'],'Événement initial',hook=change_form);self.assert_render_ok(r,1)
        self.assertEqual(r['publication'].splitlines()[0],
                         'Titre proposé : '+r['report']['event']+' | Les Sentinelles')
        self.assertIn(r['report']['sponsors'],r['publication'])

    def test_T25_preflight_guards(self):
        x=runner(ROOT/'T25',[]);messages=[]
        with patch.object(module.messagebox,'showwarning',side_effect=lambda *a:messages.append(a)):
            App.run_thread(x)
        self.assertEqual(len(messages),1)
        x.files=[str(FILES['r1'])];messages=[]
        with patch.object(module.shutil,'which',return_value=None),patch.object(module.messagebox,'showerror',side_effect=lambda *a:messages.append(a)):
            App.run_thread(x)
        self.assertEqual(len(messages),1)
        EVIDENCE['T25']={'empty_selection':'warning','missing_ffmpeg':'error'}

    def test_T26_pick_deduplicates_real_path_symlink_and_hardlink(self):
        items=[]
        x=SimpleNamespace(files=[],source_id=App.source_id,list=SimpleNamespace(insert=lambda pos,f:items.append(f)))
        paths=[str(FILES[k]) for k in ['r1','r1','alias','hardlink','r2']]
        with patch.object(module.filedialog,'askopenfilenames',return_value=paths):App.pick(x)
        self.assertEqual(x.files,[paths[0],paths[-1]]);self.assertEqual(items,x.files)
        EVIDENCE['T26']={'unique_imports':x.files,'aliases_ignored':3}

    def test_T27_launcher_observation(self):
        script=REPO/'app/run_linux_mac.sh'
        with self.assertRaises(PermissionError):
            REAL_RUN([str(script)],cwd=REPO/'app',capture_output=True,text=True)
        from_root=REAL_RUN(['sh','app/run_linux_mac.sh'],cwd=REPO,capture_output=True,text=True)
        self.assertEqual(from_root.returncode,2);self.assertIn('app.py',from_root.stderr)
        EVIDENCE['T27']={'mode':oct(script.stat().st_mode&0o777),'direct_execution':'PermissionError',
                         'from_repo_root_exit':from_root.returncode,'from_repo_root_stderr':from_root.stderr}

    def test_T28_two_starts_thread_observation(self):
        x=runner(ROOT/'T28',['r1']);x.process=lambda:None;starts=[]
        class FakeThread:
            def __init__(self,**kwargs):pass
            def start(self):starts.append('started')
        with patch.object(module.threading,'Thread',FakeThread):
            App.run_thread(x);App.run_thread(x)
        self.assertEqual(len(starts),2)
        EVIDENCE['T28']={'two_requests_start_two_workers':True,'actual_Tk_concurrency':'not tested'}

    def test_T29_mp4_video_2s_audio_60s(self):
        r=execute('T29',['long_audio']);EVIDENCE['T29']['input_probe']=probe(FILES['long_audio'])
        self.assert_render_ok(r,1)
        self.assertEqual(r['report']['sources'][0]['duration'],2)
        self.assertEqual(r['report']['exports'][0]['start'],0)
        v=next(s for s in r['outputs'][0]['probe']['streams'] if s['codec_type']=='video')
        self.assertAlmostEqual(float(v['duration']),2,places=2)

    def test_T30_same_physical_source_alias_no_duplicate(self):
        r=execute('T30',['r1','alias','hardlink']);self.assert_render_ok(r,1)
        self.assertTrue(os.path.samefile(FILES['r1'],FILES['alias']))
        self.assertEqual(len(r['report']['sources']),3)
        self.assertEqual(len({s['source_id'] for s in r['report']['sources']}),1)
        self.assertTrue(all(s.get('error') for s in r['report']['sources'][1:]))

    def test_T31_long_physical_source_alias_temporal_gap(self):
        r=execute('T31',['long1','long_alias']);self.assert_render_ok(r,3)
        self.assertEqual([e['start'] for e in r['report']['exports']],[3,15,27])
        self.assertEqual(len({e['source_id'] for e in r['report']['exports']}),1)

    def test_T32_zero_byte_successful_process_is_rejected(self):
        def zero(x,cmd):Path(cmd[-1]).write_bytes(b'')
        r=execute('T32',['r1'],hook=zero);self.assert_no_output(r)
        self.assertEqual(r['outputs'],[])
        self.assertEqual(r['report']['errors'][0]['stage'],'export')

    def test_T33_wrong_dimensions_rejected_and_later_export_continues(self):
        def wrong(x,cmd):
            if cmd[-1].endswith('short_02_9x16.mp4'):shutil.copyfile(FILES['r2'],cmd[-1])
        r=execute('T33',['r1','r2','r3'],hook=wrong);self.assert_render_ok(r,2)
        self.assertEqual(len(r['report']['errors']),1)
        self.assertEqual(r['report']['errors'][0]['error'],'Dimensions export invalides')

    def test_T34_audio_only_export_rejected(self):
        def audio(x,cmd):shutil.copyfile(FILES['audio_only'],cmd[-1])
        r=execute('T34',['r1'],hook=audio);self.assert_no_output(r)
        self.assertEqual(r['report']['errors'][0]['error'],'Export sans flux vidéo')

    def test_T35_nonzero_invalid_export_rejected(self):
        def invalid(x,cmd):Path(cmd[-1]).write_bytes(b'nonzero invalid media file')
        r=execute('T35',['r1'],hook=invalid);self.assert_no_output(r)
        self.assertGreater(r['outputs'][0]['bytes'],0)
        self.assertIn('probe_error',r['outputs'][0])

    def test_T36_mkv_video_duration_must_ignore_long_audio(self):
        r=execute('T36',['long_audio_mkv'])
        EVIDENCE['T36']['input_probe']=probe(FILES['long_audio_mkv'])
        packets=json.loads(REAL_CHECK(['ffprobe','-v','error','-select_streams','v:0','-show_packets',
                                       '-show_entries','packet=pts_time,duration_time','-of','json',
                                       str(FILES['long_audio_mkv'])],text=True))['packets']
        EVIDENCE['T36']['video_packets']=packets
        self.assert_finished(r)
        self.assertLessEqual(r['report']['sources'][0]['duration'],2.1,
                             'Selection uses the 60-second container rather than the 2-second video')
        self.assert_render_ok(r,1)

    def test_T37_corrupt_video_payload_must_not_be_status_ok(self):
        packet_records=[]
        def corrupt(x,cmd):packet_records.extend(corrupt_packets(Path(cmd[-1])))
        r=execute('T37',['r1'],hook=corrupt)
        EVIDENCE['T37']['injected_corruption']={'method':'zero video packet payloads, retain MP4 structure',
                                               'packets':packet_records}
        self.assert_finished(r)
        self.assertNotEqual(r['outputs'][0]['decode'],{'returncode':0,'stderr':''})
        self.assertEqual(r['report']['exports'],[],
                         'Corrupted H.264 is marked status: ok despite full-decoder errors')

    def test_T38_publication_write_failure_keeps_report_and_valid_exports(self):
        r=execute('T38',['r1'],publication_failure=True);self.assert_finished(r)
        self.assertEqual(r['report']['status'],'failed');self.assertEqual(r['status'],'Erreur')
        self.assertEqual(len(r['report']['exports']),1)
        self.assertEqual(r['report']['errors'][-1]['stage'],'run')
        self.assertIsNone(r['publication'])
        self.assertEqual(r['outputs'][0]['decode'],{'returncode':0,'stderr':''})

    def test_T39_missing_source_and_audio_only_do_not_block_valid_source(self):
        r=execute('T39',['r1','missing','audio_only']);self.assert_render_ok(r,1)
        self.assertEqual(len(r['report']['sources']),3)
        self.assertEqual(len(r['report']['errors']),2)
        self.assertTrue(all(e['stage']=='probe' for e in r['report']['errors']))

    def test_T40_silent_mp4_and_silent_mkv(self):
        for name in ['r1','silent_mkv']:
            r=execute('T40_'+name,[name]);self.assert_render_ok(r,1)
            self.assertFalse(any(s['codec_type']=='audio' for s in r['outputs'][0]['probe']['streams']))
        EVIDENCE['T40']={'silent_sources':['mp4','mkv'],'valid_video_exports':2}

    def test_T41_all_exports_fail_still_report_and_no_success(self):
        def invalid(x,cmd):Path(cmd[-1]).write_bytes(b'')
        r=execute('T41',['r1','r2','r3'],hook=invalid);self.assert_no_output(r)
        self.assertEqual(len(r['commands']),3);self.assertEqual(len(r['report']['sources']),3)
        self.assertEqual(len(r['report']['errors']),3)
        self.assertEqual(r['outputs'],[])

    def test_T42_thread_ui_call_sites_observation(self):
        calls=[]
        x=runner(ROOT/'T42',['r1'])
        ident=module.threading.get_ident()
        class TracedValue(Value):
            def get(self):
                calls.append({'method':'StringVar.get double','thread':module.threading.get_ident()})
                return super().get()
            def set(self,v):
                calls.append({'method':'StringVar.set double','thread':module.threading.get_ident()})
                return super().set(v)
        class TracedProgress(Progress):
            def start(self,n):
                calls.append({'method':'Progressbar.start double','thread':module.threading.get_ident()})
                return super().start(n)
            def stop(self):
                calls.append({'method':'Progressbar.stop double','thread':module.threading.get_ident()})
                return super().stop()
        x.event=TracedValue('Threads');x.sponsor=TracedValue('Partenaire');x.status=TracedValue('Prêt')
        x.progress=TracedProgress()
        x.files=[str(FILES['half_second'])]
        def dialog(*args):calls.append({'method':'messagebox double','thread':module.threading.get_ident()})
        with patch.object(module.messagebox,'showwarning',side_effect=dialog):
            t=module.threading.Thread(target=lambda:App.process(x))
            t.start();t.join(timeout=10)
        self.assertFalse(t.is_alive());self.assertFalse(x.progress.active)
        self.assertTrue(any(c['thread']!=ident for c in calls))
        EVIDENCE['T42']={'main_thread':ident,'calls':calls,
                         'actual_Tk_widgets':'not tested; no DISPLAY/Xvfb',
                         'conclusion':'original process calls UI interfaces from worker thread'}

    def test_T99_global_report_and_decode_checks(self):
        checks=[];missing=[];bad_ok=[]
        for test_id,r in list(EVIDENCE.items()):
            for item in r.get('reports',[]):
                if not item['exists']:missing.append({'test':test_id,**item})
            ok={e['file'] for e in (r.get('report') or {}).get('exports',[]) if e.get('status')=='ok'}
            for item in r.get('outputs',[]):
                record={'test':test_id,'file':item['file'],'bytes':item['bytes'],
                        'probe':item.get('probe'),'probe_error':item.get('probe_error'),
                        'decode':item['decode'],'recorded_ok':item['file'] in ok}
                checks.append(record)
                v=next((s for s in item.get('probe',{}).get('streams',[]) if s['codec_type']=='video'),None)
                if record['recorded_ok'] and (not v or (v.get('width'),v.get('height'))!=(1080,1920)
                                            or item['bytes']==0 or item['decode']!={'returncode':0,'stderr':''}):
                    bad_ok.append(record)
        EVIDENCE['T99']={'checked_outputs':len(checks),'checks':checks,'missing_reports':missing,
                         'invalid_status_ok':bad_ok}
        self.assertGreater(len(checks),0);self.assertEqual(missing,[])
        self.assertEqual(bad_ok,[],'At least one invalid export is registered status: ok')

started=time.monotonic()
suite=unittest.defaultTestLoader.loadTestsFromTestCase(AuditTests)
result=unittest.TextTestRunner(verbosity=2).run(suite)
after={str(p.relative_to(REPO)):hashlib.sha256(p.read_bytes()).hexdigest()
       for p in (REPO/'app').rglob('*') if p.is_file()}
integrity={'unchanged':APP_BEFORE==after,'before':APP_BEFORE,'after':after}
summary={'environment':{'python':sys.version,'platform':platform.platform(),
                        'tk':module.tk.TkVersion,'tcl':module.tk.TclVersion,'display':os.environ.get('DISPLAY'),
                        'ffmpeg':REAL_CHECK(['ffmpeg','-version'],text=True).splitlines()[0],
                        'ffprobe':REAL_CHECK(['ffprobe','-version'],text=True).splitlines()[0]},
         'elapsed_seconds':time.monotonic()-started,'tests_run':result.testsRun,
         'failures':[{'test':t.id(),'traceback':trace} for t,trace in result.failures],
         'errors':[{'test':t.id(),'traceback':trace} for t,trace in result.errors],
         'app_integrity':integrity,'evidence':EVIDENCE}
(ROOT/'evidence.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print('EVIDENCE',ROOT/'evidence.json')
print('APPLICATION FILES UNCHANGED',integrity['unchanged'])
if not integrity['unchanged']:raise RuntimeError('Application changed during audit')
sys.exit(0 if result.wasSuccessful() else 1)

```

**Code de `confirm_v03.py`**

```python
"""Focused confirmations on the exact immutable app.py, separate from unittest harness."""
import hashlib,importlib.util,json,os,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
repo=Path(sys.argv[1]).resolve();root=Path(sys.argv[2]).resolve()
spec=importlib.util.spec_from_file_location('v03_confirmed_app',repo/'app/app.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
data=json.loads((root/'evidence.json').read_text())['evidence']
def probe(path):
    result=subprocess.run(['ffprobe','-v','error','-show_entries',
                           'stream=codec_type,width,height,duration:format=duration','-of','json',str(path)],
                          capture_output=True,text=True)
    return {'returncode':result.returncode,'data':json.loads(result.stdout),'stderr':result.stderr}
def decode(path):
    p=subprocess.run(['ffmpeg','-v','error','-i',str(path),'-f','null','-'],
                     stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,text=True)
    return {'returncode':p.returncode,'stderr':p.stderr}
before={str(p.relative_to(repo)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (repo/'app').rglob('*') if p.is_file()}
runs=sorted(p for p in root.rglob('run_*') if p.is_dir())
c1={'id':'C01','run_count':len(runs),'missing_reports':[str(p) for p in runs if not (p/'rapport.json').is_file()]}
assert c1['missing_reports']==[]
c1['parsed_reports']=len([json.loads((p/'rapport.json').read_text()) for p in runs])
control=root/'controls';control.mkdir(exist_ok=True)
source=Path(data['T36']['inputs'][0])
cmd=data['T36']['commands'][0].copy()
cmd[cmd.index('-ss')+1]='0';cmd[cmd.index('-t')+1]='2';cmd[-1]=str(control/'mkv_at_actual_video_start.mp4')
render=subprocess.run(cmd,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,text=True)
c2={'id':'C02','original_probe_source':m.App.probe_source(source),'input_decode':decode(source),
    'control_command':cmd,'control_render_returncode':render.returncode,'control_probe':probe(cmd[-1]),'control_decode':decode(cmd[-1])}
assert render.returncode==0 and c2['input_decode']=={'returncode':0,'stderr':''}
assert c2['control_decode']=={'returncode':0,'stderr':''}
assert any(s['codec_type']=='video' and (s['width'],s['height'])==(1080,1920) for s in c2['control_probe']['data']['streams'])
path=Path(data['T37']['outputs'][0]['file'])
c3={'id':'C03','path':str(path),'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
    'original_verify_export_return':m.App.verify_export(path),'independent_probe':probe(path),'independent_decode':decode(path)}
assert c3['original_verify_export_return'] is True and c3['independent_decode']['returncode']!=0
after={str(p.relative_to(repo)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (repo/'app').rglob('*') if p.is_file()}
assert before==after
out={'confirmations':[c1,c2,c3],'app_unchanged':before==after}
(root/'confirmations.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
print(json.dumps(out,ensure_ascii=False,indent=2))

```

