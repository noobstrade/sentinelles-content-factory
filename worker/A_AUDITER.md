# À AUDITER

## Mission
Auditer la version présente sur la branche `develop` sans modifier le code sauf demande explicite.

## Méthode obligatoire
- Reproduire chaque défaut avant de le déclarer confirmé.
- Classer : CRITIQUE / MAJEUR / MINEUR.
- Donner les étapes de reproduction et les preuves.
- Identifier le commit audité et l'environnement de test.
- Écrire le rapport dans `worker/RESULTAT_AUDIT.md`.
- Si possible, créer une issue GitHub par défaut confirmé.

## Priorités actuelles
1. Tous les rushs d'un événement doivent être exploités, pas uniquement le premier.
2. Éviter les clips identiques ou quasi-identiques.
3. Ne jamais écraser silencieusement une génération précédente.
4. Vérifier l'isolation et le versionnement par événement.
5. Vérifier ensuite transcription/sous-titres, sélection intelligente et reporting partenaires.

## Contrainte produit
Objectif à mesurer, et non promesse validée : communication humaine <= 90 min/semaine et <= 30 min/jour hors tournage.
