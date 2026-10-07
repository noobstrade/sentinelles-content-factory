# À AUDITER — MVP 0.6

Auditer le HEAD de `develop` sans modifier `app/`.

## Contexte terrain macOS
Le MVP 0.5 a démarré correctement sur un Mac réel (Python Homebrew 3.14.6, Tk 9.1, FFmpeg Homebrew 9.0.2). Quatre MP4 WhatsApp 1920x1080 ont été correctement probés et trois candidats sélectionnés, mais les trois exports ont échoué avec FFmpeg exit status 8.

Diagnostic terrain reproduit par :
`ffmpeg -hide_banner -filters | grep drawtext`
Aucune sortie : le build FFmpeg Homebrew standard testé ne fournit pas `drawtext`.

## Correctif MVP 0.6 à vérifier
- détection de la capacité FFmpeg `drawtext` ;
- si disponible : comportement de branding antérieur ;
- si absent : export doit continuer avec scale + crop + drawbox, sans texte ;
- `rapport.json` doit tracer `ffmpeg_capabilities.drawtext` ;
- si absent, le rapport doit contenir un warning explicite ;
- aucun export ne doit être déclaré ok sans le contrôle ffprobe + décodage intégral existant.

## Régression obligatoire
Rejouer toute la campagne MVP 0.5, y compris les 48 contrôles précédemment passés.

Ajouter au minimum :
1. simulation/build FFmpeg avec drawtext présent ;
2. simulation/build FFmpeg sans drawtext : 3 exports valides 1080x1920 doivent pouvoir être produits ;
3. vérifier que le bandeau drawbox reste présent dans la chaîne de filtre sans drawtext ;
4. vérifier qu'une absence d'un filtre réellement indispensable échoue proprement et est tracée ;
5. vérifier le rapport/warning/capability ;
6. décoder intégralement chaque export déclaré `ok`.

## Point de vigilance
La validation GUI macOS terrain devra être rejouée après audit. Ne pas déclarer le produit validé uniquement sur tests synthétiques.

## Hors périmètre
Toujours absents : transcription/sous-titres, scoring hockey intelligent, sélection multimodale, suivi intelligent 9:16, Sponsor Manager, reporting partenaire.

## Livrable
Remplacer `worker/RESULTAT_AUDIT.md`, commit sur `develop`, fournir commit audité, preuves et verdict BLOQUÉ/CANDIDAT/VALIDÉ.
