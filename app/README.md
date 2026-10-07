# Sentinelles Content Factory — MVP 0.2

Base issue du MVP 0.1 fourni le 7 octobre 2026.

## Correctifs structurels 0.2
- tous les rushs importés sont inventoriés et alimentent le pool de candidats ;
- sélection initiale en round-robin entre les rushs ;
- déduplication temporelle des candidats issus d'un même rush ;
- chaque génération possède un dossier `run_<timestamp>` distinct ;
- le rapport JSON trace la source, le début et la durée de chaque export.

## Fonctions encore absentes
Le MVP 0.2 ne prétend pas encore fournir : scoring hockey intelligent, PySceneDetect réellement branché au pipeline, transcription faster-whisper, sous-titres, vision locale, suivi intelligent 9:16, Sponsor Manager ou reporting partenaire.

## Installation
Python 3.11+ et FFmpeg/ffprobe dans le PATH. Lancer `python app.py`.

## Règle
Validation humaine obligatoire avant publication.
