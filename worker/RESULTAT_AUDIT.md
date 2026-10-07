# Audit indépendant — Sentinelles Content Factory MVP 0.6

**Verdict final : CANDIDAT.**

Le repli sans `drawtext` est conforme dans les simulations exécutées : **trois exports H.264 1080×1920 valides** à partir de quatre MP4 synthétiques 1920×1080, avec `scale + crop + drawbox`, sans texte, capability false et warning explicite dans le JSON. Une seconde confirmation par un exécutable CLI simulé qui refuse réellement toute utilisation de drawtext produit également trois exports valides. Le contrôle des exports reste actif.

La campagne MVP 0.5 est rejouée intégralement et complétée : **55 contrôles, 54 réussis, 1 échec documentaire mineur T27, aucune erreur de harnais**. Les sept nouveaux contrôles T48–T54 passent, ainsi que les grilles T02/T03 et C01–C08. **72 exports réellement enregistrés ok ont tous été décodés intégralement sans erreur**. Aucun défaut critique ou majeur n’est reproduit dans le périmètre exécuté.

Le README affiche encore MVP 0.5, et le lanceur reste sans bit exécutable dans Git. Ces mineurs ne sont pas déclarés corrigés. La recette GUI sur le Mac réel doit être rejouée : **VALIDÉ n’est pas justifié par les essais synthétiques réalisés ici**.

**Cible, lectures et intégrité**

