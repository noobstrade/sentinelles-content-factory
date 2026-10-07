# Workflow GitHub

## Branches
- `main` : version validée.
- `develop` : intégration et corrections en cours.
- branches `fix/*` ou `feature/*` : changements isolés si nécessaire.

## Boucle de travail
1. Une version candidate est placée sur `develop`.
2. `worker/A_AUDITER.md` décrit le périmètre à contrôler.
3. Le Worker audite le commit exact.
4. Le Worker dépose son résultat dans `worker/RESULTAT_AUDIT.md` et/ou dans des issues.
5. Les défauts sont reproduits puis corrigés.
6. Les tests de non-régression sont exécutés.
7. Un nouvel audit est demandé.
8. `main` n'est mise à jour qu'après validation.

## Règle de preuve
Ne jamais écrire « corrigé », « validé » ou « testé » sans identifier le test ou la preuve correspondante.
