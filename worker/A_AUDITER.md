# À AUDITER — MVP 0.2

## Cible
Branche : `develop`
Application : `app/app.py`

## Mission
Auditer sans modifier le code sauf demande explicite.

## Régressions à vérifier en priorité
1. Avec 3 rushs ou plus, les 3 premiers Shorts doivent provenir de rushs distincts si chaque rush est exploitable.
2. Avec 1 ou 2 rushs, aucun candidat sélectionné ne doit être un quasi-doublon temporel du même rush (écart minimal actuel : 12 s).
3. Deux générations successives du même événement doivent créer deux dossiers `run_*` distincts et ne rien écraser.
4. `rapport.json` doit inventorier tous les rushs et tracer chaque export vers sa source, son start et sa durée.
5. Vérifier les vidéos très courtes et les noms d'événements atypiques.

## Important
Ne pas déclarer présents : sous-titres, scoring hockey intelligent, sélection multimodale, Sponsor Manager ou reporting partenaire. Ces fonctions restent à implémenter.

## Rapport
Remplacer `worker/RESULTAT_AUDIT.md` par : commit audité, environnement, tests, CRITIQUES/MAJEURS/MINEURS, reproduction, preuves et verdict BLOQUÉ/CANDIDAT/VALIDÉ.
