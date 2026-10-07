# À AUDITER — MVP 0.3

## Cible
Branche `develop`. Auditer le HEAD contenant le correctif post-audit MVP 0.2.

## Mission
Audit indépendant sans modifier `app/`.

## Régressions historiques à rejouer
- multi-rush ;
- déduplication temporelle ;
- générations successives sans écrasement.

## Défauts MAJEURS du précédent audit à rejouer impérativement
1. MAJ-01 / T17 : vidéo 2 s + audio 60 s. Aucun faux Short audio-only ne doit être annoncé.
2. MAJ-02 / T09 : portrait 80x160 (1:2), plus 9:16 et paysage. Les exports doivent rester 1080x1920 avec flux vidéo.
3. MAJ-03 : événement 300 caractères, destination invalide et collision de run. Aucune exception non gérée ; progression arrêtée.
4. MAJ-04 / T10-T15 : rush corrompu au milieu et échec d'un export. Le traitement des autres rushs doit continuer autant que possible et `rapport.json` doit conserver sources, erreurs et exports valides.
5. MAJ-05 / T11-T16 : même fichier via chemin réel + symlink. Il doit être reconnu comme même source et ne pas produire deux clips identiques.
6. MIN-01 : zéro export doit être présenté comme « aucun segment exploitable », jamais « prêt à valider ».

## Contrôles supplémentaires
- Source sans audio : doit pouvoir produire une vidéo.
- Vérifier que la durée utilisée pour la sélection correspond au flux vidéo, pas au conteneur/audio.
- Vérifier chaque export avec ffprobe + décodage FFmpeg.
- Vérifier les dimensions 1080x1920.
- Vérifier qu'un export invalide/0 octet n'est jamais enregistré comme `status: ok`.
- Vérifier que le rapport JSON existe sur toute exécution où un run_dir a pu être créé.
- Rejouer la grille combinatoire du sélecteur adaptée à `source_id`.
- Examiner les risques Tk/thread sans les déclarer corrigés sans reproduction.

## Fonctions toujours hors périmètre
Ne pas déclarer présentes : transcription/sous-titres, scoring hockey intelligent, sélection multimodale, suivi intelligent 9:16, Sponsor Manager, reporting partenaire.

## Livrable
Remplacer `worker/RESULTAT_AUDIT.md`, committer sur `develop`, fournir commit audité + commit rapport + verdict BLOQUÉ/CANDIDAT/VALIDÉ.
