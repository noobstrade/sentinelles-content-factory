# Audit indépendant — Sentinelles Content Factory MVP 0.4

**Verdict final : BLOQUÉ.**

Les trois blocages du MVP 0.3 sont levés dans les scénarios rejoués : durée vidéo du MKV, rejet du H.264 indécodable et cohérence du snapshot événement/partenaire. Les 43 tests de régression passent. Un défaut supplémentaire, **MAJ-08**, contrevient au contrôle demandé de libération du verrou après erreur : un échec de démarrage du thread laisse `processing=True` sans génération active ; la demande suivante est refusée. Cet échec est injecté explicitement, sans prétendre qu’une saturation réelle du système a été observée.

**Cible et intégrité**

- Dépôt : [noobstrade/sentinelles-content-factory](https://github.com/noobstrade/sentinelles-content-factory).
- Branche : `develop`.
- Commit audité : [`351aff8f7679dbce7029533a43f72ccfe05e5704`](https://github.com/noobstrade/sentinelles-content-factory/commit/351aff8f7679dbce7029533a43f72ccfe05e5704).
- Date : 7 octobre 2026, UTC.
- Arbre racine : `a24b864890b5e6ffaaef0a7bf929f6bdf53cfc1c`.
- Arbre `app/` : `4f9b3fdb1b2f5796d269e13f7ea8e08f9817b5ab`.
- Blob de `app/app.py` : `8b96e2bbd3c42e25c251361e8c8e8075d0509d28`.
- Lectures intégrales : mandat MVP 0.4 `worker/A_AUDITER.md`, `docs/PRODUCT_SPEC.md`, `docs/AUDIT_BASELINE.md`, `docs/WORKFLOW.md`, puis les six fichiers de `app/`. Le rapport MVP 0.3 de `ed46ee188ef1070f55538a99db96c7d5d886ec31` est inchangé dans ce snapshot et ses 43 scénarios sont conservés. Aucun `AGENTS.md` dans le dépôt.
- Snapshot des 12 blobs vérifié par taille et SHA Git. Aucun fichier de l’application modifié, aucun cache Python créé dans `app/` ; contrôle SHA-256 avant/après la suite et les confirmations.
- Seul livrable à commiter : `worker/RESULTAT_AUDIT.md` sur `develop`. Aucun correctif appliqué et aucun passage sur `main`.

**Campagne et méthode**

**48 tests : 43 régressions rejouées et 5 contrôles supplémentaires. Résultat final : 47 réussis, 1 échec (T45), aucune erreur de harnais.** Durée unittest : 62,285 s. La grille T02 comporte **66 429 configurations**, sans violation, et la grille T03 ajoute **120 configurations avec alias et sources en erreur**.

Environnement : Python 3.12.14, Linux x86_64 / noyau 6.18.44 / glibc 2.39, Tk/Tcl 9.0, FFmpeg et ffprobe 6.1.1-3ubuntu5. Les méthodes originales du commit sont chargées sans réécriture. Fixtures vidéo et audio, probing, rendus et décodages sont réels. Les chemins, dimensions, durées, codes de retour, JSON, textes et hashes sont contrôlés.

Le harnais du précédent rapport est adapté à `process(snapshot)`, au schéma 0.4 et au nouveau décodage FFmpeg interne. Il distingue les commandes d’encodage des commandes de vérification : seules les premières déclenchent les injections et le compteur des exports. Le test T46 compte deux départs et deux arrêts de progression, puisqu’il exécute deux générations. **Seule l’exécution finale dans `execution_v04_final` sert aux chiffres et au verdict ci-dessous** ; les premiers essais d’adaptation du harnais sont exclus.

Les erreurs d’export, d’écriture et de démarrage de thread, les collisions horloge/UUID et la corruption des payloads après rendu sont des injections documentées. Elles contrôlent les branches d’erreur et les garde-fous. Le MP4 corrompu en entrée, le chemin absent, les sources sans audio et les cas MKV sont des fichiers réels traités par le pipeline original.

Les variables/progression/messagebox de la campagne moteur utilisent des doubles. T43 et T46 lancent de vrais threads Python ; C05 emploie la véritable classe `threading.Thread` avec son `start` en échec injecté et de vraies `tk.StringVar` sur un interpréteur Tcl. Les widgets graphiques Tk ne sont pas exercés : aucun `DISPLAY` ni Xvfb dans l’environnement. Cette limite ne constitue pas un défaut reproduit de l’application et la sûreté graphique reste non validée.

**Preuves transversales indépendantes**

| Confirmation | Preuve et résultat |
|---|---|
| C01 | Lecture des **51 dossiers run** et parsing de leurs **51 rapports JSON**. Extraction de **58 entrées réellement marquées ok**, y compris l’export valide de la première génération T46 dont le statut global est failed. Contrôle individuel ffprobe et décodage intégral de tous les flux : **58 vidéos 1080×1920, 58 codes 0, 58 stderr vides**. |
| C02 | Appel original `probe_source` sur le MKV : fin vidéo **2,023 s**, identique au maximum indépendant des PTS + durées de ses quatre paquets vidéo. Conteneur : **60,023 s**. Le pipeline produit un vrai Short, start 0, images de 2 s ; source et export se décodent. |
| C03 | Le même type de H.264 corrompu que T37 reste probe-able en 1080×1920 mais échoue au décodage (code 69). `verify_export` original lève désormais `ValueError: Décodage vidéo de contrôle échoué` ; aucune entrée ok. |
| C04 | Lecture croisée de T44 : malgré des changements de nom, partenaire, liste de rushs et destination avant le lancement effectif du worker, dossier/JSON/texte/sources utilisent le snapshot initial. |
| C05 | Confirmation séparée de MAJ-08 avec la vraie classe Thread et des variables Tcl réelles : `RuntimeError` à start, `processing=True` après l’erreur, puis warning `Traitement en cours` au nouvel appel ; aucun worker démarré. |
| C06 | AAC corrompu après rendu : rejet par le vérificateur original, erreur export enregistrée, aucune entrée ok. Le décodage complet indépendant échoue également. Aucune généralisation à toutes les formes possibles de corruption audio. |

Les **63 fichiers MP4 laissés par le pipeline** sont contrôlés par ffprobe et décodage complet dans la campagne, y compris les sorties rejetées. Les cinq fichiers exclus sont : mauvais format 320×180, audio-only, texte invalide, H.264 corrompu et AAC corrompu. Les fichiers de zéro octet ont été supprimés. Aucun fichier invalide n’est déclaré `ok` dans cette exécution. Le scan indépendant C01 assure la couverture des deux rapports de T46, au-delà du dernier rapport exposé par le helper de campagne.

**Statut des constats précédents et des durcissements demandés**

| Point à contrôler | Tests / confirmations | Conclusion limitée aux preuves obtenues |
|---|---|---|
| MAJ-01 résiduel / MKV vidéo ~2 s et audio ~60 s | T36, C02 ; MP4 T29 | **Corrigé dans les cas testés** : sélection sur la timeline vidéo 2,023 s en MKV, 2 s en MP4 ; un export vidéo exploitable dans chacun. |
| MAJ-06 / H.264 probe-able mais indécodable | T37, T99, C03 | **Corrigé dans ce scénario** : corruption rejetée, erreur persistée, zéro export ok ; warning sans Short prêt. |
| MAJ-07 / modification événement/partenaire pendant le rendu | T24, T44, C04 | **Corrigé dans les scénarios testés** : valeurs initiales cohérentes dans dossier, JSON et texte ; fichiers et destination également figés par snapshot. |
| Second run_thread durant une génération | T28, T43 | **Refus démontré** : un seul worker, un warning ; T43 maintient un vrai worker à une barrière pendant le second appel. |
| Verrou libéré après succès | T43 et contrôles processing dans les rendus | **Démontré** pour les générations terminées : processing false, attributs de snapshot nettoyés, progression arrêtée. |
| Verrou libéré après erreur dans le worker | T21, T23, T38, T46 | **Démontré** pour ces erreurs : dans T46, échec d’écriture puis lancement suivant autorisé et réussi, deux arrêts de progression. |
| Verrou libéré après erreur de démarrage du worker | T45, C05 | **NON CONFORME — MAJ-08** : erreur échappée, processing reste true, aucune génération active, appel suivant refusé. |
| Multi-rush, toutes sources inventoriées, suite après source absente/corrompue | T04–T06, T19, T20, T39 | Non-régression confirmée ; erreurs par source/export conservées et autres rushs exploités. Maximum 3 exports par run. |
| Déduplication temporelle et alias | T02, T03, T07–T10, T26, T30, T31 | Non-régression confirmée : seuil minimal 12 s par source_id, symlink/hardlink reconnus sur Linux. |
| Generations successives et collisions | T11, T23 | Non-régression confirmée : dossiers distincts, précédente génération intacte, retry/épuisement gérés. |
| Portrait 80×160, 9:16, carré, paysage, source silencieuse MP4/MKV | T04, T15, T16, T18, T40 | Vidéo 1080×1920 décodable dans chaque cas ; absence d’audio acceptée. |
| Zéro export et sorties invalides | T14, T32–T35, T37, T41, T47 | Pas d’annonce de Shorts prêts lorsque zéro export ; rejet des sorties invalides testées, zéro octet supprimé, rapport conservé. |
| Rapport après création d’un run | T19, T20, T38, T41, T46, C01 | 51/51 rapports présents et parseables dans cette campagne, y compris les runs échoués. Aucun nouveau run lors de T21, collision épuisée de T23 ou démarrage échoué de T45. |

La déduplication est temporelle, pas sémantique : à 48 s, starts 3/15/27 et extraits de 18 s se chevauchent de 6 s, conformément au seuil demandé de 12 s entre débuts. Détection de copies de contenu sous des inodes différents non démontrée.

**Grille complète de la campagne**

| Test | Scénario | Résultat observé |
|---|---|---|
| T01 | Syntaxe AST et import original | OK — syntaxe/import du commit exact, APP_NAME = MVP 0.4. |
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
| T24 | Modification événement/partenaire après FFmpeg, avant les textes | OK — texte, JSON et dossier restent Événement initial / Partenaire test après modification du formulaire pendant le rendu. |
| T25 | Précontrôles sans fichiers et FFmpeg absent | OK — warning et error respectivement, sans lancement de traitement. |
| T26 | Import réel + doublon de chemin + symlink + hardlink | OK — deux imports uniques sur cinq chemins ; trois alias ignorés. |
| T27 | Lanceur Linux/macOS direct et depuis la racine | OBSERVATION CONFIRMÉE — mode 0644 : PermissionError ; sh app/run_linux_mac.sh depuis la racine : code 2 ; MIN-02. Le test réussit en vérifiant ces défauts. |
| T28 | Deux demandes run_thread avec double de Thread | OK — un seul worker simulé en attente ; second appel refusé avec warning Traitement en cours. |
| T29 | MP4 : vidéo 2 s, audio 60 s | OK — durée sélectionnée 2 s, start 0, un export vidéo+audio de 2 s ; aucun faux succès audio-only. |
| T30 | Même rush court par chemin réel, symlink et hardlink | OK — 3 chemins inventoriés, 1 source_id, 1 export ; alias identifiés. |
| T31 | Rush de 48 s et son symlink | OK — 1 identité, starts 3/15/27 s ; pas de répétition du même intervalle sous deux chemins. |
| T32 | FFmpeg réussi, sortie tronquée à 0 octet avant vérification | OK — fichier rejeté et supprimé, zéro status: ok, JSON présent, warning. |
| T33 | Sortie 2 remplacée par un MP4 valide de mauvaises dimensions | OK — rejet 320×180, erreur Dimensions export invalides ; exports 1 et 3 maintenus. |
| T34 | Sortie remplacée par un MP4 audio-only | OK — rejet Export sans flux vidéo ; aucune entrée ok. |
| T35 | Sortie non nulle remplacée par du texte invalide | OK — échec ffprobe, aucune entrée ok ; erreur export enregistrée. |
| T36 | Même vidéo 2 s/audio 60 s remuxée en MKV | OK — fin vidéo 2,023 s au lieu du conteneur 60,023 s ; start 0, un Short vidéo de 2 s décodable. |
| T37 | Payloads H.264 corrompus après rendu, structure MP4 conservée | OK — fichier H.264 probe-able 1080×1920 mais décodage code 69 ; rejet avec erreur Décodage vidéo de contrôle échoué, aucun export ok. |
| T38 | Échec injecté lors de l’écriture du texte de publication | OK — status failed, JSON de secours et export valide conservés ; progression arrêtée et processing libéré. |
| T39 | Rush valide, chemin absent et source audio-only | OK — 1 export valide, 3 sources inventoriées, 2 erreurs probe ; poursuite du traitement. |
| T40 | Sources sans audio, MP4 et MKV | OK — un export vidéo sans audio pour chaque source. |
| T41 | Trois sorties de 0 octet après trois encodages réussis | OK — trois tentatives, trois erreurs, zéro export ok, rapport conservé, warning. |
| T42 | process original dans un vrai thread avec doubles d’UI tracés | OBSERVATION — vrai thread Python ; interfaces d’UI appelées depuis le worker avec doubles ; processing libéré ; widgets Tk réels non testés. |
| T43 | Second run_thread pendant un vrai worker arrêté à une barrière de rendu | OK — processing actif à la barrière, un seul worker créé, second appel refusé, puis succès et processing false. |
| T44 | Snapshot initial puis édition événement/partenaire/rushs/destination avant exécution | OK — dossier/JSON/texte/source/destination restent ceux du snapshot initial. Destination modifiée non créée. |
| T45 | Échec injecté de Thread.start avant le démarrage effectif | ÉCHEC — RuntimeError échappée ; processing reste true sans génération ; MAJ-08, confirmé par C05. |
| T46 | Vrai worker en erreur d’écriture puis nouvelle génération réussie | OK — deux workers successifs, verrou libéré après chaque run ; status Erreur puis Terminé ; deux JSON et deux exports valides conservés. |
| T47 | Payloads AAC corrompus après encodage, vidéo conservée | OK — rejet avec Décodage vidéo de contrôle échoué ; décodage intégral code 69 ; aucune entrée ok. |
| T99 | Contrôle transversal de tous les fichiers MP4 produits | OK — 63 fichiers MP4 probés/décodés ; zéro fichier invalide marqué ok. C01 complète le comptage des deux rapports de T46 et confirme 58 exports ok valides. |

**Défauts critiques**

Aucun défaut critique reproduit dans le périmètre exécuté.

**Défaut majeur ouvert : MAJ-08 — le verrou survit à une erreur de démarrage du thread**

Localisation : `app/app.py`, lignes **49–57**, particulièrement acquisition du verrou ligne **55** et lancement ligne **57**. La libération ligne **202** n’est exécutée que si `process()` a effectivement démarré. Preuves : **T45 et C05**.

Reproduction déterministe :

1. Préparer une sélection valide, FFmpeg/ffprobe disponibles, `processing=False`.
2. Injecter `RuntimeError("audit injection: can't start new thread")` dans `Thread.start()`.
3. Appeler la méthode originale `App.run_thread()`.
4. Examiner l’exception, le booléen et le nombre de workers ; appeler de nouveau `run_thread()` après retrait de l’injection.

Résultat : le premier appel laisse échapper `RuntimeError` après avoir affecté `processing=True`. Aucun worker et aucun run_dir n’ont été créés. Le booléen reste actif. Le second appel produit uniquement `Traitement en cours / Une génération est déjà en cours.`, alors qu’aucune génération ne travaille.

Extrait de la confirmation indépendante :

```json
{
  "thread_start_calls": 1,
  "escaped": {
    "type": "RuntimeError",
    "message": "audit injection: can't start new thread"
  },
  "processing_after_error": true,
  "warnings_on_next_request": [
    ["Traitement en cours", "Une génération est déjà en cours."]
  ]
}
```

Attendu, selon le mandat : libérer le verrou après erreur et permettre un nouveau lancement. Une erreur de démarrage doit être signalée sans laisser un état « traitement en cours » permanent. Le `finally` du worker ne peut pas assurer cette libération si ce worker n’a jamais démarré.

Impact : après une erreur de lancement, toutes les demandes suivantes restent bloquées dans la même instance ; l’interface ne prévoit aucun reset de processing. **Aucune perte de données ni saturation spontanée n’a été observée.** La gravité retenue est majeure car ce chemin échoue au contrôle explicite de libération du verrou et rend toute nouvelle génération impossible sans recréer l’instance.

Condition de levée : prendre en charge l’échec de construction/démarrage et remettre l’état à disponible lorsque le worker n’a pas démarré. Rejouer T45/C05 pour obtenir aucun échappement non géré, processing false, puis une génération effectivement autorisée. Conserver T43 (second appel refusé pendant le run) et T46 (verrou libéré après erreur interne puis succès). Aucun correctif réalisé par cet audit.

**Mineurs et limites toujours ouverts**

- **MIN-02 : lanceur Linux non exécutable et dépendant du répertoire courant.** T27 reproduit mode 0644, PermissionError en exécution directe, code 2 de `sh app/run_linux_mac.sh` depuis la racine. Le README indique une alternative en lançant `python app.py` depuis `app/`. Le comportement macOS n’a pas été exécuté.
- **MIN-03 : documentation de version décalée.** `app/README.md` affiche toujours MVP 0.2, alors que T01 vérifie APP_NAME MVP 0.4. La roadmap reste un plan ; aucune séparation moteur/UI ni suite de tests livrée dans `app/` n’est démontrée. Preuves : lecture intégrale et arbre Git exact.
- Les erreurs partielles T19/T20 restent visibles dans `rapport.json` ; le message final d’UI simulée annonce le nombre de sorties sans récapitulatif de ces erreurs. Ce constat ne retire pas la traçabilité et la poursuite prouvées.
- **Tk/thread : sûreté des widgets réels non validée.** T42 trace encore, dans un vrai thread Python avec doubles, les interfaces de variables, progression et messagebox depuis le worker. `process` effectue aussi des appels d’UI avant son try (lignes 143–150). Aucun crash Tk ni absence de crash Tk n’est déclaré reproduit. Windows/macOS, double lancement avec widgets réels et fermeture de fenêtre en cours de rendu restent à exercer dans une session graphique.

**Fonctions hors périmètre et portée produit**

Le moteur reste une sélection à fractions temporelles fixes 25/50/75 %, avec recadrage central et bandeau fixe. Import multiple, provenance, exports locaux versionnés et texte social générique sont constatés. La liste des partenaires alimente le texte ; aucun Sponsor Manager n’est présent.

Toujours absents et non déclarés présents : transcription/sous-titres, scoring hockey intelligent, sélection multimodale, suivi intelligent 9:16, Sponsor Manager, reporting partenaire. Des dépendances déclarées dans requirements ne prouvent pas une intégration. Le rappel de validation humaine ne démontre pas un circuit éditorial complet. Aucune audience, pertinence hockey, qualité de cadrage d’un match réel ou économie de temps bénévole mesurée par cette campagne.

**Décision finale**

**BLOQUÉ** sur `351aff8f7679dbce7029533a43f72ccfe05e5704` pour **MAJ-08**, malgré les trois anciens blocages désormais levés dans les cas testés et les 58 exports ok décodables. La condition demandée « verrou libéré après erreur » n’est pas remplie au démarrage. Ce verdict ne suppose pas un crash graphique non reproduit. Après correction et retest, la candidature du moteur pourra être réévaluée ; la sûreté de l’UI devra faire l’objet d’essais graphiques séparés. Aucun changement de `main`.

**Annexe — contrôle individuel de toutes les sorties laissées**

« ok » désigne la valeur réellement enregistrée dans un rapport JSON, retrouvée par C01. Les 63 fichiers ont été probés et décodés intégralement. Les deux générations T46 sont distinguées par leur statut global : l’export valide du run failed est bien marqué ok et contrôlé.

| Test/run | Fichier | Octets | Vidéo selon ffprobe | Durée vidéo (s) | Décodage FFmpeg | Statut export |
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
| T36 | short_01_9x16.mp4 | 99569 | 1080×1920 | 2.000000 | 0 / stderr vide | ok |
| T37 | short_01_9x16.mp4 | 69596 | 1080×1920 | 2.000000 | 69 / erreurs | exclu |
| T38 | short_01_9x16.mp4 | 69596 | 1080×1920 | 2.000000 | 0 / stderr vide | ok |
| T39 | short_01_9x16.mp4 | 69596 | 1080×1920 | 2.000000 | 0 / stderr vide | ok |
| T40_r1 | short_01_9x16.mp4 | 69596 | 1080×1920 | 2.000000 | 0 / stderr vide | ok |
| T40_silent_mkv | short_01_9x16.mp4 | 69596 | 1080×1920 | 2.000000 | 0 / stderr vide | ok |
| T43 | short_01_9x16.mp4 | 69596 | 1080×1920 | 2.000000 | 0 / stderr vide | ok |
| T44 | short_01_9x16.mp4 | 69596 | 1080×1920 | 2.000000 | 0 / stderr vide | ok |
| T46 (failed) | short_01_9x16.mp4 | 69596 | 1080×1920 | 2.000000 | 0 / stderr vide | ok |
| T46 (completed) | short_01_9x16.mp4 | 69596 | 1080×1920 | 2.000000 | 0 / stderr vide | ok |
| T47 | short_01_9x16.mp4 | 99151 | 1080×1920 | 2.000000 | 69 / erreurs | exclu |

Les sorties invalides non nulles sont conservées sur disque mais exclues des exports ok et reliées à une erreur du JSON. Les fichiers à zéro octet de T19/T32/T41 sont supprimés.

**Annexe — empreintes de l’application**

Même inventaire, mêmes octets avant/après ; aucune écriture dans `app/`.

| Fichier | SHA-256 identique avant/après |
|---|---|
| app/README.md | `9a6fd2e07bfa16230b0ecb425d83dde33e91024a0573a3e8cc10a168a1952412` |
| app/ROADMAP.md | `e98b00f8ec9dc508fb675f01aa96bef1a86f181c465e8b760e66cae4e0fcd25b` |
| app/app.py | `60b24e8bd0f6769114e0805c5870188a4c275270a6f315416892f0635191b617` |
| app/requirements.txt | `be654442659daf5deace60880d5b13bda39c702793ff78a0e6ea2ddd2e7ef64b` |
| app/run_linux_mac.sh | `1a1032a1498d3370155a0ff2952d26bfcc88a68cad53c9f1a473189e5f8fca16` |
| app/run_windows.bat | `92f53ecbc23b49cf50624c8de78dc5dbbb119237c1ac45fc03e0ff2dd3e76f5e` |

**Annexe — reproduction autonome**

Copier les deux blocs Python dans `/tmp/audit_v04.py` et `/tmp/confirm_v04.py`. Les exécuter hors du dépôt avec un répertoire de résultats neuf. Les identités inode, timestamps et hashes d’encodage peuvent varier selon les machines ; dimensions, statuts, erreurs et décodages constituent les critères reproductibles.

```sh
git clone --branch develop https://github.com/noobstrade/sentinelles-content-factory.git /tmp/sentinelles-mvp04
git -C /tmp/sentinelles-mvp04 checkout --detach 351aff8f7679dbce7029533a43f72ccfe05e5704
PYTHONDONTWRITEBYTECODE=1 python3 /tmp/audit_v04.py /tmp/sentinelles-mvp04 /tmp/sentinelles-audit04-resultats-neufs
PYTHONDONTWRITEBYTECODE=1 python3 /tmp/confirm_v04.py /tmp/sentinelles-mvp04 /tmp/sentinelles-audit04-resultats-neufs
```

Le premier script retourne **1 attendu sur ce commit** pour T45, mais écrit quand même `evidence.json` avec les 48 tests. Lancer ensuite le second script séparément ; il confirme le défaut et les corrections, vérifie tous les rapports/exports ok, écrit `confirmations.json` et retourne 0 si ces confirmations sont établies. Python standard, Tk importable, FFmpeg/ffprobe avec libx264 et drawtext suffisent ; aucune dépendance IA utilisée.

| Script final exécuté, reproduit ci-dessous | SHA-256 |
|---|---|
| audit_v04.py | `9a531575fe5870f47a6790fb39498602e23492b9a29f8a859f428eedbb150b26` |
| confirm_v04.py | `c1ce34982562985a4955f222f7fed495ba9201c2c8ab1471dd71088906205dde` |

| Trace retenue pour cet audit | SHA-256 de l’exécution |
|---|---|
| test_run_v04_final.log | `d9bff04fc32abf26f1a9116f3eb398ad062611567484e081238e2c2417a6b980` |
| confirm_run_v04.log | `03c3add68da5a63fbdc823b1a669eede4354cf9982b503264653500cff05c7ee` |
| execution_v04_final/evidence.json | `9f3f9a2a5af5f975f2827571ba506923c915a5b96c5d5302ae9156cba6e350bf` |
| execution_v04_final/confirmations.json | `6d25ed646030a71fa0bc567c6d82d8511b1cf1a859b6b0f9154eeff7cd5fcd4f` |

**Code de `audit_v04.py`**

```python
"""Independent MVP 0.4 audit. No application file is modified.
Usage: PYTHONDONTWRITEBYTECODE=1 python3 audit_v04.py /path/to/repo /new/output/dir
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
REAL_THREAD = module.threading.Thread
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
                      event=Value(event),sponsor=Value(sponsor),status=Value('Prêt'),progress=Progress(),processing=False)
    for name in ['event_slug','source_id','probe_source','build_candidates','select_candidates','verify_export']:
        setattr(x,name,getattr(App,name))
    x.duration=lambda f:App.duration(x,f)
    x.new_run_dir=lambda:App.new_run_dir(x)
    x.process=lambda snapshot=None:App.process(x,snapshot)
    return x

def corrupt_packets(path,stream="v:0"):
    data=json.loads(REAL_CHECK(['ffprobe','-v','error','-select_streams',stream,'-show_packets',
                               '-show_entries','packet=pos,size','-of','json',str(path)],text=True))
    b=bytearray(path.read_bytes())
    for packet in data['packets']:
        pos=int(packet['pos']);size=int(packet['size'])
        b[pos:pos+size]=b'\0'*size
    path.write_bytes(b)
    return data['packets']

def execute(identifier,files,event='Événement test',output=None,hook=None,
            render_failure=None,publication_failure=False,driver=None,before_render=None):
    output=Path(output or ROOT/identifier)
    if not output.exists(): output.mkdir(parents=True)
    x=runner(output,files,event)
    if driver is None:x.processing=True
    messages=[];commands=[];escaped=None
    before_dirs=set(output.rglob('run_*')) if output.is_dir() else set()
    write_text=Path.write_text
    def run(cmd,*args,**kwargs):
        is_render=cmd[0]=='ffmpeg' and '-c:v' in cmd and '-vf' in cmd
        if is_render:
            commands.append(cmd[:])
            if before_render:before_render(x,cmd)
            if render_failure is not None and len(commands)==render_failure:
                Path(cmd[-1]).write_bytes(b'')
                raise subprocess.CalledProcessError(1,cmd,stderr='audit injection: failed export')
        result=REAL_RUN(cmd,*args,**kwargs)
        if hook and is_render: hook(x,cmd)
        return result
    def write(path,*args,**kwargs):
        if publication_failure and path.name=='publication_proposee.txt' and (not callable(publication_failure) or publication_failure(path)):
            raise PermissionError('audit injection: publication write denied')
        return write_text(path,*args,**kwargs)
    with patch.object(module.subprocess,'run',side_effect=run), \
         patch.object(Path,'write_text',write), \
         patch.object(module.messagebox,'showinfo',side_effect=lambda *a:messages.append(['info',*a])), \
         patch.object(module.messagebox,'showwarning',side_effect=lambda *a:messages.append(['warning',*a])), \
         patch.object(module.messagebox,'showerror',side_effect=lambda *a:messages.append(['error',*a])):
        try:
            if driver:driver(x)
            else:App.process(x)
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
              'escaped':escaped,'processing':x.processing,'run_snapshot_attrs_remaining':[a for a in ('_run_output','_run_event') if hasattr(x,a)],'driver_observations':getattr(x,'audit_dispatch',None),'messages':messages,'run_dirs':[str(p) for p in created],
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
        self.assertGreater(r['progress_starts'],0)
        self.assertEqual(r['progress_stops'],r['progress_starts'])
        self.assertIsNotNone(r['report'])
        self.assertTrue(all(item['exists'] for item in r['reports']))
        self.assertEqual(r['report']['schema_version'],'0.4')
        self.assertFalse(r['processing'])
        self.assertEqual(r['run_snapshot_attrs_remaining'],[])

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
        self.assertEqual(module.APP_NAME,'Sentinelles Content Factory MVP 0.4')
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
        self.assertFalse(x.processing)
        EVIDENCE['T25']={'empty_selection':'warning','missing_ffmpeg':'error','processing':x.processing}

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
        x=runner(ROOT/'T28',['r1']);starts=[]
        class FakeThread:
            def __init__(self,**kwargs):pass
            def start(self):starts.append('started')
        messages=[]
        with patch.object(module.threading,'Thread',FakeThread),patch.object(module.messagebox,'showwarning',side_effect=lambda *a:messages.append(a)):
            App.run_thread(x);App.run_thread(x)
        self.assertEqual(len(starts),1)
        self.assertEqual(len(messages),1)
        self.assertEqual(messages[0][0],'Traitement en cours')
        self.assertTrue(x.processing)
        EVIDENCE['T28']={'workers_started':1,'second_refused':True,'warnings':messages,
                         'processing_while_worker_pending':x.processing,'actual_Tk_concurrency':'not tested'}

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
        self.assert_no_output(r)
        self.assertEqual(r['report']['errors'][0]['error'],'Décodage vidéo de contrôle échoué')

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
        x.processing=True
        x.files=[str(FILES['half_second'])]
        def dialog(*args):calls.append({'method':'messagebox double','thread':module.threading.get_ident()})
        with patch.object(module.messagebox,'showwarning',side_effect=dialog):
            t=module.threading.Thread(target=lambda:App.process(x))
            t.start();t.join(timeout=10)
        self.assertFalse(t.is_alive());self.assertFalse(x.progress.active);self.assertFalse(x.processing)
        self.assertTrue(any(c['thread']!=ident for c in calls))
        EVIDENCE['T42']={'main_thread':ident,'calls':calls,
                         'actual_Tk_widgets':'not tested; no DISPLAY/Xvfb',
                         'conclusion':'original process calls UI interfaces from worker thread'}


    def test_T43_actual_worker_second_start_refused_and_success_unlocks(self):
        ready=module.threading.Event();release=module.threading.Event();workers=[]
        def pause(x,cmd):
            ready.set()
            if not release.wait(timeout=15):raise RuntimeError('audit barrier timeout')
        def factory(**kwargs):
            t=REAL_THREAD(**kwargs);workers.append(t);return t
        def drive(x):
            with patch.object(module.threading,'Thread',side_effect=factory):
                App.run_thread(x)
                if not ready.wait(timeout=15):
                    release.set();raise RuntimeError('worker did not reach rendering barrier')
                active=x.processing
                App.run_thread(x)
                count=len(workers)
                release.set()
                for t in workers:t.join(timeout=20)
                x.audit_dispatch={'processing_at_barrier':active,'workers_created':count,
                                  'workers_alive_after_join':sum(t.is_alive() for t in workers)}
        r=execute('T43',['r1'],driver=drive,before_render=pause);self.assert_render_ok(r,1)
        self.assertEqual(r['driver_observations'],
                         {'processing_at_barrier':True,'workers_created':1,'workers_alive_after_join':0})
        self.assertEqual(sum(m[0]=='warning' and m[1]=='Traitement en cours' for m in r['messages']),1)

    def test_T44_snapshot_frozen_before_worker_and_despite_form_edits(self):
        pending=[]
        class DeferredThread:
            def __init__(self,**kwargs):self.kwargs=kwargs
            def start(self):pending.append(self.kwargs)
        def drive(x):
            with patch.object(module.threading,'Thread',DeferredThread):App.run_thread(x)
            initial=pending[0]['args'][0]
            x.event.set('Autre événement');x.sponsor.set('Autre partenaire')
            x.files[:]=[str(FILES['r2'])]
            x.output=ROOT/'T44_other_output'
            pending[0]['target'](*pending[0]['args'])
            x.audit_dispatch={'snapshot_event':initial['event'],'snapshot_sponsor':initial['sponsor'],
                              'snapshot_files':initial['files'],'snapshot_output':str(initial['output']),
                              'current_files':x.files,'current_output':str(x.output),
                              'current_event':x.event.get(),'current_sponsor':x.sponsor.get()}
        r=execute('T44',['r1'],'Événement initial',driver=drive);self.assert_render_ok(r,1)
        self.assertEqual(r['report']['event'],'Événement initial')
        self.assertEqual(r['report']['sponsors'],'Partenaire test')
        self.assertEqual(r['report']['sources'][0]['file'],str(FILES['r1']))
        self.assertEqual(Path(r['run_dirs'][0]).parent.parent,ROOT/'T44')
        self.assertEqual(r['publication'].splitlines()[0],'Titre proposé : Événement initial | Les Sentinelles')
        self.assertIn('Partenaire test',r['publication'])
        self.assertNotIn('Autre partenaire',r['publication'])
        self.assertFalse((ROOT/'T44_other_output').exists())

    def test_T45_thread_start_failure_must_release_processing_lock(self):
        class CannotStartThread:
            def __init__(self,**kwargs):pass
            def start(self):raise RuntimeError("audit injection: can't start new thread")
        def drive(x):
            with patch.object(module.threading,'Thread',CannotStartThread):App.run_thread(x)
        r=execute('T45',['r1'],driver=drive)
        self.assertEqual((r['escaped'],r['processing']),(None,False),
                         'Thread-start error escapes and leaves processing True with no running generation')
        self.assertEqual(r['run_dirs'],[])

    def test_T46_lock_released_after_error_then_next_generation_succeeds(self):
        workers=[];write_attempts=[]
        def fail_once(path):
            write_attempts.append(str(path))
            return len(write_attempts)==1
        def factory(**kwargs):
            t=REAL_THREAD(**kwargs);workers.append(t);return t
        def drive(x):
            states=[]
            with patch.object(module.threading,'Thread',side_effect=factory):
                for _ in range(2):
                    App.run_thread(x);workers[-1].join(timeout=20)
                    if workers[-1].is_alive():raise RuntimeError('audit worker timeout')
                    states.append({'processing':x.processing,'status':x.status.get()})
            x.audit_dispatch={'workers_created':len(workers),'after_each_run':states}
        r=execute('T46',['r1'],driver=drive,publication_failure=fail_once);self.assert_render_ok(r,1)
        self.assertEqual(r['driver_observations']['workers_created'],2)
        self.assertEqual(r['driver_observations']['after_each_run'],
                         [{'processing':False,'status':'Erreur'},{'processing':False,'status':'Terminé : 1 Shorts prêts à valider'}])
        reports=[json.loads((Path(p)/'rapport.json').read_text()) for p in r['run_dirs']]
        self.assertEqual(sorted(report['status'] for report in reports),['completed','failed'])
        self.assertEqual(len(r['outputs']),2)
        self.assertFalse(any(m[0]=='warning' and m[1]=='Traitement en cours' for m in r['messages']))

    def test_T47_audio_payload_corruption_must_not_be_status_ok(self):
        packet_records=[]
        def corrupt_audio(x,cmd):packet_records.extend(corrupt_packets(Path(cmd[-1]),stream='a:0'))
        r=execute('T47',['audio'],hook=corrupt_audio)
        EVIDENCE['T47']['injected_corruption']={'method':'zero AAC packet payloads, retain video and MP4 structure',
                                               'packet_count':len(packet_records)}
        self.assert_finished(r)
        self.assertNotEqual(r['outputs'][0]['decode'],{'returncode':0,'stderr':''})
        self.assertEqual(r['report']['exports'],[],
                         'Output with undecodable audio is marked status: ok')

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

**Code de `confirm_v04.py`**

```python
"""Independent confirmations for the exact MVP 0.4 snapshot."""
import hashlib,importlib.util,json,subprocess,sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
sys.dont_write_bytecode=True
repo=Path(sys.argv[1]).resolve();root=Path(sys.argv[2]).resolve()
spec=importlib.util.spec_from_file_location('v04_confirmed_app',repo/'app/app.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
data=json.loads((root/'evidence.json').read_text())['evidence']
def decode(path,video_only=False):
    cmd=['ffmpeg','-v','error','-i',str(path)]
    if video_only:cmd+=['-map','0:v:0']
    cmd+=['-f','null','-']
    p=subprocess.run(cmd,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,text=True)
    return {'returncode':p.returncode,'stderr':p.stderr}
before={str(p.relative_to(repo)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (repo/'app').rglob('*') if p.is_file()}
runs=sorted(p for p in root.rglob('run_*') if p.is_dir())
reports=[json.loads((p/'rapport.json').read_text()) for p in runs]
ok=[{'run':str(p),'entry':e} for p,r in zip(runs,reports) for e in r['exports'] if e['status']=='ok']
checks=[]
for item in ok:
    file=Path(item['entry']['file'])
    decoded=decode(file)
    metadata=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0',
                                                '-show_entries','stream=width,height,duration','-of','json',str(file)],text=True))
    item.update({'bytes':file.stat().st_size,'probe':metadata,'decode':decoded})
    assert decoded=={'returncode':0,'stderr':''}
    assert (metadata['streams'][0]['width'],metadata['streams'][0]['height'])==(1080,1920)
    checks.append(item)
c1={'id':'C01','created_run_dirs':len(runs),'parsed_reports':len(reports),
    'actual_status_ok_count':len(checks),'all_status_ok_decode_checks':checks}
source=Path(data['T36']['inputs'][0])
packets=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_packets',
                                           '-show_entries','packet=pts_time,duration_time','-of','json',str(source)],text=True))['packets']
