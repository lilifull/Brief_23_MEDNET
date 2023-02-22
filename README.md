Bienvenu dans mon application de prédiction !

Cette application permet de prédire les organes sur des images de radiographie.
Elle repose sur un réseau neuronal convolutif entrainé et testé en amont sur un dataset de 48 000 images.
Son score de prédiction est de 99,93% (score = accuracy).
Les formats d'image accéptés sont les .png et les .jpeg.
La prédiction a de très bon résultats avec les images du dataset.
Il possible de prédire des images provenant d'internet ou d'autres sources.
Seulement les prédictiond donnent de moins bon résultat si l'image est trop éloigée du dataset d'entrainement de l'IA.

Pour utiliser cette application, suivre ces étapes :

1) faire un git clone à partir de ce repository :

  - git clone https://github.com/lilifull/Brief_23_MEDNET.git

2) aller dans le dossier app

3) installer les librairies nécaissaires au fonctionnement de l'app à partir du fichier requirements.txt :

  - pip install -r requirements.txt

4) lancer l'application, il y a le choix entre deux méthodes :

  - en ligne de commande:
    - flask --app mednet_app run --debug
    - python -m flask --app mednet_app --debug run
  
  - avec l'exécusion de ce script python:
    - python app.py
