# Sentinelles Content Factory — MVP 0.5

Prototype local-first de génération assistée de Shorts pour Les Sentinelles.

## Fiabilité acquise dans les audits précédents
- tous les rushs sont inventoriés et les erreurs d'une source n'arrêtent pas les autres ;
- sélection round-robin et déduplication temporelle par identité physique de source ;
- générations versionnées sans écrasement ;
- rapports JSON persistants, y compris lors d'exécutions partielles ;
- durée fondée sur le flux vidéo, y compris les MKV testés avec audio plus long ;
- exports 1080×1920 contrôlés par ffprobe puis décodage FFmpeg complet ;
- snapshot événement/partenaire/rushs/destination figé au lancement ;
- un seul traitement simultané ; le verrou est libéré après succès, erreur interne ou échec de démarrage du worker.

## Fonctions encore absentes
Le MVP 0.5 ne prétend pas encore fournir : scoring hockey intelligent, PySceneDetect branché au pipeline, transcription faster-whisper, sous-titres, vision locale, suivi intelligent 9:16, Sponsor Manager ou reporting partenaire.

## Installation
Python 3.11+ et FFmpeg/ffprobe dans le PATH.

Windows : lancer `run_windows.bat`.
Linux/macOS : `sh app/run_linux_mac.sh` depuis la racine du dépôt, ou `sh run_linux_mac.sh` depuis `app/`.
Alternative : `python app/app.py` depuis la racine.

## Règle
Validation humaine obligatoire avant publication.