end=max(float(p['pts_time'])+float(p['duration_time']) for p in packets)
c2={'id':'C02','original_probe_source':m.App.probe_source(source),'independent_packet_video_end':end,
    'container_duration':data['T36']['input_probe']['format']['duration'],
    'input_decode':decode(source),'pipeline_export_count':len(data['T36']['report']['exports'])}
assert abs(c2['original_probe_source']['duration']-end)<1e-6
assert c2['input_decode']=={'returncode':0,'stderr':''} and c2['pipeline_export_count']==1
def verify_result(path):
    try:return {'return':m.App.verify_export(path),'error':None}
    except Exception as e:return {'return':None,'error':{'type':type(e).__name__,'message':str(e)}}
damaged=Path(data['T37']['outputs'][0]['file'])
c3={'id':'C03','path':str(damaged),'bytes':damaged.stat().st_size,
    'sha256':hashlib.sha256(damaged.read_bytes()).hexdigest(),'original_verify_export':verify_result(damaged),
    'independent_decode':decode(damaged),'report_exports':data['T37']['report']['exports']}
assert c3['original_verify_export']['error']['type']=='ValueError' and c3['report_exports']==[]
assert c3['independent_decode']['returncode']!=0
r=data['T44']
c4={'id':'C04','snapshot':r['driver_observations'],'report_event':r['report']['event'],
    'report_sponsors':r['report']['sponsors'],'run_dir':r['run_dirs'][0],'publication':r['publication']}
