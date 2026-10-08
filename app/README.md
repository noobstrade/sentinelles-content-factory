# Sentinelles Content Factory — MVP 0.6

Prototype local-first de génération assistée de Shorts pour Les Sentinelles.

## État de validation
Audit indépendant MVP 0.6 : **CANDIDAT**, 54 contrôles réussis sur 55. Le seul échec concerne l'ancien intitulé du présent README. La recette sur le Mac réel et ses rushs WhatsApp reste à confirmer ; ne pas qualifier cette version de VALIDÉE avant cette recette.

## Fiabilité contrôlée
- tous les rushs sont inventoriés ; une source défectueuse ne bloque pas les autres ;
- sélection round-robin, maximum trois extraits, déduplication temporelle par identité de source ;
- générations versionnées sans écrasement et rapports JSON, y compris lors des échecs ;
- durée fondée sur le flux vidéo, y compris les MKV avec audio plus long ;
- exports 1080×1920 vérifiés par ffprobe et décodage FFmpeg ;
- snapshot événement/partenaire/rushs/destination au lancement ;
- verrou contre les traitements simultanés, libéré après erreur ;
- détection du filtre FFmpeg `drawtext` : s'il manque, export avec bandeau `drawbox` mais **sans libellé texte** ; capability et avertissement dans `rapport.json`.

## Limites actuelles
Les extraits sont choisis selon des positions temporelles, **pas** par reconnaissance des actions de hockey. Le 9:16 est un recadrage central, sans suivi de palet ou de joueur. Pas encore de PySceneDetect intégré, faster-whisper, sous-titres, vision locale, Sponsor Manager ou reporting partenaire.

## Installation
Python 3.11+ avec Tkinter fonctionnel, FFmpeg et ffprobe accessibles dans le PATH.

Sur macOS Homebrew : vérifier `/opt/homebrew/bin/python3 -c "import tkinter; print(tkinter.TkVersion)"`.

Windows : `run_windows.bat`.
Linux/macOS : `sh app/run_linux_mac.sh` depuis la racine du dépôt ou `sh run_linux_mac.sh` depuis `app/`. L'exécution directe du script n'est pas encore prise en charge par le mode Git 100644.
Alternative macOS depuis la racine : `/opt/homebrew/bin/python3 app/app.py`.

## Recette macOS requise
1. `cd ~/Desktop/sentinelles-content-factory && git pull origin develop`
2. `/opt/homebrew/bin/python3 app/app.py`
3. Importer les quatre MP4 WhatsApp du test précédent, choisir une destination puis générer.
4. Vérifier trois fichiers MP4 lisibles, cadrage 1080×1920 et bandeau bleu ; sans drawtext, le titre est volontairement absent.
5. Vérifier `rapport.json` : `status`, `exports`, `errors`, `ffmpeg_capabilities`, `warnings`.
6. Conserver le rapport et les éventuels messages d'erreur pour l'analyse. Ne pas publier automatiquement.

## Règle
Validation humaine obligatoire avant toute publication. Aucun changement sur `main` sans recette et validation.
