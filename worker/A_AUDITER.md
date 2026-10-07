# À AUDITER — MVP 0.4

Auditer le HEAD de `develop` sans modifier `app/`.

## Rejouer toute la régression MVP 0.3
Rejouer notamment les 43 tests du rapport précédent et la grille combinatoire.

## Blocages à lever
- MAJ-01 résiduel / T36 : MKV avec vidéo ~2 s et audio ~60 s. La durée de sélection doit provenir de la timeline vidéo, pas du conteneur.
- MAJ-06 / T37-T99 : un H.264 structurellement probe-able mais indécodable ne doit jamais être enregistré `status: ok`.
- MAJ-07 / T24 : modifier événement/partenaire pendant le rendu ne doit jamais désynchroniser dossier, JSON et texte de publication.

## Durcissements à contrôler
- Deux appels `run_thread` pendant une génération : le second doit être refusé.
- Contrôler qu'après succès ou erreur le verrou `processing` est libéré.
- Vérifier MP4/MKV, vidéo silencieuse, portrait, paysage, corruption, source absente et génération partielle.
- Décoder intégralement chaque export déclaré `ok`.

## Hors périmètre
Toujours absents : transcription/sous-titres, scoring hockey intelligent, sélection multimodale, suivi intelligent 9:16, Sponsor Manager, reporting partenaire.

## Livrable
Remplacer `worker/RESULTAT_AUDIT.md`, commit sur `develop`, fournir commit audité, preuves et verdict BLOQUÉ/CANDIDAT/VALIDÉ.
