# À AUDITER — MVP 0.5

Auditer le HEAD de `develop` sans modifier `app/`.

Rejouer l'intégralité de la campagne MVP 0.4 : 48 tests, grilles T02/T03, contrôles C01–C06 et décodage intégral de tous les exports déclarés ok.

## Blocage MVP 0.4 à lever
MAJ-08 / T45 / C05 : injecter un échec de construction ou de `Thread.start()`. Aucun RuntimeError ne doit s'échapper de `run_thread`, `processing` doit revenir à false, une erreur utilisateur doit être signalée, puis un lancement suivant doit être autorisé.

Conserver les non-régressions T43 (second lancement refusé pendant un worker actif) et T46 (verrou libéré après erreur interne puis génération suivante réussie).

## Mineurs à vérifier
- Lanceur Linux/macOS utilisable depuis la racine via `sh app/run_linux_mac.sh` et depuis `app/` via `sh run_linux_mac.sh`.
- README cohérent avec MVP 0.5.
- Ne pas considérer le bit exécutable comme corrigé si GitHub ne le conserve pas : distinguer exécution directe et exécution via `sh`.

## Verdict
BLOQUÉ si un défaut majeur reproductible subsiste. CANDIDAT si moteur conforme mais essais GUI réels restent nécessaires. VALIDÉ uniquement si les preuves demandées justifient ce terme.

Remplacer `worker/RESULTAT_AUDIT.md`, committer le rapport sur `develop`, fournir commit audité + commit rapport.