assert c4['report_event']==c4['snapshot']['snapshot_event']=='Événement initial'
assert c4['report_sponsors']==c4['snapshot']['snapshot_sponsor']=='Partenaire test'
assert c4['publication'].splitlines()[0]=='Titre proposé : Événement initial | Les Sentinelles'
interpreter=m.tk.Tcl()
x=SimpleNamespace(processing=False,files=[str(source)],event=m.tk.StringVar(master=interpreter,value='Démarrage'),
                  sponsor=m.tk.StringVar(master=interpreter,value='Partenaire'),output=root/'unused_start',
                  process=lambda snapshot:None)
escaped=None;warnings=[]
with patch.object(m.threading.Thread,'start',side_effect=RuntimeError("audit injection: can't start new thread")) as starts:
    try:m.App.run_thread(x)
    except Exception as e:escaped={'type':type(e).__name__,'message':str(e)}
    start_calls=starts.call_count
with patch.object(m.messagebox,'showwarning',side_effect=lambda *args:warnings.append(args)):
    m.App.run_thread(x)
c5={'id':'C05','actual_thread_class_with_start_failure_injected':True,'actual_tcl_variables':True,
    'escaped':escaped,'thread_start_calls':start_calls,'processing_after_error':x.processing,
    'warnings_on_next_request':warnings}
assert escaped['type']=='RuntimeError' and x.processing is True and start_calls==1
assert warnings[0][0]=='Traitement en cours'
audio=Path(data['T47']['outputs'][0]['file'])
c6={'id':'C06','original_verify_export':verify_result(audio),'independent_decode':decode(audio),
    'report_exports':data['T47']['report']['exports']}
assert c6['original_verify_export']['error']['type']=='ValueError' and c6['report_exports']==[]
after={str(p.relative_to(repo)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (repo/'app').rglob('*') if p.is_file()}
assert before==after
out={'confirmations':[c1,c2,c3,c4,c5,c6],'app_unchanged':before==after}
(root/'confirmations.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
print(json.dumps({'created_run_dirs':len(runs),'reports':len(reports),'status_ok_count':len(checks),
                  'mk_video_duration':c2['original_probe_source']['duration'],'mkv_container_duration':c2['container_duration'],
                  'h264_gate_error':c3['original_verify_export']['error'],'startup_fault':c5,
                  'audio_corruption_gate_error':c6['original_verify_export']['error'],'app_unchanged':before==after},ensure_ascii=False,indent=2))

```