- Dépôt : [noobstrade/sentinelles-content-factory](https://github.com/noobstrade/sentinelles-content-factory).
- Branche : `develop`.
- Commit audité : [`2654cd76f32d602f2c42d7aa92a817cff4f3fb30`](https://github.com/noobstrade/sentinelles-content-factory/commit/2654cd76f32d602f2c42d7aa92a817cff4f3fb30).
- Date : 7 octobre 2026, UTC.
- Arbre racine : `e48d1d44a3bcc468bf8e56a632e8550d140685bb`.
- Arbre `app/` : `3a2a06743fc18a04d0d811bfa295960568ebccba`.
- Blob `app/app.py` : `c7d451df03258f4ace01a821aaf7b1928a0c3bfd`.
- Lectures intégrales : mandat `worker/A_AUDITER.md` MVP 0.6, `docs/PRODUCT_SPEC.md`, `docs/AUDIT_BASELINE.md`, `docs/WORKFLOW.md`, puis les six fichiers de `app/`. Les 48 scénarios du rapport MVP 0.5 conservé dans ce commit sont repris, avec adaptation du titre/schéma attendu à 0.6 et ajout du helper de capacité original. Aucun `AGENTS.md` dans l’arbre du dépôt.
- Le snapshot des 12 fichiers est vérifié par taille et SHA de blob Git. Le rapport précédent a le blob `3a61a5024e791f761f91b541430a8541101fdba2`.
- Aucun fichier de `app/` modifié, aucun cache Python ni média ajouté dans l’application. Les SHA-256 avant/après la suite et les confirmations sont identiques. Fixtures, scripts, shims et traces sont hors du dépôt.
- Seul fichier remplacé : `worker/RESULTAT_AUDIT.md`, destiné au commit sur `develop`. Aucun correctif appliqué à l’application et aucun changement de `main`.

| Référence lue | Blob Git exact |
|---|---|
| docs/AUDIT_BASELINE.md | `655a509d70e6e2f2ec45e37113d1d840b85777a8` |
| docs/PRODUCT_SPEC.md | `06ea2a976addbd88a4a8cd63cd9b3fb4b871d8ce` |
| docs/WORKFLOW.md | `54bfa59a7ffb03ac189a2785d8a32ac00a8146a2` |
| worker/A_AUDITER.md | `7ff03ff2880ef877d0eafefaa352975f594f9f79` |

**Mandat terrain et portée de la reproduction**

Le mandat rapporte un démarrage GUI réussi du MVP 0.5 sur un Mac avec Python Homebrew 3.14.6, Tk 9.1 et FFmpeg Homebrew 9.0.2, puis l’échec de trois exports avec code 8 et absence de drawtext dans la liste des filtres. **Ces observations terrain proviennent du mandat ; elles n’ont pas été observées directement dans cet environnement.** Les quatre fichiers WhatsApp originaux ne sont pas fournis à cet audit.

Le build local de référence est FFmpeg Linux 6.1.1-3ubuntu5 et fournit drawtext, drawbox, scale et crop. Il permet de contrôler le cas positif. Le cas sans drawtext est exercé par deux simulations strictes documentées, avec encodages et décodages réels. Aucun build Homebrew n’est compilé ou exécuté ici. Les fixtures 1080p sont synthétiques, de deux secondes à deux images/seconde ; elles reproduisent le nombre, le format et les dimensions d’entrée, pas le contenu ni toutes les caractéristiques des rushs WhatsApp réels.

**Campagne et méthode**

Les identifiants **T01–T47 et T99**, soit les 48 contrôles précédents, sont conservés. Résultat de cette régression : **47 réussis et T27 en échec sur la seule cohérence de version du README**. Les vérifications de chemin du lanceur réalisées dans T27 réussissent. Les sept ajouts **T48–T54 passent**. Total : **54/55 réussis**, zéro erreur de harnais. Durée unittest : **41,389 s**, hors génération des fixtures et confirmations.

Les grilles passent sans violation :

- **T02 : 66 429 configurations**, une à cinq sources, durées 0,5/1/2/10/18/24/48/60/120 s ; bornes, minimum une seconde, maximum 18 s par extrait, limite de trois exports, diversité et écart minimal de 12 s par identité source.
- **T03 : 120 configurations** avec alias et source en erreur ; frontière à 48 s : starts 3/15/27.
- **T53 : dix cas** pour le détecteur original : flags de filtres, espaces/en-têtes, nom exact, nom voisin, simple mention dans une description, liste vide, retour non nul et exception.

Environnement : **Python 3.12.14, Linux x86_64 / noyau 6.18.44 / glibc 2.39, Tk/Tcl 9.0, FFmpeg et ffprobe 6.1.1-3ubuntu5**. Tk est importable ; aucun DISPLAY ni Xvfb disponible. Pas d’installation des dépendances IA, non utilisées par ce moteur.

Les méthodes originales du commit sont importées sans réécriture. Probing, création des fixtures, rendus autorisés et décodages sont réels. Les interfaces de formulaire/progression/dialogues sont remplacées par des doubles dans la campagne moteur. T43, les reprises T45 et T46 utilisent de vrais threads Python ; C05 utilise de vraies StringVar sur un interpréteur Tcl mais intercepte les dialogues. Les widgets Tk et la mainloop réels ne sont pas exercés.

Le wrapper de la campagne conserve la sortie réelle de `ffmpeg -hide_banner -filters` pour le cas présent ; pour le cas absent, il retire uniquement l’entrée drawtext et refuse un rendu qui continuerait à employer ce filtre. Les filtres indispensables et les décodages restent réels. T51 simule séparément un build sans scale et trois rejets code 8. Les injections de corruption s’appliquent après encodage et avant le vérificateur original.

C07/C08 emploient un **exécutable ffmpeg simulé sur PATH**, créé hors du dépôt : il masque le filtre annoncé absent, refuse son utilisation et transmet les autres commandes au véritable `/usr/bin/ffmpeg`. Ces confirmations ne patchent ni `ffmpeg_has_filter` ni `subprocess.run`. Le shim de C07 est d’abord vérifié par une commande utilisant drawtext : il retourne bien code 8 et `No such filter: 'drawtext'`. Le pipeline original produit ensuite ses trois Shorts sans rencontrer ce rejet.

**Matrice des exigences MVP 0.6**

| Exigence du mandat | Tests / confirmations | Résultat |
|---|---|---|
| Détecter drawtext disponible | T48, T53 ; régression sur build local | Détecteur original true ; chaîne de branding identique à celle du MVP 0.5 ; trois exports valides. |
| Continuer sans drawtext et produire trois Shorts 1080×1920 | T49, C07, C01 | Quatre sources 1920×1080 inventoriées, trois candidats et trois exports valides dans chaque méthode de simulation. Aucun drawtext dans les filtres de rendu. |
| Conserver drawbox dans la chaîne sans texte | T49, T50, C07 | scale/crop/drawbox présents. Contrôle supplémentaire des pixels : bandeau bleu sur une source noire, partie basse noire. |
| Tracer capability et warning | T48–T50, T54, C07, C01 | `ffmpeg_capabilities.drawtext` true/false selon la branche ; warning explicite si false. Champ présent dans les 62 rapports de génération et schéma 0.6. |
| Échouer proprement si un filtre indispensable manque | T51, C08 | scale annoncé absent et refusé ; trois erreurs export tracées avec commandes/code 8, zéro entrée ok, warning Aucun Short, progression arrêtée et processing false. |
| Ne jamais enregistrer ok sans contrôle de sortie | T32–T37, T47, T52, T99, C01, C03, C06 | Vérificateur ffprobe/décodage original conservé. T52 rejette les trois H.264 corrompus en branche sans drawtext. Les 72 sorties ok passent en outre le décodage indépendant de tous les flux. |

**Preuve détaillée du repli**

Localisation : `app/app.py`, détecteur **lignes 135–141**, filtre de base et branche conditionnelle **184–193**, vérification avant inscription ok **199–201**.

| Cas | Sources / candidats | JSON drawtext | Warning JSON | Chaîne de rendu | Exports ok |
|---|---|---|---|---|---:|
| T48, drawtext réel disponible | 3 / 3 | true | Aucun warning de repli | scale + crop + drawbox + drawtext | 3 |
| T49, liste sans drawtext et usage refusé | 4 MP4 1920×1080 / 3 | false | Explicite | scale + crop + drawbox | 3 |
| C07, exécutable CLI sans drawtext | 4 MP4 1920×1080 / 3 | false | Explicite | scale + crop + drawbox | 3 |
| T51 / C08, scale indispensable absent | 3 / 3 dans T51, 4 / 3 dans C08 | true | Aucun warning drawtext, car drawtext reste disponible | scale tenté et refusé | 0 |
| T52, branche sans texte puis H.264 corrompu | 3 / 3 | false | Explicite | scale + crop + drawbox, puis contrôle en échec | 0 |
| T54, énumération en erreur | 1 / 1 dans chacun des deux sous-cas | false | Explicite | scale + crop + drawbox | 1 par sous-cas |

Filtre réellement envoyé en branche sans texte :

```text
scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920:(iw-1080)/2:(ih-1920)/2,drawbox=x=0:y=0:w=iw:h=150:color=0x081B4B@0.82:t=fill
```

Extrait des rapports T49 et C07 :

```json
{
  "schema_version": "0.6",
  "status": "completed",
  "ffmpeg_capabilities": {"drawtext": false},
  "warnings": [
    "FFmpeg sans drawtext : bandeau graphique conservé, libellé texte omis."
  ]
}
```

Chacun contient trois exports ok, contrôlés par ffprobe puis décodage interne et indépendant. Les chaînes avec drawtext de T48 sont comparées intégralement à la chaîne antérieure. T50 ajoute un contrôle sur une première image RGB décodée : moyenne du bandeau **[0.0, 19.0, 66.0]**, moyenne de la zone inférieure **[0.0, 0.0, 0.0]** ; bandeau bleu conservé en l’absence de texte.

Si l’énumération échoue, `ffmpeg_has_filter` renvoie false et le moteur utilise le repli. T54 démontre deux exports valides dans ces cas ; **false indique alors une capacité non confirmée, pas la preuve d’un filtre absent du build**. Le JSON ne distingue pas ces deux causes. Le warning demandé est présent dans le rapport ; aucun affichage d’alerte de repli dans une GUI réelle n’est revendiqué.

Pour l’absence de scale, l’application conserve trois erreurs contenant le stade export, la source, la destination, la commande avec scale et le code 8. Elle ne persiste pas le stderr détaillé `No such filter`, car l’encodage utilise stderr DEVNULL. Le diagnostic exact du filtre absent est connu grâce à la simulation ; la preuve de traçabilité applicative porte sur la commande/code/source et l’absence de faux succès.

**Confirmations indépendantes**

| Contrôle | Preuve |
|---|---|
| C01 | Scan de **62 dossiers run**, lecture de **62 JSON** ; **72 entrées ok**, y compris le premier run T46 globalement failed et les trois sorties C07. Fichiers non vides, vidéo 1080×1920, **72 décodages complets code 0 avec stderr vide**. Schéma 0.6 et champ ffmpeg_capabilities dans chaque rapport. |
| C02 | MKV vidéo ~2 s/audio ~60 s : durée originale **2,023 s**, égale au maximum indépendant PTS + durée des paquets vidéo ; conteneur **60,023 s**. Source et export vidéo exploitables, start 0. |
| C03 | H.264 corrompu mais probe-able : vérificateur original en ValueError, décodage indépendant en échec, aucune entrée ok. |
| C04 | Snapshot original conservé malgré modification événement/partenaire/rushs/destination avant le worker différé : dossier/JSON/texte/source cohérents. |
| C05 | Construction et start en échec injecté avec variables Tcl réelles : aucune exception échappée, processing false, statut Erreur et appel Démarrage impossible, puis lancement d’un vrai thread autorisé. T45 démontre les reprises complètes et leur libération finale. |
| C06 | Payloads AAC corrompus : rejet original et erreur export, décodage complet indépendant en échec, aucune entrée ok. |
| C07 | Second chemin sans drawtext par exécutable CLI strict : son rejet drawtext code 8 est vérifié, puis trois rendus réels valides avec bandeau, capability false, warning explicite et trois décodages internes observés. |
| C08 | Filtre scale absent par exécutable CLI strict : trois rejets code 8, trois erreurs JSON, zéro export ok, processing false et progression arrêtée. |

**Inventaire des sorties contrôlées**

La suite laisse **77 MP4**, dont 69 ok et huit rejets ; C07 ajoute trois MP4 ok. Total des générations auditées : **80 fichiers MP4 restants**, **72 ok**, **8 exclus**. Les sorties de zéro octet sont supprimées et ne sont pas comptées.

Les huit rejets correspondent aux mauvaises dimensions T33, audio-only T34, texte invalide T35, H.264 corrompu T37, AAC corrompu T47 et trois H.264 corrompus sans drawtext T52. C08 ne laisse aucun MP4. Aucun fichier invalide n’est enregistré ok. Les 77 sorties de la suite sont probées et entièrement décodées par le harnais ; C01 redécode les 72 ok, y compris les trois confirmations CLI.

**Non-régressions des défauts antérieurs**

| Point | Preuves | Conclusion |
|---|---|---|
| MAJ-01 résiduel, MKV avec audio plus long | T29, T36, C02 | Non-régression : durée de sélection vidéo, un export vidéo exploitable. |
| MAJ-06, H.264 indécodable accepté | T37, T52, T99, C03 | Non-régression sur branche avec et sans texte : rejet des payloads corrompus, erreurs persistées, aucun faux ok. |
| MAJ-07, métadonnées désynchronisées | T24, T44, C04 | Non-régression : événement/partenaire/rushs/destination figés et cohérents. |
| MAJ-08, verrou conservé après échec de démarrage | T45, C05 | Non-régression : construction/start gérés, notification, processing false, nouvelle génération réelle réussie dans chaque sous-cas. |
| Deux demandes pendant un vrai worker actif | T28, T43 | Un seul worker, second appel refusé ; processing libéré après succès. |
| Erreur interne puis nouvelle génération | T21, T23, T38, T46 | Verrou libéré. T46 produit deux rapports, statut Erreur puis Terminé, deux exports valides et deux arrêts de progression. |
| Toutes sources inventoriées et poursuite après erreur | T04–T06, T19, T20, T39, T49 | Inventaire complet, erreurs par source/export, poursuite des autres rushs ; maximum trois exports par run. |
| Alias et déduplication temporelle | T02, T03, T07–T10, T26, T30, T31 | Écart minimal 12 s par source_id ; symlink/hardlink reconnus sur Linux. |
| Versionnement sans écrasement et collisions | T11, T23 | Dossiers distincts ; hashes MP4/TXT/JSON précédents inchangés ; retry et épuisement gérés. |
| Portraits, carré, paysage, MP4/MKV silencieux et AAC | T04, T15–T18, T29, T40 | Exports vidéo 1080×1920 décodables dans les cas exécutés. |
| Zéro export, corruption, génération partielle | T14, T19, T32–T35, T37, T41, T47, T51, T52 | Rapport et erreurs, pas d’annonce de Shorts prêts si aucun export ; fichiers de zéro octet supprimés. |

La déduplication est temporelle, pas sémantique : à 48 s, starts 3/15/27 et extraits de 18 s se chevauchent de 6 s, conformément au seuil de 12 s entre débuts. L’inventaire de quatre rushs avec trois Shorts ne prouve pas que chaque rush apparaît dans une sortie.

**Grille complète des 55 contrôles**

| Test | Scénario | Résultat observé |
|---|---|---|
| T01 | Syntaxe AST et import original | OK — syntaxe et import originaux ; APP_NAME = MVP 0.6. |
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
| T27 | Lanceur via sh depuis racine/app, exécution directe et README | ÉCHEC MINEUR MIN-03 — README encore MVP 0.5. Les deux commandes sh résolvent app.py correctement ; vrai Python atteint Tk puis échoue faute de DISPLAY. Mode Git 100644/0644 et PermissionError en exécution directe inchangés (MIN-02). |
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
| T48 | drawtext présent dans le build de référence ; chaîne de branding comparée à MVP 0.5 | OK — détecteur true, chaîne complète identique, trois exports H.264 1080×1920 valides, trois décodages internes, aucun warning de repli. |
| T49 | drawtext absent simulé ; quatre MP4 synthétiques 1920×1080 | OK — quatre sources inventoriées, trois candidats et trois exports valides ; scale/crop/drawbox sans texte, capability false, warning explicite, zéro erreur. |
| T50 | Bandeau sans drawtext sur une source noire ; contrôle de pixels | OK — drawbox dans la chaîne et image réellement décodée : moyenne bandeau RGB 0/19/66, zone basse 0/0/0. Un export valide. |
| T51 | Filtre scale indispensable annoncé absent et refusé | OK — trois tentatives et trois erreurs export avec commandes/code 8, zéro ok, no_usable_segment, warning, progression arrêtée et processing false. |
| T52 | Sans drawtext, trois payloads H.264 corrompus avant vérification | OK — trois vérifications originales puis rejets Décodage vidéo de contrôle échoué ; trois décodages indépendants en échec, aucune entrée ok. |
| T53 | Détecteur original sur flags, noms voisins, descriptions, retours et exceptions | OK — dix cas, zéro faux positif ; retour non nul ou exception donne false. |
| T54 | Énumération des filtres en erreur non nulle puis OSError injectée | OK — capability false et warning, filtre sans texte, un export valide par sous-cas ; erreur de détection traitée conservativement. |
| T99 | Contrôle transversal de tous les fichiers MP4 produits | OK — 77 MP4 probés/décodés, zéro invalide marqué ok. C01 scanne ensuite tous les rapports et confirme 72 exports ok valides, avec les trois sorties CLI C07. |

**Défauts critiques et majeurs**

Aucun défaut critique ou majeur reproduit dans cette campagne. L’absence d’un filtre indispensable n’est pas une défaillance du repli drawtext : c’est une condition externe impossible à compenser par la suppression du texte ; les tests démontrent son traitement sans faux succès.

**Mineur MIN-03 réouvert — README resté en MVP 0.5**

Localisation : `app/README.md`, **lignes 1 et 16**. `APP_NAME` et le schéma JSON sont 0.6 ; le README titre MVP 0.5 et emploie encore ce numéro dans la liste des fonctions absentes. Il ne documente pas le nouveau repli et son warning. Preuve : **T27**, lecture intégrale et blob Git `e316330a4ac587e2c7302c9d52ac9cf035a24dfe` inchangé depuis MVP 0.5.

Reproduction : lire le titre de app/README.md, comparer à APP_NAME et aux rapports schema_version 0.6. Le test de cohérence de version échoue sur `assertIn("MVP 0.6", readme)`. Les commandes sh documentées restent correctes.

Impact : version et comportement de branding non expliqués à l’utilisateur. Gravité mineure : aucun blocage d’export ni perte de données reproduit. Condition de levée : actualiser le README pour 0.6 et le repli, puis rejouer le contrôle documentaire. **Aucune modification de l’application effectuée par cet audit.**

**Mineur MIN-02 persistant — exécution directe du lanceur**

Mode Git **100644**, copie fidèle **0644**, exécution directe : **PermissionError**. Ce bit n’est pas déclaré corrigé.

| Commande | Répertoire | Résultat |
|---|---|---|
| `sh app/run_linux_mac.sh` | Racine | Chemin absolu app.py correct ; substitut Python code 0 ; vrai Python atteint Tk puis code 1 faute de DISPLAY. |
| `sh run_linux_mac.sh` | app/ | Même résolution et même limite d’affichage. |
| Exécution directe du script | Racine et app/ | PermissionError, mode 0644. |

Preuve : T27. Le mode Git est conservé ; le lanceur n’a pas été rendu exécutable par l’audit. La résolution via sh sur Linux ne prouve pas une recette graphique macOS.

**Limites et recette macOS requise**

Le mandat rapporte un démarrage de l’ancienne GUI 0.5 sur Mac. Il ne valide pas la GUI 0.6 ni ses nouveaux exports. T42 observe encore des appels d’UI depuis le worker avec des doubles. Le code appelle des interfaces d’UI avant le try de process (ligne 160) et lit le snapshot avant le try de run_thread (ligne 56). Aucun crash Tk ni absence de crash Tk n’est déclaré prouvé ici.

La recette à effectuer sur le Mac réel après cet audit :

1. Lancer le MVP 0.6 avec le même environnement Homebrew et les quatre rushs WhatsApp originaux.
2. Vérifier capability drawtext et warning du rapport ; en branche false, constater trois vidéos 1080×1920 décodables avec bandeau sans libellé.
3. Vérifier la progression, les dialogues et le statut dans une mainloop réelle, le refus d’un deuxième lancement et la reprise après erreur.
4. Contrôler humainement cadrage, audio, texte social et absence d’écrasement des générations ; essayer la fermeture pendant le traitement.

Les erreurs partielles restent tracées dans le JSON ; le dialogue final indique le nombre de sorties sans résumer toutes ces erreurs. Les sorties invalides non nulles restent sur disque mais sont exclues des exports ok.

**Portée produit et communication**

Le moteur conserve la sélection à fractions temporelles fixes 25/50/75 %, un recadrage central et un bandeau fixe. Le libellé LES SENTINELLES n’est ajouté que si drawtext est confirmé disponible. Les partenaires alimentent le texte social générique, sans gestion métier des contreparties.

Toujours absents et hors périmètre : transcription/sous-titres, scoring hockey intelligent, sélection multimodale, suivi intelligent 9:16, Sponsor Manager et reporting partenaire. Les dépendances déclarées ne prouvent pas leur intégration. Le rappel de validation humaine ne démontre pas un circuit éditorial complet. Audience, pertinence hockey, qualité sur un événement réel et temps bénévole économisé restent **à mesurer**.

**Décision finale**

**CANDIDAT** sur `2654cd76f32d602f2c42d7aa92a817cff4f3fb30`. Le repli drawtext, le maintien du bandeau, les métadonnées/warnings, les contrôles de sortie et les non-régressions moteur sont démontrés. Le seul échec de la suite est documentaire et mineur. Les **72 exports ok** sont décodables. **La recette GUI macOS doit être rejouée avant de prononcer VALIDÉ.** Aucun changement de main.

**Annexe — toutes les sorties restantes**

Les 80 fichiers sont identifiés ci-dessous. Le statut ok est retrouvé dans les rapports par C01. Les deux runs T46 sont distingués par leur statut global ; l’export valide du run failed est bien contrôlé.

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
| T48 | short_01_9x16.mp4 | 69596 | 1080×1920 | 2.000000 | 0 / stderr vide | ok |
| T48 | short_02_9x16.mp4 | 70385 | 1080×1920 | 2.000000 | 0 / stderr vide | ok |
| T48 | short_03_9x16.mp4 | 69540 | 1080×1920 | 2.000000 | 0 / stderr vide | ok |
| T49 | short_01_9x16.mp4 | 111758 | 1080×1920 | 2.000000 | 0 / stderr vide | ok |
| T49 | short_02_9x16.mp4 | 111402 | 1080×1920 | 2.000000 | 0 / stderr vide | ok |
| T49 | short_03_9x16.mp4 | 111507 | 1080×1920 | 2.000000 | 0 / stderr vide | ok |
| T50 | short_01_9x16.mp4 | 2332 | 1080×1920 | 2.000000 | 0 / stderr vide | ok |
| T52 | short_01_9x16.mp4 | 64999 | 1080×1920 | 2.000000 | 69 / erreurs | exclu |
| T52 | short_02_9x16.mp4 | 65776 | 1080×1920 | 2.000000 | 69 / erreurs | exclu |
| T52 | short_03_9x16.mp4 | 64915 | 1080×1920 | 2.000000 | 69 / erreurs | exclu |
| T54_probe_nonzero | short_01_9x16.mp4 | 64999 | 1080×1920 | 2.000000 | 0 / stderr vide | ok |
| T54_probe_exception | short_01_9x16.mp4 | 64999 | 1080×1920 | 2.000000 | 0 / stderr vide | ok |
| C07 | short_01_9x16.mp4 | 111758 | 1080×1920 | 2.000000 | 0 / stderr vide | ok |
| C07 | short_02_9x16.mp4 | 111402 | 1080×1920 | 2.000000 | 0 / stderr vide | ok |
| C07 | short_03_9x16.mp4 | 111507 | 1080×1920 | 2.000000 | 0 / stderr vide | ok |

**Annexe — empreintes de app/**

Inventaire, octets et modes Git conservés. Aucun fichier ajouté dans app/.

| Fichier | SHA-256 identique avant/après |
|---|---|
| app/README.md | `3692cc6e33b1e89b3f36e4df9072a7646abdedc6b06942d9723ca9181c824190` |
| app/ROADMAP.md | `e98b00f8ec9dc508fb675f01aa96bef1a86f181c465e8b760e66cae4e0fcd25b` |
| app/app.py | `e2958268e0e5a73ed29305b99c0c8151e201185de4dbb4bbdde49d3dd2601a62` |
| app/requirements.txt | `be654442659daf5deace60880d5b13bda39c702793ff78a0e6ea2ddd2e7ef64b` |
| app/run_linux_mac.sh | `dadf3dbd662f23326342ea15572f88c7529dea0b218613bdcaacbe1f77c3a236` |
| app/run_windows.bat | `92f53ecbc23b49cf50624c8de78dc5dbbb119237c1ac45fc03e0ff2dd3e76f5e` |

**Annexe — reproduction autonome**

Copier les deux blocs ci-dessous dans /tmp/audit_v06.py et /tmp/confirm_v06.py. Exécuter sur Linux, avec Python/Tk importable, FFmpeg/ffprobe, libx264, drawtext et drawbox pour le build de référence. Aucun paquet IA nécessaire. Le répertoire de résultats doit être neuf ; T27 suppose un environnement sans affichage.

```sh
git clone --branch develop https://github.com/noobstrade/sentinelles-content-factory.git /tmp/sentinelles-mvp06
git -C /tmp/sentinelles-mvp06 checkout --detach 2654cd76f32d602f2c42d7aa92a817cff4f3fb30
env -u DISPLAY PYTHONDONTWRITEBYTECODE=1 python3 /tmp/audit_v06.py /tmp/sentinelles-mvp06 /tmp/sentinelles-audit06-resultats-neufs
env -u DISPLAY PYTHONDONTWRITEBYTECODE=1 python3 /tmp/confirm_v06.py /tmp/sentinelles-mvp06 /tmp/sentinelles-audit06-resultats-neufs
```

Le premier script retourne **1 sur ce commit** pour le défaut documentaire T27, écrit néanmoins evidence.json et exécute les 55 contrôles. Lancer le second séparément : il ajoute les confirmations CLI, scanne tous les rapports/exports ok, écrit confirmations.json et retourne **0** lorsque ces confirmations sont établies.

Les deux scripts sont identiques aux fichiers réellement exécutés, vérifiés par comparaison textuelle, parse AST et SHA-256. Identités inode, timestamps, chemin du Python et hashes d’encodage peuvent varier ; dimensions, statuts, filtres, messages demandés et décodages constituent les critères reproductibles. Les simulations de filtres ne prétendent pas être un build Homebrew.

| Script exécuté et reproduit ci-dessous | SHA-256 |
|---|---|
| audit_v06.py | `8613a254c990bd7984923a1b18b0f2b07dc09e3ccd1db6895f04a1cd97cbea05` |
| confirm_v06.py | `27d44e477c397b73cb236a8b822d678b4af420419e70598d6cf585bae451f6b3` |

| Trace de cette exécution | SHA-256 |
|---|---|
| test_run_v06.log | `b3d685c5a4246c5d1c9aeb46e8d78e2886197fd175e13e9cae3d89c36773f8d3` |
| confirm_run_v06.log | `e8691129c66c0c0b2ac82681a8d5bd3fa5568cb99d5f6c42cefc05a1e60278f6` |
| execution_v06/evidence.json | `3bc66dd99d2b8bce0bbe17510e13dcf03938148aca7672d3f6041168867154d6` |
| execution_v06/confirmations.json | `b24db4a2138a3ed3a19fede93676e57c73e29beea0596cc161d4ac4f39a1ffb7` |
| execution_v06/cli_absent.jsonl | `76f3fd2c47c89b47d9c8b8b95fb127f157ba5fea7e485d6eafe75bcf9b3154bb` |
| execution_v06/cli_missing_scale.jsonl | `b76afa5a17db3b2abf8e664b3b58194a2bd0028c02780be3742eeea9a8cb7473` |
| execution_v06/ffmpeg_cli_shim/ffmpeg | `7f7baabc1e4e49ad9337ed83d634b894b929861b32eaba1abf3ced4adbacd79c` |

**Code de audit_v06.py**

```python
"""Independent MVP 0.6 audit. No application file is modified.
Usage: PYTHONDONTWRITEBYTECODE=1 python3 audit_v06.py /path/to/repo /new/output/dir
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
for i in range(1,5):
    FILES['wa'+str(i)]=generate('wa'+str(i),'1920x1080',2,2,(i-1)*90)
FILES['black']=FIXTURES/'black.mp4'
REAL_RUN(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','lavfi','-i',
          'color=c=black:size=320x180:rate=2:duration=2','-c:v','libx264','-pix_fmt','yuv420p',
          str(FILES['black'])],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)


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
    for name in ['event_slug','source_id','probe_source','build_candidates','select_candidates','ffmpeg_has_filter','verify_export']:
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
            render_failure=None,publication_failure=False,driver=None,before_render=None,capability_mode=None):
    output=Path(output or ROOT/identifier)
    if not output.exists(): output.mkdir(parents=True)
    x=runner(output,files,event)
    if driver is None:x.processing=True
    messages=[];commands=[];escaped=None;filter_probes=[];verification_commands=[];simulated_rejections=[]
    before_dirs=set(output.rglob('run_*')) if output.is_dir() else set()
    write_text=Path.write_text
    def run(cmd,*args,**kwargs):
        if cmd[0]=='ffmpeg' and '-filters' in cmd:
            if capability_mode=='probe_exception':
                filter_probes.append({'command':cmd[:],'mode':capability_mode,'exception':'OSError injected'})
                raise OSError('audit injection: filter enumeration unavailable')
            result=REAL_RUN(cmd,*args,**kwargs)
            if capability_mode=='absent':
                result.stdout='\n'.join(line for line in result.stdout.splitlines() if line.split()[1:2]!=['drawtext'])+'\n'
            elif capability_mode=='missing_scale':
                result.stdout='\n'.join(line for line in result.stdout.splitlines() if line.split()[1:2]!=['scale'])+'\n'
            elif capability_mode=='probe_nonzero':
                result.returncode=9
            selected=[line for line in result.stdout.splitlines() if line.split()[1:2] in
                      [['drawtext'],['drawbox'],['scale'],['crop']]]
            filter_probes.append({'command':cmd[:],'mode':capability_mode,'returncode':result.returncode,
                                  'selected_lines':selected})
            return result
        is_render=cmd[0]=='ffmpeg' and '-c:v' in cmd and '-vf' in cmd
        if cmd[0]=='ffmpeg' and not is_render and '-map' in cmd and '-f' in cmd and cmd[-1]=='-':
            verification_commands.append(cmd[:])
        if is_render:
            commands.append(cmd[:])
            if before_render:before_render(x,cmd)
            vf=cmd[cmd.index('-vf')+1]
            names=[part.split('=',1)[0] for part in vf.split(',')]
            missing=('drawtext' if capability_mode=='absent' and 'drawtext' in names else
                     'scale' if capability_mode=='missing_scale' and 'scale' in names else None)
            if missing:
                Path(cmd[-1]).write_bytes(b'')
                simulated_rejections.append({'filter':missing,'command':cmd[:],'returncode':8,
                                             'stderr':"No such filter: '"+missing+"'"})
                raise subprocess.CalledProcessError(8,cmd,stderr="No such filter: '"+missing+"'")
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
              'reports':reports,'commands':commands,'report':report,'publication':copy,'outputs':exports,
              'capability_mode':capability_mode,'filter_probes':filter_probes,
              'verification_commands':verification_commands,'simulated_rejections':simulated_rejections}
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
        self.assertEqual(r['report']['schema_version'],'0.6')
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
        self.assertEqual(module.APP_NAME,'Sentinelles Content Factory MVP 0.6')
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
        EVIDENCE['T27']={'mode':oct(script.stat().st_mode&0o777),'launches':launches,
                         'readme_heading':readme.splitlines()[0],'expected_app_version':'MVP 0.6',
                         'readme_matches_current_version':'MVP 0.6' in readme,
                         'gui_startup':'not available: no DISPLAY'}
        for expected in ['sh app/run_linux_mac.sh','sh run_linux_mac.sh',
                         'échec de démarrage du worker','Fonctions encore absentes']:
            self.assertIn(expected,readme)
        self.assertIn('MVP 0.6',readme,'MIN-03: README does not match the audited MVP 0.6')

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

    def assert_capability(self,r,expected):
        self.assertEqual(r['report']['ffmpeg_capabilities'],{'drawtext':expected})
        warnings=r['report'].get('warnings',[])
        if expected:
            self.assertEqual(warnings,[])
        else:
            self.assertEqual(warnings,['FFmpeg sans drawtext : bandeau graphique conservé, libellé texte omis.'])
        self.assertEqual(len(r['filter_probes']),r['progress_starts'])
        for cmd in r['commands']:
            vf=cmd[cmd.index('-vf')+1]
            self.assertIn('scale=1080:1920:force_original_aspect_ratio=increase',vf)
            self.assertIn('crop=1080:1920:(iw-1080)/2:(ih-1920)/2',vf)
            self.assertIn('drawbox=x=0:y=0:w=iw:h=150:color=0x081B4B@0.82:t=fill',vf)
            self.assertEqual('drawtext=' in vf,expected)

    def test_T48_drawtext_present_preserves_exact_branding_chain(self):
        self.assertTrue(App.ffmpeg_has_filter('drawtext'),'Reference Linux build must provide drawtext')
        r=execute('T48',['r1','r2','r3'],capability_mode='present')
        self.assert_render_ok(r,3);self.assert_capability(r,True)
        old_vf=("scale=1080:1920:force_original_aspect_ratio=increase,"
                "crop=1080:1920:(iw-1080)/2:(ih-1920)/2,"
                "drawbox=x=0:y=0:w=iw:h=150:color=0x081B4B@0.82:t=fill,"
                "drawtext=text='LES SENTINELLES':x=(w-text_w)/2:y=45:fontsize=54:fontcolor=white")
        self.assertTrue(all(cmd[cmd.index('-vf')+1]==old_vf for cmd in r['commands']))
        self.assertEqual(len(r['verification_commands']),3)

    def test_T49_without_drawtext_four_1080p_inputs_three_valid_exports(self):
        r=execute('T49',['wa1','wa2','wa3','wa4'],capability_mode='absent')
        self.assert_render_ok(r,3);self.assert_capability(r,False)
        self.assertEqual(len(r['report']['sources']),4)
        self.assertEqual(len(r['report']['candidates']),3)
        self.assertTrue(all((s['width'],s['height'])==(1920,1080) for s in r['report']['sources']))
        self.assertEqual([e['source'] for e in r['report']['exports']],r['inputs'][:3])
        self.assertEqual(r['report']['errors'],[])
        self.assertEqual(r['simulated_rejections'],[])
        self.assertEqual(len(r['verification_commands']),3)
        self.assertFalse(any('drawtext' in line for line in r['filter_probes'][0]['selected_lines']))

    def test_T50_without_drawtext_drawbox_chain_and_actual_pixels(self):
        r=execute('T50',['black'],capability_mode='absent')
        self.assert_render_ok(r,1);self.assert_capability(r,False)
        output=r['outputs'][0]['file']
        decoded=REAL_RUN(['ffmpeg','-v','error','-i',output,'-frames:v','1','-f','rawvideo','-pix_fmt','rgb24','-'],
                         stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True)
        pixels=decoded.stdout;self.assertEqual(len(pixels),1080*1920*3)
        def average(y):
            points=[pixels[(row*1080+column)*3:(row*1080+column)*3+3]
                    for row in range(y,y+10) for column in range(10,20)]
            return [sum(point[channel] for point in points)/len(points) for channel in range(3)]
        top=average(10);body=average(200)
        self.assertGreater(top[2],top[0]+20)
        self.assertGreater(top[2],25)
        self.assertLessEqual(max(body),6)
        EVIDENCE['T50']['pixel_check']={'first_frame_rgb_sha256':hashlib.sha256(pixels).hexdigest(),
                                      'top_mean_rgb':top,'body_mean_rgb':body,
                                      'result':'blue band remains on black source without drawtext'}

    def test_T51_missing_indispensable_scale_fails_cleanly_and_is_reported(self):
        r=execute('T51',['r1','r2','r3'],capability_mode='missing_scale')
        self.assert_no_output(r);self.assert_capability(r,True)
        self.assertEqual(len(r['commands']),3)
        self.assertEqual(len(r['simulated_rejections']),3)
        self.assertTrue(all(item['filter']=='scale' and item['returncode']==8 for item in r['simulated_rejections']))
        self.assertEqual(len(r['report']['errors']),3)
        self.assertTrue(all(error['stage']=='export' and 'scale=' in error['error'] and 'exit status 8' in error['error']
                            for error in r['report']['errors']))
        self.assertEqual(r['outputs'],[])
        self.assertEqual(r['verification_commands'],[])

    def test_T52_without_drawtext_corrupt_video_is_never_registered_ok(self):
        def corrupt(x,cmd):corrupt_packets(Path(cmd[-1]))
        r=execute('T52',['r1','r2','r3'],hook=corrupt,capability_mode='absent')
        self.assert_no_output(r);self.assert_capability(r,False)
        self.assertEqual(len(r['outputs']),3);self.assertEqual(len(r['verification_commands']),3)
        self.assertTrue(all(item['decode']['returncode']!=0 for item in r['outputs']))
        self.assertEqual(len(r['report']['errors']),3)
        self.assertTrue(all(error['error']=='Décodage vidéo de contrôle échoué' for error in r['report']['errors']))

    def test_T53_filter_detector_parses_flags_exact_names_and_errors(self):
        cases=[
            (' ... drawtext V->V text\n',0,True),
            (' T.C drawtext V->V text\n',0,True),
            ('  TS. drawtext V->V text\n',0,True),
            ('Filters:\n ... drawtext V->V text\n',0,True),
            (' ... adrawtext V->V text\n',0,False),
            (' ... drawbox V->V mentions drawtext in description\n',0,False),
            ('Filters:\n V = Video\n',0,False),
            ('',0,False),
            (' ... drawtext V->V text\n',8,False),
        ]
        records=[]
        for stdout,code,expected in cases:
            result=subprocess.CompletedProcess(['ffmpeg','-hide_banner','-filters'],code,stdout,'')
            with patch.object(module.subprocess,'run',return_value=result) as calls:
                actual=App.ffmpeg_has_filter('drawtext')
            self.assertEqual(actual,expected);self.assertEqual(calls.call_count,1)
            records.append({'stdout':stdout,'returncode':code,'expected':expected,'actual':actual})
        with patch.object(module.subprocess,'run',side_effect=OSError('audit injection: unavailable')) as calls:
            actual=App.ffmpeg_has_filter('drawtext')
        self.assertFalse(actual);self.assertEqual(calls.call_count,1)
        EVIDENCE['T53']={'cases':records,'exception_case':{'type':'OSError','result':actual},
                         'total_cases':len(records)+1}

    def test_T54_filter_probe_failure_degrades_without_losing_exports(self):
        observations=[]
        for mode in ['probe_nonzero','probe_exception']:
            with self.subTest(mode=mode):
                r=execute('T54_'+mode,['r1'],capability_mode=mode)
                self.assert_render_ok(r,1);self.assert_capability(r,False)
                self.assertEqual(r['report']['errors'],[])
                self.assertEqual(len(r['verification_commands']),1)
                observations.append({'mode':mode,'exports':len(r['report']['exports']),
                                     'capability':r['report']['ffmpeg_capabilities'],'warnings':r['report']['warnings']})
        EVIDENCE['T54']={'cases':observations,'note':'detection failure conservatively treated as drawtext unavailable'}

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

**Code de confirm_v06.py**

```python
"""Independent confirmations for the exact MVP 0.6 snapshot."""
import hashlib,importlib.util,json,subprocess,sys,os,shutil
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
sys.dont_write_bytecode=True
repo=Path(sys.argv[1]).resolve();root=Path(sys.argv[2]).resolve()
spec=importlib.util.spec_from_file_location('v06_confirmed_app',repo/'app/app.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
data=json.loads((root/'evidence.json').read_text())['evidence']
def decode(path,video_only=False):
    cmd=['ffmpeg','-v','error','-i',str(path)]
    if video_only:cmd+=['-map','0:v:0']
    cmd+=['-f','null','-']
    p=subprocess.run(cmd,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,text=True)
    return {'returncode':p.returncode,'stderr':p.stderr}
before={str(p.relative_to(repo)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (repo/'app').rglob('*') if p.is_file()}
# Independent CLI simulation: actual subprocesses, no patch to ffmpeg_has_filter or subprocess.run.
real_ffmpeg=shutil.which('ffmpeg')
shim_dir=root/'ffmpeg_cli_shim';shim_dir.mkdir(exist_ok=True)
shim=shim_dir/'ffmpeg'
shim_body=r"""import os,sys,json,subprocess
from pathlib import Path
real=REAL_FFMPEG_PATH
args=sys.argv[1:]
profile=os.environ.get('SENTINELLES_FILTER_PROFILE','absent')
log=Path(os.environ['SENTINELLES_FFMPEG_LOG'])
phase='filters' if '-filters' in args else 'render' if '-c:v' in args and '-vf' in args else 'decode_or_other'
missing=None
if '-vf' in args:
    names=[part.split('=',1)[0] for part in args[args.index('-vf')+1].split(',')]
    if profile=='absent' and 'drawtext' in names:missing='drawtext'
    if profile=='missing_scale' and 'scale' in names:missing='scale'
with log.open('a') as stream:
    stream.write(json.dumps({'args':args,'profile':profile,'phase':phase,'rejected_filter':missing})+'\n')
if '-filters' in args:
    result=subprocess.run([real,*args],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    banned='drawtext' if profile=='absent' else 'scale'
    stdout='\n'.join(line for line in result.stdout.splitlines() if line.split()[1:2]!=[banned])+'\n'
    sys.stdout.write(stdout);sys.stderr.write(result.stderr);sys.exit(result.returncode)
if missing:
    sys.stderr.write("No such filter: '"+missing+"'\n")
    sys.exit(8)
os.execv(real,[real,*args])
"""
shim_body=shim_body.replace('REAL_FFMPEG_PATH',repr(real_ffmpeg))
shim.write_text('#!'+sys.executable+'\n'+shim_body)
shim.chmod(0o755)
class CliValue:
    def __init__(self,value):self.value=value
    def get(self):return self.value
    def set(self,value):self.value=value
class CliProgress:
    def __init__(self):self.starts=0;self.stops=0;self.active=False
    def start(self,n):self.starts+=1;self.active=True
    def stop(self):self.stops+=1;self.active=False
def cli_run(profile):
    output=root/('cli_'+profile);output.mkdir()
    inputs=[str(root/'fixtures'/('wa'+str(i)+'.mp4')) for i in range(1,5)]
    x=SimpleNamespace(processing=True,files=inputs,output=output,event=CliValue('Confirmation CLI '+profile),
                      sponsor=CliValue('Partenaire'),status=CliValue('Prêt'),progress=CliProgress())
    for name in ['event_slug','source_id','probe_source','build_candidates','select_candidates',
                 'ffmpeg_has_filter','verify_export']:
        setattr(x,name,getattr(m.App,name))
    x.new_run_dir=lambda:m.App.new_run_dir(x)
    log=root/('cli_'+profile+'.jsonl')
    messages=[];guard=None
    env={'PATH':str(shim_dir)+os.pathsep+os.environ['PATH'],'SENTINELLES_FILTER_PROFILE':profile,
         'SENTINELLES_FFMPEG_LOG':str(log)}
    with patch.dict(os.environ,env), \
         patch.object(m.messagebox,'showinfo',side_effect=lambda *args:messages.append(['info',*args])), \
         patch.object(m.messagebox,'showwarning',side_effect=lambda *args:messages.append(['warning',*args])), \
         patch.object(m.messagebox,'showerror',side_effect=lambda *args:messages.append(['error',*args])):
        if profile=='absent':
            result=subprocess.run(['ffmpeg','-hide_banner','-i',inputs[0],'-vf','drawtext=text=AUDIT','-f','null','-'],
                                  stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,text=True)
            guard={'returncode':result.returncode,'stderr':result.stderr}
            assert guard=={'returncode':8,'stderr':"No such filter: 'drawtext'\n"}
        m.App.process(x)
    assert x.processing is False and x.progress.active is False
    assert x.progress.starts==x.progress.stops==1
    runs_cli=list(output.rglob('run_*'));assert len(runs_cli)==1
    report=json.loads((runs_cli[0]/'rapport.json').read_text())
    calls=[json.loads(line) for line in log.read_text().splitlines()]
    renders=[call for call in calls if call['phase']=='render']
    assert len(renders)==3
    assert len(report['sources'])==4 and len(report['candidates'])==3
    if profile=='absent':
        assert report['status']=='completed' and len(report['exports'])==3 and report['errors']==[]
        assert report['ffmpeg_capabilities']=={'drawtext':False}
        assert report['warnings']==['FFmpeg sans drawtext : bandeau graphique conservé, libellé texte omis.']
        assert all(call['rejected_filter'] is None for call in renders)
        assert all('drawtext=' not in call['args'][call['args'].index('-vf')+1] and
                   'drawbox=' in call['args'][call['args'].index('-vf')+1] for call in renders)
        verify_calls=[call for call in calls if '-map' in call['args'] and '0:v:0' in call['args']
                      and '-c:v' not in call['args']]
        assert len(verify_calls)==3
    else:
        assert report['status']=='no_usable_segment' and report['exports']==[]
        assert report['ffmpeg_capabilities']=={'drawtext':True}
        assert len(report['errors'])==3
        assert all(error['stage']=='export' and 'exit status 8' in error['error'] and 'scale=' in error['error']
                   for error in report['errors'])
        assert all(call['rejected_filter']=='scale' for call in renders)
        assert list(runs_cli[0].glob('*.mp4'))==[]
        assert any(message[0]=='warning' and message[1]=='Aucun Short' for message in messages)
    return {'profile':profile,'real_ffmpeg':real_ffmpeg,'strict_drawtext_guard':guard,
            'run_dir':str(runs_cli[0]),'report':report,'calls':calls,'messages':messages,
            'processing_after':x.processing,'progress_starts':x.progress.starts,'progress_stops':x.progress.stops}
c7={'id':'C07','method':'external CLI shim hides and rejects drawtext; actual encoding and verification subprocesses',
    'result':cli_run('absent')}
c8={'id':'C08','method':'external CLI shim hides and rejects indispensable scale',
    'result':cli_run('missing_scale')}
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
    assert item['bytes']>0
    checks.append(item)
c1={'id':'C01','created_run_dirs':len(runs),'parsed_reports':len(reports),
    'actual_status_ok_count':len(checks),'all_status_ok_decode_checks':checks,
    'capability_fields_present':all('ffmpeg_capabilities' in report for report in reports),
    'schema_versions':sorted({report['schema_version'] for report in reports})}
assert c1['capability_fields_present'] and c1['schema_versions']==['0.6']
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
out={'confirmations':[c1,c2,c3,c4,c5,c6,c7,c8],'app_unchanged':before==after}
(root/'confirmations.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
print(json.dumps({'created_run_dirs':len(runs),'reports':len(reports),'status_ok_count':len(checks),
                  'mk_video_duration':c2['original_probe_source']['duration'],'mkv_container_duration':c2['container_duration'],
                  'h264_gate_error':c3['original_verify_export']['error'],'startup_fault':c5,
                  'audio_corruption_gate_error':c6['original_verify_export']['error'],
                  'external_cli_fallback':{'exports':len(c7['result']['report']['exports']),
                                           'capability':c7['result']['report']['ffmpeg_capabilities'],
                                           'strict_guard':c7['result']['strict_drawtext_guard']},
                  'external_cli_missing_scale':{'exports':len(c8['result']['report']['exports']),
                                                'errors':len(c8['result']['report']['errors'])},
                  'app_unchanged':before==after},ensure_ascii=False,indent=2))

```

