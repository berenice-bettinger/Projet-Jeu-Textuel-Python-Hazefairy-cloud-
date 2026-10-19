# Hazefairy-Cloud - Jeu d'Aventure et de Quêtes en Python

Projet développé dans le cadre de la formation d'ingénieur à l'ESIEE Paris.

---

## Présentation du Projet

 Hazefairy-Cloud  est un jeu d'aventure textuel et graphique fondé sur la programmation orientée objet. Le joueur incarne une princesse dans un royaume médiéval fantastique affecté par la malédiction d'un sorcier. L'objectif est d'explorer le monde, de résoudre des quêtes auprès de différents PNJ, de gérer son inventaire et de découvrir le secret du sorcier pour restaurer la paix.

Le projet propose une double interface d'utilisation :
1. Interface Graphique (GUI Tkinter) : Affichage dynamique des décors, boutons d'action rapides et console intégrée.
2. Mode Console (CLI) : Mode texte classique fonctionnant dans un terminal standard.

---

## Fonctionnalités Principales

- Navigation et exploration : Système de lieux interconnectés avec suivi d'historique et gestion de retour arrière (commandes `go`, `back`, `history`).
- Gestionnaire de quêtes (QuestManager) : Suivi des quêtes principales et secondaires, validation dynamique des objectifs et attribution de récompenses.
- Inventaire et gestion de poids : Prise en compte de la capacité d'emport du joueur, ramassage et dépôt d'objets (`take`, `drop`, `inventory`).
- Objet téléporteur (Beamer) : Dispositif magique permettant d'enregistrer des emplacements et de s'y téléporter (`charge`, `fire`).
- Personnages non-joueurs (PNJ) : Interactions avec des PNJ statiques ou mobiles se déplaçant de manière autonome sur la carte.

---

## Stack Technique et Architecture

- Langage : Python 3
- Interface graphique : Tkinter (Canvas, Grid Layout, redirection de flux stdout)
- Concepts de programmation :
  - Programmation Orientée Objet (POO) : Encapsulation, héritage et modularité répartis sur plus de 10 classes.
  - Pattern Command : Découplage de la saisie utilisateur et des traitements exécutés.
  - Gestion d'états : Sauvegarde et restauration dynamique de l'état du jeu pour la commande `back`.

---

## Structure du Projet

```text
├── game.py          # Boucle principale, configuration et interface Tkinter
├── actions.py       # Implémentation des actions du jeu
├── player.py        # Classe Player (inventaire, poids, positions)
├── room.py          # Classe Room (sorties, objets, visuels)
├── quests.py        # Gestion des quêtes et objectifs
├── item.py          # Classe de base des objets
├── beamer.py        # Objet de téléportation
├── command.py       # Structure des commandes
├── character1.py    # Personnages mobiles
├── character2.py    # Personnages statiques
└── assets/          # Images des pièces et icônes
Installation et Lancement
Prérequis
Python 3.10 ou supérieur.

Lancement du jeu
Cloner le dépôt :

Bash
git clone [https://github.com/berenice-bettinger/python-text-adventure-game.git](https://github.com/berenice-bettinger/python-text-adventure-game.git)
cd python-text-adventure-game
Lancer en mode Graphique (GUI) :

Bash
python game.py
Lancer en mode Console (CLI) :

Bash
python game.py --cli
Démonstration
(Glissez-déposez ici votre vidéo démonstrative ou votre capture d'écran sur GitHub)

Auteurs et Crédits
Projet réalisé en binôme dans le cadre de la formation d'ingénieur à l'ESIEE Paris :
Bérénice BETTINGER
Camille PUYRAJOU
