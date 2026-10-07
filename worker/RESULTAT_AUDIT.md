# Audit indépendant — Sentinelles Content Factory MVP 0.5

**Verdict final : CANDIDAT.**

La campagne demandée est rejouée intégralement : **48 contrôles réussis, aucun échec, aucune erreur de harnais**, grilles T02/T03 et confirmations C01–C06. Le blocage **MAJ-08** du MVP 0.4 est levé dans les deux cas injectés : échec de construction du thread et échec de `Thread.start()`. Dans chacun, aucune exception ne s’échappe, `processing` revient à false, une erreur utilisateur est signalée, puis un vrai worker réalise une nouvelle génération avec export décodable.

Les essais moteur justifient **CANDIDAT**. Les widgets Tk et les interactions graphiques réelles restent à exercer ; **VALIDÉ n’est pas justifié** par cet environnement sans affichage. Le bit exécutable du lanceur reste absent dans Git : ce mineur n’est pas déclaré corrigé. Aucun défaut critique ou majeur n’est reproduit dans la campagne exécutée.

**Cible, lectures et intégrité**

- Dépôt : [noobstrade/sentinelles-content-factory](https://github.com/noobstrade/sentinelles-content-factory).
- Branche : `develop`.
- Commit audité : [`8519391fbb0fe8ac3ad9ca223010ecceefa65b0b`](https://github.com/noobstrade/sentinelles-content-factory/commit/8519391fbb0fe8ac3ad9ca223010ecceefa65b0b).
- Date : 7 octobre 2026, UTC.
- Arbre racine : `eb37dee6057849a6b644c45f4f44083d78b569b2`.
- Arbre `app/` : `c1d6f41101da3df27ef701b1ac904fa50217beab`.
- Blob de `app/app.py` : `23d9a0ff13cefb7cfc70196f11a3b256468022cf`.
- Lectures intégrales, dans l’ordre demandé : `worker/A_AUDITER.md` MVP 0.5, `docs/PRODUCT_SPEC.md`, `docs/AUDIT_BASELINE.md`, `docs/WORKFLOW.md`, puis les six fichiers de `app/`. Le rapport MVP 0.4 conservé dans ce commit est relu pour conserver ses 48 scénarios et les contrôles C01–C06. Aucun `AGENTS.md` dans l’arbre du dépôt.
- Le snapshot des 12 fichiers est vérifié contre les tailles et SHA des blobs Git. Aucun fichier de `app/` n’est modifié, aucun cache Python n’y est créé ; SHA-256 contrôlés avant/après la suite et les confirmations. Fixtures, scripts et traces sont hors du dépôt.
- Seul fichier remplacé : `worker/RESULTAT_AUDIT.md`, destiné à un commit sur `develop`. Aucun correctif de l’application, aucun changement de `main`.

| Référence lue | Blob Git du commit audité |
|---|---|
| docs/PRODUCT_SPEC.md | `06ea2a976addbd88a4a8cd63cd9b3fb4b871d8ce` |
| docs/AUDIT_BASELINE.md | `655a509d70e6e2f2ec45e37113d1d840b85777a8` |
| docs/WORKFLOW.md | `54bfa59a7ffb03ac189a2785d8a32ac00a8146a2` |
| worker/A_AUDITER.md | `c8f0c2fce0cb8601aaf9e58fb93571fe0e22c404` |

**Campagne exécutée et méthode**

Les **48 scénarios de test** du MVP 0.4 sont rejoués sous les mêmes identifiants : T01–T47 et T99. T45 contient désormais deux sous-cas, construction et start, avec nouvelle génération réelle après chaque injection. T27 vérifie les deux commandes `sh` documentées et distingue le mode Git de l’exécution directe. Résultat : **48/48 contrôles réussis**, dont les observations de portée limitée T27/T42 ; aucun résultat graphique complet n’en est déduit. Durée de la suite unittest : **70,024 s**, hors création des fixtures et confirmations.

T02 explore **66 429 configurations** : une à cinq sources, durées 0,5/1/2/10/18/24/48/60/120 s, bornes temporelles, maximum trois exports, diversité des identités utilisables et écart minimal de 12 s sur la même source. T03 ajoute **120 configurations** avec alias et source en erreur, ainsi que la frontière de 48 s donnant les starts 3/15/27. **Zéro violation** dans ces grilles.

Environnement : **Python 3.12.14, Linux x86_64 / noyau 6.18.44 / glibc 2.39, Tk/Tcl 9.0, FFmpeg et ffprobe 6.1.1-3ubuntu5**. Python standard et import Tk disponibles ; pas d’installation des dépendances IA, non utilisées par ce pipeline. Aucun `DISPLAY` ni Xvfb disponible. Les méthodes originales du commit sont importées directement, sans réécriture de l’application. Génération des médias, encodage, ffprobe et décodage FFmpeg sont réels.

Les erreurs de rendu, d’écriture, de construction/démarrage de thread, les collisions et la corruption après encodage sont injectées explicitement pour exercer les branches d’erreur. Une saturation spontanée du système n’a pas été observée. Le harnais distingue les encodages, qui seuls déclenchent les injections, des décodages de contrôle internes. Les sorties rejetées sont également probées et décodées.

Les interfaces événement/partenaire/statut/progression/messagebox de la campagne moteur utilisent des doubles. T43, les relances de T45 et T46 emploient de vrais threads Python. C05 confirme séparément les deux erreurs avec de vraies `tk.StringVar` sur un interpréteur Tcl ; les dialogues y sont interceptés. Sa relance emploie un callback sans UI pour vérifier l’autorisation du lancement ; la génération complète, le rapport, l’export et la libération finale sont prouvés par T45. Les widgets graphiques réels et une mainloop Tk ne sont pas exercés.

**Confirmations indépendantes C01–C06**

| Contrôle | Preuve obtenue |
|---|---|
| C01 | Scan indépendant de **53 dossiers run**, lecture de **53 rapports JSON**, extraction de **60 entrées réellement marquées ok**, y compris l’export valide du premier run T46 dont le statut global est failed. Chaque fichier existe, est non vide, est une vidéo 1080×1920 et passe un décodage complet de tous les flux : **60 codes 0, 60 stderr vides**. |
| C02 | `probe_source` original sur le MKV vidéo ~2 s/audio ~60 s : fin vidéo **2,023 s**, identique au maximum indépendant PTS + durée des paquets vidéo. Conteneur **60,023 s**. Source décodable et un vrai Short exporté, start 0. La durée vidéo exportée est de 2 s. |
| C03 | H.264 dont les payloads vidéo sont remplacés par des zéros en conservant la structure MP4 : ffprobe trouve 1080×1920, décodage complet en échec, `verify_export` original lève `ValueError: Décodage vidéo de contrôle échoué`. Aucune entrée ok. |
| C04 | Lecture croisée de T44 : événement/partenaire/rushs/destination modifiés avant l’exécution différée ; dossier, JSON, texte et source restent ceux du snapshot initial. La nouvelle destination n’est pas créée. |
| C05 | Échecs de construction et de start injectés séparément, avec variables Tcl réelles : **aucune exception échappée**, **processing false**, statut **Erreur**, appel `showerror("Démarrage impossible", ...)`, puis **un vrai thread autorisé** dans chaque cas. T45 complète cette confirmation par deux rendus réels réussis. |
| C06 | Payloads AAC corrompus après encodage, vidéo conservée : rejet par le vérificateur original, erreur persistée, aucune entrée ok ; décodage intégral indépendant en échec. Ce scénario ne prouve pas le rejet de toutes les corruptions audio possibles. |

**65 fichiers MP4 restants** sont contrôlés individuellement dans la campagne. **60 sont déclarés ok et tous sont décodables**. Les **5 autres** sont les sorties rejetées des tests de mauvaises dimensions, audio-only, texte invalide, H.264 corrompu et AAC corrompu. Les fichiers à zéro octet de T19/T32/T41 sont supprimés. C01 scanne tous les rapports, notamment les deux générations T46, pour compléter le helper qui expose seulement le dernier rapport de chaque scénario.

**Levée de MAJ-08 — preuves de démarrage et de reprise**

Localisation du correctif contrôlé : `app/app.py`, lignes 57–63. La construction ligne 58 et `start()` ligne 59 sont dans le try ; l’exception libère `processing` ligne 61, définit le statut Erreur ligne 62 et appelle le dialogue d’erreur ligne 63.

Protocole T45, exécuté pour chacun des deux sous-cas :

1. Sélection valide, FFmpeg/ffprobe disponibles, `processing=False`.
2. Injecter un `RuntimeError` dans la construction de `Thread`, puis séparément dans `start` de la vraie classe Thread.
3. Appeler `App.run_thread` original ; observer l’absence d’exception, l’état et le dialogue demandé.
4. Retirer l’injection ; appeler de nouveau `run_thread` avec un vrai thread, attendre son terme et vérifier JSON, MP4, décodage et libération du verrou.

| Observation | Construction en échec | start en échec |
|---|---|---|
| Exception échappée au premier appel | Aucune | Aucune |
| processing après l’échec | false | false |
| Statut après l’échec | Erreur | Erreur |
| Signal utilisateur demandé | Démarrage impossible / audit injection: constructor failure | Démarrage impossible / audit injection: start failure |
| Dossier run / progression avant relance | Aucun / aucun démarrage | Aucun / aucun démarrage |
| Thread réel créé à la relance | 1 | 1 |
| Export à la relance | 1 H.264 1080×1920, décodage code 0 et stderr vide | 1 H.264 1080×1920, décodage code 0 et stderr vide |
| État final après relance | processing false, progression arrêtée | processing false, progression arrêtée |
| Faux refus Traitement en cours à la relance | Aucun | Aucun |

**MAJ-08 est corrigé dans ces deux scénarios**, confirmé par T45/C05. Le signal utilisateur est prouvé par l’appel du dialogue, pas par l’affichage d’une boîte réelle dans cet environnement.

Les non-régressions sont conservées : **T43** maintient un vrai worker à une barrière de rendu, constate `processing=True`, refuse le deuxième appel avec un seul warning et un seul worker, puis achève la génération et libère le verrou. **T46** force une erreur d’écriture du texte au premier run, vérifie `processing=False`, puis autorise une deuxième génération réussie ; deux rapports et deux exports décodables restent présents, avec deux démarrages et deux arrêts de progression.

**Statut des autres constats**

| Point | Preuves | Conclusion limitée aux cas exécutés |
|---|---|---|
| MAJ-01 résiduel, durée MKV avec audio plus long | T36, C02 ; MP4 T29 | Non-régression confirmée : timeline vidéo ~2 s, pas durée conteneur ~60 s ; export vidéo exploitable. |
| MAJ-06, H.264 probe-able mais indécodable | T37, T99, C03 | Non-régression confirmée : rejet, erreur export, aucune entrée ok. |
| MAJ-07, événement/partenaire modifiés pendant le rendu | T24, T44, C04 | Non-régression confirmée : snapshot cohérent pour dossier, JSON, texte, rushs et destination. |
| MAJ-08, échec de démarrage verrouillant l’instance | T45, C05 | Corrigé pour construction et start : notification, libération et nouvelle génération réelle. |
| Multi-rush et inventaire de toutes les sources | T04–T06, T19, T20, T39 | Toutes les entrées inventoriées, poursuite après erreur source/export, maximum trois exports par génération. |
| Déduplication temporelle et alias physiques | T02, T03, T07–T10, T26, T30, T31 | Écart minimal 12 s par source_id ; symlink/hardlink reconnus dans l’environnement Linux testé. |
| Aucun écrasement, retry de collision | T11, T23 | Dossiers distincts ; hashes MP4/TXT/JSON précédents inchangés ; retry puis épuisement de cinq essais gérés. |
| Portrait, carré, paysage, source silencieuse MP4/MKV, AAC | T04, T15–T18, T29, T40 | Exports vidéo 1080×1920 décodables ; audio conservé quand présent dans ces fixtures. |
| Zéro export, sorties invalides, génération partielle | T14, T19, T32–T35, T37, T41, T47 | Pas de faux succès lorsque zéro export ; erreurs persistées, sorties invalides exclues, zéro octet supprimé. |
| Rapport après création d’un run | T19, T20, T38, T41, T46, C01 | 53/53 rapports présents et parseables. Aucun run lors des démarrages échoués, de la destination fichier T21 ou de l’épuisement de collision T23. |
| MIN-02, résolution du lanceur depuis racine/app | T27, lecture du script et README | Corrigée sur Linux pour les deux commandes sh documentées ; voir distinction du bit exécutable ci-dessous. |
| MIN-03, README en retard de version | T01, T27, lecture intégrale | Corrigé : README MVP 0.5, version du titre et du schéma 0.5, commandes sh cohérentes et fonctions absentes explicitement listées. |

La déduplication reste temporelle : starts 3/15/27 et durées 18 s se chevauchent de 6 s, conformément au seuil de 12 s entre débuts. Une copie du même contenu sous une autre identité inode n’est pas une déduplication sémantique démontrée. L’inventaire de quatre sources avec maximum trois Shorts ne prouve pas que chaque source soit représentée dans un export.

**Lanceur et documentation — résultat précis**

Le fichier `app/run_linux_mac.sh` est enregistré dans l’arbre Git avec le mode **100644** ; la copie fidèle a le mode **0644**. L’exécution directe lève **PermissionError** dans chacun des deux répertoires testés. **La correction du bit exécutable n’est pas prouvée et ce point mineur reste ouvert.** Le mode Git a été conservé ; le lanceur n’a pas été rendu exécutable par l’audit.

| Invocation | Répertoire courant | Résolution vérifiée | Exécution réelle dans cet environnement |
|---|---|---|---|
| `sh app/run_linux_mac.sh` | Racine du dépôt | python3 reçoit le chemin absolu de app/app.py ; substitut Python sort 0 | app.py est chargé, puis TclError faute de DISPLAY ; code 1 |
| `sh run_linux_mac.sh` | app/ | Même chemin absolu ; substitut Python sort 0 | Même chargement et même limite d’affichage ; code 1 |
| Exécution directe du script | Racine et app/ | Non démarrée, mode 0644 | PermissionError |

Le substitut Python de T27 est créé hors du dépôt et journalise argv et cwd. Les lancements avec le vrai Python atteignent Tk ; aucune erreur `can't open file`. Le défaut antérieur de recherche de app.py depuis la racine n’est plus reproduit. Le lancement complet de la GUI sur macOS n’est pas exécuté.

`app/README.md` affiche MVP 0.5 et décrit le snapshot, le verrou et ses erreurs, le probing vidéo, le contrôle des exports et les deux commandes sh. Ces comportements correspondent aux preuves T24/T29/T36/T37/T43–T46/C01–C05. Les fonctions absentes restent explicites. La roadmap décrit des étapes ; elle ne prouve pas leur livraison. Aucune suite de tests intégrée ni séparation moteur/UI n’est ajoutée à l’application par cet audit.

**Grille complète des 48 contrôles**

| Test | Scénario | Résultat observé |
|---|---|---|
| T01 | Syntaxe AST et import original | OK — syntaxe et import originaux ; APP_NAME = MVP 0.5. |
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
| T14 | Sources de 0,5 s et une seule image | OK — zéro export, no_usable_segment, statut et appel warning sans annonce de Shorts prêts. |
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
| T27 | Lanceur via sh depuis racine/app, exécution directe et README | OK pour sh depuis racine et app/ : chemin absolu correct, substitut Python code 0, vrai Python atteint Tk puis échoue faute de DISPLAY. README MVP 0.5. OBSERVATION : mode Git 100644/0644 et exécution directe PermissionError restent inchangés. |
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
| T45 | Échecs de construction/start injectés puis relances réelles | OK — deux sous-cas construction/start : aucune exception échappée, processing false, statut Erreur et dialogue Démarrage impossible ; relance avec vrai worker, un export décodable et verrou libéré dans chaque cas. C05 confirme séparément. |
| T46 | Vrai worker en erreur d’écriture puis nouvelle génération réussie | OK — deux workers successifs, verrou libéré après chaque run ; status Erreur puis Terminé ; deux JSON et deux exports valides conservés. |
| T47 | Payloads AAC corrompus après encodage, vidéo conservée | OK — rejet avec Décodage vidéo de contrôle échoué ; décodage intégral code 69 ; aucune entrée ok. |
| T99 | Contrôle transversal de tous les fichiers MP4 produits | OK — 65 MP4 probés et décodés, aucun invalide marqué ok. C01 scanne tous les rapports, y compris les deux T46, et confirme 60 exports ok valides. |

**Défauts et limites**

Aucun défaut critique ou majeur reproduit dans la campagne demandée. Mineur ouvert : bit exécutable du lanceur Linux/macOS absent dans Git, avec contournement documenté par sh et preuve de résolution correcte sur Linux.

**GUI réelle encore à valider.** T42 constate que le worker appelle les interfaces de variables, progression et messagebox avec des doubles. Le code comporte encore des appels d’UI avant le try de `process` (ligne 152) et une lecture de snapshot avant le try de `run_thread` (ligne 56). Aucun crash des widgets Tk ni absence de crash n’est déclaré prouvé. Les tests d’injection T45/C05 portent sur construction/start, pas sur une exception de widget réel. L’absence de DISPLAY est une limite d’environnement, pas un défaut majeur reproduit de l’application.

Essais restants pour envisager VALIDÉ :

- Génération depuis une fenêtre Tk réelle sur les systèmes cibles, avec progression, statut et dialogues.
- Deux demandes pendant un rendu, modification des champs et destination, puis vérification du snapshot, du refus et du rétablissement de l’interface.
- Erreur interne et nouvelle génération, fermeture de la fenêtre pendant un traitement, comportement des callbacks et threads avec une mainloop active.
- Lancement GUI Linux/macOS et Windows dans leurs environnements natifs ; validation humaine du cadrage et du texte sur un événement pilote réel.

Les erreurs partielles T19/T20 sont visibles dans rapport.json ; le message final annonce le nombre de sorties sans résumé de ces erreurs. Les fichiers invalides non nuls restent sur disque, liés à une erreur JSON et exclus des exports ok. Cela n’invalide pas les preuves de poursuite et de traçabilité obtenues.

**Portée produit et communication**

Le moteur sélectionne à fractions temporelles fixes 25/50/75 %, recadre au centre et applique un bandeau fixe. Il produit des exports locaux versionnés, leur provenance et un texte social générique. Les partenaires alimentent ce texte ; aucune gestion métier des contreparties n’est démontrée.

Toujours absents et hors du mandat de fiabilisation : transcription/sous-titres, scoring hockey intelligent, sélection multimodale, suivi intelligent 9:16, Sponsor Manager et reporting partenaire. Les dépendances déclarées ne prouvent pas leur intégration. Le rappel de validation humaine ne démontre pas un circuit éditorial complet. La pertinence hockey, l’audience, la qualité sur un match réel et le gain de temps bénévole restent **à mesurer**, conformément à PRODUCT_SPEC/AUDIT_BASELINE.

**Décision finale**

**CANDIDAT** sur `8519391fbb0fe8ac3ad9ca223010ecceefa65b0b` : les 48 contrôles, les deux grilles et C01–C06 passent ; MAJ-08 est levé avec reprises réelles et les anciens blocages ne réapparaissent pas. Les **60 exports ok** ont tous été décodés intégralement. Les essais graphiques et natifs restent nécessaires pour prononcer VALIDÉ. Aucun transfert sur main.

**Annexe — chaque sortie laissée par la campagne**

Statut « ok » retrouvé dans les rapports par C01. Les deux runs T46 sont distingués par leur statut global : l’export du run failed est valide et bien contrôlé. Cette table contient les 65 fichiers restants, y compris les 5 rejets.

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
| T45_constructor | short_01_9x16.mp4 | 69596 | 1080×1920 | 2.000000 | 0 / stderr vide | ok |
| T45_start | short_01_9x16.mp4 | 69596 | 1080×1920 | 2.000000 | 0 / stderr vide | ok |
| T46 (failed) | short_01_9x16.mp4 | 69596 | 1080×1920 | 2.000000 | 0 / stderr vide | ok |
| T46 (completed) | short_01_9x16.mp4 | 69596 | 1080×1920 | 2.000000 | 0 / stderr vide | ok |
| T47 | short_01_9x16.mp4 | 99151 | 1080×1920 | 2.000000 | 69 / erreurs | exclu |

**Annexe — intégrité de app/**

Inventaire et SHA-256 identiques avant/après ; modes Git conservés. Aucun fichier ajouté dans app/.

| Fichier | SHA-256 identique avant/après |
|---|---|
| app/README.md | `3692cc6e33b1e89b3f36e4df9072a7646abdedc6b06942d9723ca9181c824190` |
| app/ROADMAP.md | `e98b00f8ec9dc508fb675f01aa96bef1a86f181c465e8b760e66cae4e0fcd25b` |
| app/app.py | `f655f00d72b1c6080e52a2d7ddb8dd740ac750b202ce0ac5d980672370da12da` |
| app/requirements.txt | `be654442659daf5deace60880d5b13bda39c702793ff78a0e6ea2ddd2e7ef64b` |
| app/run_linux_mac.sh | `dadf3dbd662f23326342ea15572f88c7529dea0b218613bdcaacbe1f77c3a236` |
| app/run_windows.bat | `92f53ecbc23b49cf50624c8de78dc5dbbb119237c1ac45fc03e0ff2dd3e76f5e` |

**Annexe — reproduction autonome et traces**

Copier les deux blocs Python ci-dessous dans /tmp/audit_v05.py et /tmp/confirm_v05.py. Exécuter sur Linux avec Python/Tk importable, FFmpeg/ffprobe, libx264 et drawtext. Le répertoire de résultats doit être neuf. Aucune dépendance IA n’est utilisée. T27 suppose un environnement sans affichage ; les commandes ci-dessous retirent DISPLAY.

```sh
git clone --branch develop https://github.com/noobstrade/sentinelles-content-factory.git /tmp/sentinelles-mvp05
git -C /tmp/sentinelles-mvp05 checkout --detach 8519391fbb0fe8ac3ad9ca223010ecceefa65b0b
env -u DISPLAY PYTHONDONTWRITEBYTECODE=1 python3 /tmp/audit_v05.py /tmp/sentinelles-mvp05 /tmp/sentinelles-audit05-resultats-neufs
env -u DISPLAY PYTHONDONTWRITEBYTECODE=1 python3 /tmp/confirm_v05.py /tmp/sentinelles-mvp05 /tmp/sentinelles-audit05-resultats-neufs
```

Les deux scripts retournent **0 dans cette exécution**. Le premier écrit evidence.json ; le second scanne tous les rapports/exports ok et écrit confirmations.json. Identités inode, noms temporels et hashes d’encodage peuvent varier selon les machines ; dimensions, statuts, messages demandés et décodages sont les critères reproductibles. Les codes ci-dessous sont identiques aux scripts réellement exécutés, vérifiés par SHA-256 et comparaison textuelle.

| Script exécuté et reproduit ci-dessous | SHA-256 |
|---|---|
| audit_v05.py | `65aa44d54c78e20fc908cff6b2fb044d87b6a9f9d29fbfdf36d49823e70270f5` |
| confirm_v05.py | `d0867fb2f2593c3f55e4acb2ef07cb7a4c3faeb4a1cb6c0a3832aad33da38bdb` |

| Trace retenue pour cet audit | SHA-256 de l’exécution |
|---|---|
| test_run_v05.log | `d857eac93311d12a4d66e5ce6ece24880d4205f07a5fbcaa77b41bdf8bfa1776` |
| confirm_run_v05.log | `ce349974556a5e8cfda955e23c673e120c91d559cd256073721929e0f17bcf3b` |
| execution_v05/evidence.json | `cd87aacd9a514b34c2a326a695f26054b45a66e49c3ba857c990b994d87c790f` |
| execution_v05/confirmations.json | `9d20cf66990053c16db6f65ddc995554c431335fdc5fa33502ade0299bdfdc30` |

**Code de audit_v05.py**

```python
"""Independent MVP 0.5 audit. No application file is modified.
Usage: PYTHONDONTWRITEBYTECODE=1 python3 audit_v05.py /path/to/repo /new/output/dir
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
        self.assertEqual(r['report']['schema_version'],'0.5')
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
        self.assertEqual(module.APP_NAME,'Sentinelles Content Factory MVP 0.5')
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

    def test_T27_launchers_from_root_and_app_and_readme(self):
        script=REPO/'app/run_linux_mac.sh'
        shim=ROOT/'launcher_shim';shim.mkdir()
        fake_python=shim/'python3'
        fake_python.write_text("#!/bin/sh\nprintf '%s\\n' \"$PWD\" \"$@\" > \"$SENTINELLES_LAUNCH_LOG\"\nexit 0\n")
        fake_python.chmod(0o755)
        launches=[]
        for label,cwd,args in [('root',REPO,['sh','app/run_linux_mac.sh']),
                               ('app',REPO/'app',['sh','run_linux_mac.sh'])]:
            log=ROOT/('launcher_'+label+'.log')
            env=dict(os.environ,PATH=str(shim)+os.pathsep+os.environ['PATH'],SENTINELLES_LAUNCH_LOG=str(log))
            dispatched=REAL_RUN(args,cwd=cwd,env=env,capture_output=True,text=True)
            self.assertEqual(dispatched.returncode,0)
            observed=log.read_text().splitlines()
            self.assertEqual(observed,[str(cwd),str(REPO/'app/app.py')])
            real=REAL_RUN(args,cwd=cwd,capture_output=True,text=True)
            self.assertEqual(real.returncode,1)
            self.assertIn('no display name and no $DISPLAY environment variable',real.stderr)
            self.assertNotIn("can't open file",real.stderr)
            with self.assertRaises(PermissionError):
                REAL_RUN([str(script)],cwd=cwd,capture_output=True,text=True)
            launches.append({'cwd':str(cwd),'command':args,'shim_returncode':dispatched.returncode,
                             'shim_observed':observed,'real_returncode':real.returncode,'real_stderr':real.stderr,
                             'direct_execution':'PermissionError'})
        readme=(REPO/'app/README.md').read_text()
        for expected in ['MVP 0.5','sh app/run_linux_mac.sh','sh run_linux_mac.sh',
                         'échec de démarrage du worker','Fonctions encore absentes']:
            self.assertIn(expected,readme)
        self.assertNotIn('MVP 0.4',readme)
        EVIDENCE['T27']={'mode':oct(script.stat().st_mode&0o777),'launches':launches,
                         'readme_mvp_0_5_consistent':True,'gui_startup':'not available: no DISPLAY'}

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

    def test_T45_constructor_and_start_failure_notify_unlock_and_allow_retry(self):
        results=[]
        for stage in ['constructor','start']:
            with self.subTest(stage=stage):
                def drive(x):
                    injected=RuntimeError('audit injection: '+stage+' failure')
                    fault=(patch.object(module.threading,'Thread',side_effect=injected) if stage=='constructor'
                           else patch.object(REAL_THREAD,'start',side_effect=injected))
                    escaped=None
                    with fault as attempts:
                        try:App.run_thread(x)
                        except Exception as e:escaped={'type':type(e).__name__,'message':str(e)}
                        fault_calls=attempts.call_count
                    initial={'escaped':escaped,'processing':x.processing,'status':x.status.get(),
                             'fault_calls':fault_calls,'progress_starts':x.progress.starts,
                             'run_dirs':[str(p) for p in x.output.rglob('run_*')]}
                    workers=[]
                    def factory(**kwargs):
                        worker=REAL_THREAD(**kwargs);workers.append(worker);return worker
                    with patch.object(module.threading,'Thread',side_effect=factory):
                        App.run_thread(x)
                        for worker in workers:
                            worker.join(timeout=20)
                            if worker.is_alive():raise RuntimeError('audit retry worker timeout')
                    x.audit_dispatch={'failure_stage':stage,'after_injected_failure':initial,
                                      'retry_workers_created':len(workers),
                                      'retry_workers_alive':sum(w.is_alive() for w in workers)}
                r=execute('T45_'+stage,['r1'],driver=drive)
                self.assert_render_ok(r,1)
                self.assertEqual(r['driver_observations']['after_injected_failure'],
                                 {'escaped':None,'processing':False,'status':'Erreur','fault_calls':1,
                                  'progress_starts':0,'run_dirs':[]})
                self.assertEqual(r['driver_observations']['retry_workers_created'],1)
                self.assertEqual(r['driver_observations']['retry_workers_alive'],0)
                errors=[m for m in r['messages'] if m[0]=='error']
                self.assertEqual(errors,[['error','Démarrage impossible','audit injection: '+stage+' failure']])
                self.assertFalse(any(m[0]=='warning' and m[1]=='Traitement en cours' for m in r['messages']))
                results.append({'stage':stage,'result':'notified, unlocked, subsequent real render succeeds',
                                'observations':r['driver_observations']})
        EVIDENCE['T45']={'cases':results}

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

**Code de confirm_v05.py**

```python
"""Independent confirmations for the exact MVP 0.5 snapshot."""
import hashlib,importlib.util,json,subprocess,sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
sys.dont_write_bytecode=True
repo=Path(sys.argv[1]).resolve();root=Path(sys.argv[2]).resolve()
spec=importlib.util.spec_from_file_location('v05_confirmed_app',repo/'app/app.py')
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
real_thread=m.threading.Thread
startup_checks=[]
for stage in ['constructor','start']:
    callbacks=[];messages=[];escaped=None
    def finished(snapshot):callbacks.append({'event':snapshot['event'],'files':snapshot['files']})
    x=SimpleNamespace(processing=False,files=[str(source)],
                      event=m.tk.StringVar(master=interpreter,value='Démarrage'),
                      sponsor=m.tk.StringVar(master=interpreter,value='Partenaire'),
                      status=m.tk.StringVar(master=interpreter,value='Prêt'),
                      output=root/'unused_start',process=finished)
    injection=RuntimeError('audit injection: '+stage+' failure')
    fault=(patch.object(m.threading,'Thread',side_effect=injection) if stage=='constructor'
           else patch.object(real_thread,'start',side_effect=injection))
    with patch.object(m.messagebox,'showerror',side_effect=lambda *args:messages.append(['error',*args])), \
         patch.object(m.messagebox,'showwarning',side_effect=lambda *args:messages.append(['warning',*args])):
        with fault as attempts:
            try:m.App.run_thread(x)
            except Exception as e:escaped={'type':type(e).__name__,'message':str(e)}
            fault_calls=attempts.call_count
        after_failure={'escaped':escaped,'processing':x.processing,'status':x.status.get(),
                       'fault_calls':fault_calls,'messages':list(messages),'callbacks':list(callbacks)}
        workers=[]
        def factory(**kwargs):
            t=real_thread(**kwargs);workers.append(t);return t
        with patch.object(m.threading,'Thread',side_effect=factory):
            m.App.run_thread(x)
            for worker in workers:worker.join(timeout=5)
    assert after_failure=={'escaped':None,'processing':False,'status':'Erreur','fault_calls':1,
                           'messages':[['error','Démarrage impossible','audit injection: '+stage+' failure']],
                           'callbacks':[]}
    assert len(workers)==1 and not workers[0].is_alive() and len(callbacks)==1
    assert not any(msg[0]=='warning' for msg in messages)
    startup_checks.append({'stage':stage,'after_injected_failure':after_failure,
                           'subsequent_workers_created':len(workers),'subsequent_callback_executed':callbacks,
                           'actual_thread_class_on_retry':True,'all_messages':messages,
                           'processing_after_callback_stub':x.processing,
                           'callback_stub_note':'callback does not invoke process/finally; full success and unlock checked by T45'})
c5={'id':'C05','actual_tcl_variables':True,'actual_thread_start_failure_injected':True,
    'checks':startup_checks,'full_pipeline_retry_evidence':['T45_constructor','T45_start']}
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
