# Description: Game class
# Import modules
from room import Room
from item import Item
from beamer import Beamer
from player import Player
from command import Command
from actions import Actions
from character1 import Character
from character2 import Character2
from quests import Quest
import copy
from pathlib import Path
import sys
import time
import tkinter as tk
from tkinter import ttk, simpledialog


# Toggle debugging messages across modules. Import this variable from other modules
# as: `from game import DEBUG` and guard debug prints with `if DEBUG: ...`
DEBUG = False
 
class Game:

    # Constructor
    def __init__(self):
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.player = None
        self.history = []
        self.gui = None  # Reference to GUI window (None in CLI mode)
    
    # Setup the game
    def setup(self, player_name=None):

        # Setup commands

        help = Command("help", " : afficher cette aide", Actions.help, 0)
        self.commands["help"] = help
        quit = Command("quit", " : quitter le jeu", Actions.quit, 0)
        self.commands["quit"] = quit
        go = Command("go", " <direction> : se déplacer dans une direction cardinale (N, E, S, O, U, D)", Actions.go, 1)
        self.commands["go"] = go
        look = Command("look", " : regarder la pièce (liste des objets présents)", Actions.look, 0)
        self.commands["look"] = look
        history = Command("history", " : afficher l'historique des pièces visitées", Actions.history, 0)
        self.commands["history"] = history
        back = Command("back", " : revenir à la pièce précédente", Actions.back, 0)
        self.commands["back"] = back
        inventory = Command("inventory", " : afficher l'inventaire du joueur", Actions.inventory, 0)
        self.commands["inventory"] = inventory
        take = Command("take", " <item_name> : prendre un objet dans la pièce", Actions.take, 1)
        self.commands["take"] = take
        drop = Command("drop", " <item_name> : déposer un objet de l'inventaire dans la pièce", Actions.drop, 1)
        self.commands["drop"] = drop
        check = Command("check", " : examiner l'inventaire du joueur", Actions.check, 0)
        self.commands["check"] = check
        charge = Command("charge", " <slot_name> : charger le beamer dans un slot nommé", Actions.charge, 1)
        self.commands["charge"] = charge
        fire = Command("fire", " <slot_name> : téléporter le joueur vers le slot nommé", Actions.fire, 1)
        self.commands["fire"] = fire
        characters = Command("characters", " : lister les personnages présents dans la pièce", Actions.characters, 0)
        self.commands["characters"] = characters
        talk = Command("talk", " <character_name> : parler à un personnage dans la pièce", Actions.talk, 1)
        self.commands["talk"] = talk
        list_beamer = Command("list_beamer", " : lister les slots du beamer", Actions.list_beamer, 0)
        self.commands["list_beamer"] = list_beamer

        # questes commands
        self.commands["quests"] = Command("quests"
                                          , " : afficher la liste des quêtes"
                                          , Actions.quests
                                          , 0)
        self.commands["quest"] = Command("quest"
                                         , " <titre> : afficher les détails d'une quête"
                                         , Actions.quest
                                         , 1)
        self.commands["activate"] = Command("activate"
                                            , " <titre> : activer une quête"
                                            , Actions.activate
                                            , 1)
        self.commands["rewards"] = Command("rewards"
                                           , " : afficher vos récompenses"
                                           , Actions.rewards
                                           , 0)
        # Setup rooms

        chambre = Room("Chambre", "votre chambre.", image = "chambre.png")
        self.rooms.append(chambre)
        penderie = Room("Penderie", "votre penderie.", image = "penderie.png")
        self.rooms.append(penderie)
        couloir = Room("Couloir", "un couloir de votre château.", image = "couloir.png")
        self.rooms.append(couloir)
        cuisine = Room("Cuisine", "la cuisine de votre château.", image = "cuisine.png")
        self.rooms.append(cuisine)
        bibliotheque = Room("Bibliothèque", "la bibliothèque du château.", image = "bibliotheque.png")
        self.rooms.append(bibliotheque)
        chateau = Room("Chateau", "la cour du château.", image = "chateau.png")
        self.rooms.append(chateau)
        foret = Room("Forêt enchantée", "une forêt enchantée, peuplée d'animaux extraordianires.", image = "foret.png")
        self.rooms.append(foret)
        village = Room("Village", "un village paisible.", image = "village.png")
        self.rooms.append(village)
        ruines = Room("Ruines", "les ruines d'un ancien temple.", image = "ruines.png")
        self.rooms.append(ruines)
        pont = Room("Pont", "sur un ponton. Vous contemplez la mer à perte de vue.", image = "pont.png")
        self.rooms.append(pont)
        grotte = Room("Grotte", "une grotte sombre et sinueuse.", image = "grotte.png")
        self.rooms.append(grotte)
        mer = Room("Mer", "une mer calme et paisible.", image = "mer.png")
        self.rooms.append(mer)
        montagne = Room("Montagne", "les montagnes du royaume.", image = "montagne.png")
        self.rooms.append(montagne)
        cristaux = Room("Cristaux", "une grotte de cristal. Un dragon apparaît devant vous. Montez sur son dos !", image = "cristaux.png")
        self.rooms.append(cristaux)
        ciel = Room("Ciel", "les airs ! Vous vous dirigez en direction du repère du sorcier à dos de dragon.", image = "ciel.png")
        self.rooms.append(ciel)
        repere = Room("Repère du sorcier", "le repère du sorcier...", image = "repere.png")
        self.rooms.append(repere)
        fontaine = Room("Fontaine", "une fontaine magique.", image = "fontaine.png")
        self.rooms.append(fontaine)
        Maison_du_sage = Room("Maison du sage", "la maison du sage.", image = "maison_du_sage.png")
        self.rooms.append(Maison_du_sage)
        Le_jardin = Room("Le jardin du jardinier", "un jardin rempli de plante et de fruit et légumes.", image = "le_jardin.png")
        self.rooms.append(Le_jardin)
        L_épicerie = Room("L'épicerie", " Le lieux de travail d'Elra qui vend toute sorte d'herbe et potions.", image = "l_epicerie.png")
        self.rooms.append(L_épicerie)
        sous_sol_du_sorcier = Room("Sous-sol du sorcier", "le sous-sol du sorcier, rempli de potions et ingrédients mystérieux.", image = "sous_sol_du_sorcier.png")
        self.rooms.append(sous_sol_du_sorcier)
        bibliothèque_du_sorcier = Room("Bibliothèque du sorcier", "la bibliothèque du sorcier, remplie de livres anciens et de parchemins magiques.", image = "bibliothèque_du_sorcier.png")
        self.rooms.append(bibliothèque_du_sorcier)
        couloir_du_sorcier = Room("Couloir du sorcier", "le couloir du sorcier, menant à différentes pièces mystérieuses.", image = "couloir_du_sorcier.png")
        self.rooms.append(couloir_du_sorcier)
        salle_de_rituel = Room("Salle de rituel", "la salle de rituel du sorcier, où des cérémonies magiques ont lieu.", image = "salle_de_rituel.png")
        self.rooms.append(salle_de_rituel)

        # Create exits for rooms

        chambre.exits = {"N" : None, "E" : penderie, "S" : None, "O" : None, "U" : None, "D" : couloir} 
        penderie.exits = {"N" : None, "E" : None, "S" : None, "O" : chambre, "U" : None, "D" : None}
        couloir.exits = {"N" : None, "E" : cuisine, "S" : chateau, "O" : bibliotheque, "U" : chambre, "D" : None}
        cuisine.exits = {"N" : None, "E" : None, "S" : None, "O" : couloir, "U" : None, "D" : None}
        bibliotheque.exits = {"N" : None, "E" : couloir, "S" : None, "O" : None, "U" : None, "D" : None}
        chateau.exits = {"N" : couloir, "E" : None, "S" : foret, "O" : None, "U" : None, "D" : None}
        foret.exits = {"N" : chateau, "E" : None, "S" : fontaine, "O" : None, "U" : None, "D" : None}
        fontaine.exits = {"N" : foret, "E" : ruines, "S" : pont, "O" : village, "U" : None, "D" : None}
        village.exits = {"N" : L_épicerie, "E" : fontaine, "S" : Le_jardin, "O" : Maison_du_sage, "U" : None, "D" : None}
        Le_jardin.exits = {"N" : village, "E" : None, "S" : None, "O" : None, "U" : None, "D" : None}
        L_épicerie.exits ={"N" : None, "E" : None, "S" : village, "O" : None, "U" : None, "D" : None}
        Maison_du_sage.exits = {"N" : None, "E" : village, "S" : None, "O" : None, "U" : None, "D" : None}
        ruines.exits = {"N" : None, "E" : grotte, "S" : montagne, "O" : fontaine, "U" : None, "D" : None}
        pont.exits = {"N" : fontaine, "E" : None, "S" : None, "O" : None, "U" : mer, "D" : None}
        grotte.exits = {"N" : None, "E" : None, "S" : None, "O" : None, "U" : None, "D" : None}
        montagne.exits = {"N" : None, "E" : cristaux, "S" : None, "O" : None, "U" : None, "D" : None}
        cristaux.exits = {"N" : None, "E" : None, "S" : None, "O" : None, "U" : ciel, "D" : None}
        ciel.exits = {"N" : None, "E" : None, "S" : None, "O" : None, "U" : None, "D" : repere}
        repere.exits = {"N" : None, "E" : None, "S" : couloir_du_sorcier, "O" : None, "U" : None, "D" : None}
        mer.exits = {"N" : None, "E" : None, "S" : None, "O" : None, "U" : None, "D" : montagne}
        couloir_du_sorcier.exits = {"N" : None, "E" : bibliothèque_du_sorcier, "S" : sous_sol_du_sorcier, "O" : salle_de_rituel, "U" : None, "D" : None}
        sous_sol_du_sorcier.exits = {"N" : couloir_du_sorcier, "E" : None, "S" : None, "O" : None, "U" : None, "D" : None}
        salle_de_rituel.exits = {"N" : None, "E" : None, "S" : None, "O" : None, "U" : None, "D" : None}
        bibliothèque_du_sorcier.exits = {"N" : None, "E" : None, "S" : None, "O" : couloir_du_sorcier, "U" : None, "D" : None}
 
        # Setup player and starting room

        if player_name:
            self.player = Player(player_name)
        else:
            self.player = Player(input("\nEntrez votre nom: "))
        self.player.current_room = chambre 

        # Setup all quests
        self._set_quests()
        
        # Activate main quest at start
        self.player.quest_manager.activate_quest("Vaincre le Sorcier")

        # Set up objets in rooms
        diary = Item("diary", "votre carnet relié en cuir. ", 0.7)
        chambre.item[diary.name] = diary
        # Quelques objets supplémentaires répartis sur la map
        sac = Item("sac", "un sac à dos pour commencer votre aventure.", 0.8)
        penderie.item[sac.name] = sac
        pomme = Item("pomme", "une pomme rouge et juteuse.", 0.2)
        cuisine.item[pomme.name] = pomme
        livre = Item("livre", "un vieux grimoire poussiéreux.", 1.2)
        bibliotheque.item[livre.name] = livre
        baguette = Item("Baguette", "une baguette de pain chaud sortie du four.", 0.3)
        cuisine.item[baguette.name] = baguette
        # Placer un Beamer (avec comportements de charge / fire) dans le château
        beamer = Beamer("beamer", "un beamer magique pour vous téléporter. Charger-le dans un lieu pour vous téléporter dans ce lieu à partir d'un autre endroit.", 2)
        chateau.item[beamer.name] = beamer
        artefact = Item("artefact", "un artefact ancien et mystérieux.", 0.9)
        ruines.item[artefact.name] = artefact
        gemme = Item("gemme", "une gemme brillante aux reflets multicolores.", 0.1)
        cristaux.item[gemme.name] = gemme
        pendantif = Item("pendantif", "un pendentif en or orné d'une pierre précieuse se trouve au fond de l'eau.", 0.4)
        pont.item[pendantif.name] = pendantif
        # Cela serait bien que cela soit un PNJ enfant qui donne la peluche au joueur dans le village. Prendre en compte le cas où le sac est déjà rempli (poid 2.5Kg).
        peluche = Item("peluche", "une peluche douce en forme de dragon.", 0.1)
        village.item[peluche.name] = peluche
        oeuf_de_dragon = Item("oeuf de dragon", "un œuf de dragon chaud au toucher.", 2)
        foret.item[oeuf_de_dragon.name] = oeuf_de_dragon
        corne_de_licorne = Item("corne de licorne", "une corne de licorne scintillante. La légende raconte qu'elle porterai bonheur...", 0.3)
        foret.item[corne_de_licorne.name] = corne_de_licorne
        livre_de_sorts = Item("livre de sorts", "un livre de sorts magiques.", 1.5)
        repere.item[livre_de_sorts.name] = livre_de_sorts
        objet_brise = Item("objet_brisé", "un objet ancien brisé, fait de pierre et de métal.", 1.0)
        inscription_effacee = Item("inscription_effacée", "une pierre avec une inscription effacée.", 0.3)
        fragment_ancien = Item("fragment_ancien", "un fragment ancien marqué de runes mystiques.", 0.5)
        foret.item[objet_brise.name] = objet_brise
        village.item[inscription_effacee.name] = inscription_effacee
        foret.item[fragment_ancien.name] = fragment_ancien
        # --- Plantes magiques ---
        plante_magique1 = Item("plante_magique", "Une plante rare aux propriétés curatives.", 0.2)
        plante_magique2 = Item("plante_magique2", "Une autre plante rare aux propriétés curatives.", 0.2)
        foret.item[plante_magique1.name] = plante_magique1
        Le_jardin.item[plante_magique2.name] = plante_magique2
        # --- Souvenirs du royaume ---
        souvenir1 = Item("pierre_gravée", "Une pierre gravée d'un symbole ancien.", 0.3)
        souvenir2 = Item("coquillage_bleu", "Un coquillage bleu brillant provenant de la mer.", 0.1)
        souvenir3 = Item("plume_dorée", "Une plume dorée provenant d'un oiseau légendaire.", 0.1)
        # Placement des souvenirs
        ruines.item[souvenir1.name] = souvenir1
        pont.item[souvenir2.name] = souvenir2
        village.item[souvenir3.name] = souvenir3

        # Characters
        garde = Character2("Garde", "un garde vigilant protégeant le château.", chateau, ["Bonjour votre majesté !", "Tout est en ordre dans le château."])
        chateau.item[garde.name] = garde
        bibliothecaire = Character2("Bibliothécaire", "un vieux bibliothécaire avec une longue barbe blanche.", bibliotheque, ["Chut ! C'est une bibliothèque.", "Avez-vous besoin d'aide pour trouver un livre ?"])
        bibliotheque.item[bibliothecaire.name] = bibliothecaire
        cuisinière= Character2 ("Cuisinière", "Une femme âgée qui cuisine dans la cuisine.", cuisine, ["Bonjour ! Que voulez-vous manger aujourd'hui ?", "J'ai préparé un délicieux repas pour vous."])
        cuisine.item[cuisinière.name]= cuisinière
        lutin = Character("Lutin", "un petit lutin espiègle avec un chapeau pointu.", foret, ["Bienvenue dans la forêt enchantée !", "Faites attention aux créatures magiques."])
        foret.item[lutin.name] = lutin
        le_sage = Character("Le_sage", "un vieil homme sage avec une longue barbe grise.", Maison_du_sage, ["Vous avez fait un long voyage pour arriver ici.", "La sagesse est la clé de nombreux mystères."])
        Maison_du_sage.item[le_sage.name] = le_sage
        Cylian = Character2("Cylian", "un grand dragon rouge avec des écailles étincelantes.", ciel, ["Rohouuuuu ! Je suis le gardien des airs.", "Monte sur mon dos pour un voyage inoubliable !"])
        ciel.item[Cylian.name] = Cylian
        Zeph = Character2("Zeph", "un sorcier mystérieux vêtu d'une robe sombre.", salle_de_rituel, ["Vous avez réussi à me trouver.", "Le véritable pouvoir réside en vous."])
        salle_de_rituel.item[Zeph.name] = Zeph
        Willow = Character("Willow", "une petite fée lumineuse avec des ailes scintillantes.", cristaux, ["Bienvenue dans la grotte de cristal.", "La magie est partout autour de nous."])
        cristaux.item[Willow.name] = Willow
        pêcheur = Character2("Pêcheur", "un pêcheur robuste qui vend des bateaux.", pont, ["La mer est calme aujourd'hui.", "Vous voulez acheter un bateau ?"])
        pont.item[pêcheur.name] = pêcheur
        Elra = Character2("Elra", "une jeune Herboriste.", village, ["Salut ! Je fournis toujours pleins de potion pour être prêt pour l'aventures.", "As-tu entendu parler des ruines anciennes ?"])
        village.item[Elra.name] = Elra
        Sully = Character("Sully", "un animal fantastique fidèle au joueur.", chambre, ["Je suis prêt pour l'aventure !", "N'oublie pas de me nourrir."])
        couloir.item[Sully.name] = Sully
        Villageois1 = Character2("Villageois1", "la piplette du village qui absorbe tout votre temps.", village, ["Bonjour ! Comment se passe votre journée ?", "Avez-vous entendu parler des rumeurs du village ?"])
        village.item[Villageois1.name] = Villageois1
        Villageois2 = Character2("Villageois2", "L'historien du village, il vous raccontera des histoires.", village, ["Salut ! J'ai une histoire incroyable à te raconter.", "Le village est plein de mystères."])
        village.item[Villageois2.name] = Villageois2
        Villageois3 = Character2("Villageois3", "Le guide du village  qui aime aider les voyageurs.", village, ["Bonjour ! Comment puis-je vous aider aujourd'hui ?", "Le village est un endroit accueillant."])
        village.item[Villageois3.name] = Villageois3
        Villageois4 = Character2("Villageois4", "une petite fille qui aime chanter des chansons.", village, ["Salut ! Voulez-vous entendre une chanson ?", "La musique est la langue universelle."])
        village.item[Villageois4.name] = Villageois4
        Villageois5 = Character2("Villageois5", "Le jardinier qui aime les plantes et la végetation.", village, ["Bonjour ! Avez-vous besoin de conseils sur le jardinage ?", "Les plantes sont mes amies."])
        village.item[Villageois5.name] = Villageois5
        esprit = Character2("Esprit", "un esprit ancien qui hante les ruines.", ruines,["Pour ouvrir la porte sacrée, trouve les trois fragments perdus..."])
        ruines.item[esprit.name] = esprit

    def _set_quests (self):   
        """Initialize all quests."""
        
        # Main quest
        main_quest = Quest(
        title="Vaincre le Sorcier",
        description="Affrontez le sorcier maléfique et mettez fin à son règne.",
        objectives=["Atteindre le repère du sorcier", "Vaincre le sorcier"],
        reward="Victoire du royaume"
        )
        self.player.quest_manager.add_quest(main_quest)
        
        # Money quest
        money_quest = Quest(
        title="Financer le voyage",
        description="Gagnez assez d'écus pour acheter un bateau.",
        objectives=["Gagner 60 écus"],
        reward="Accès au bateau"
        )
        self.player.quest_manager.add_quest(money_quest)
        
        # Sorcerer secret quest (conditional - appears when talking to Zeph)
        sorcerer_secret_quest = Quest(
        title="Le Secret du Sorcier",
        description="Découvrez le secret caché du sorcier Zeph.",
        objectives=["Découvrir le secret de Zeph"],
        reward="Connaissance ancestrale"
        )
        self.player.quest_manager.add_quest(sorcerer_secret_quest)

        # Ruins quest
        ruins_quest = Quest(
        title="La Clé des Ruines",
        description="Trouvez les trois fragments nécessaires pour ouvrir la porte des ruines.",
        objectives=["objet_brisé", "inscription_effacée", "fragment_ancien"],
        reward="Clé des ruines"
        )
        self.player.quest_manager.add_quest(ruins_quest)

       # --- Mini-quête : Rencontrer les habitants ---
        talk_quest = Quest(
        title="Rencontrer les habitants",
        description="Parlez à 5 personnes du royaume.",
        objectives=["Parler à 5 PNJ"],
        reward="20 écus"
        )
        self.player.quest_manager.add_quest(talk_quest)

        # --- Mini-quête : Collecte de plantes ---
        plants_quest = Quest(
            title="Collecte de plantes",
            description="Récupérez une plante magique dans la nature.",
            objectives=["Récupérer plante"],
            reward="30 écus"
        )
        self.player.quest_manager.add_quest(plants_quest)

        # --- Mini-quête : Obtenir le beamer ---
        beamer_quest = Quest(
            title="Obtenir le beamer",
            description="Trouvez et prenez le beamer magique.",
            objectives=["Prendre beamer"],
            reward="30 écus"
        )
        self.player.quest_manager.add_quest(beamer_quest)

        # --- Mini-quête : Souvenirs ---
        souvenir_quest = Quest(
            title="Souvenirs du royaume",
            description="Trouvez trois objets souvenirs.",
            objectives=["pierre_gravée", "coquillage_bleu", "plume_dorée"],
            reward="30 écus"
        )
        self.player.quest_manager.add_quest(souvenir_quest)



    # Play the game
    def play(self):
        self.setup()
        self.print_welcome()
        # Loop until the game is finished
        while not self.finished:
            # Get the command from the player
            self.process_command(input("> "))
        try:
            print("\nFermeture du jeu dans 5 secondes...\n")
            sys.stdout.flush()
            time.sleep(5)
        except Exception:
            pass
        return None

    # Process the command entered by the player
    def process_command(self, command_string) -> None:

        # Split the command string into a list of words
        list_of_words = command_string.split(" ")
        # Optional debug output for developers
        if DEBUG:
            try:
                print("DEBUG: process_command: ", list_of_words)
            except Exception:
                pass

        command_word = list_of_words[0]

        # If the command is not recognized, print an error message
        if command_word not in self.commands.keys() and command_word != "":
            print(f"\nCommande '{command_word}' non reconnue. Entrez 'help' pour voir la liste des commandes disponibles.\n")
        # If the command is recognized, execute it
        elif command_word == "":
            self.process_command(input("> "))
        else:
            command = self.commands[command_word]
            previous_room = None
            try:
                previous_room = self.player.current_room
            except Exception:
                previous_room = None

            try:
                command.action(self, list_of_words, command.number_of_parameters)
                if DEBUG:
                    try:
                        print(f"DEBUG: executed command '{command_word}'")
                    except Exception:
                        pass
            except Exception:
                pass

            # Faire avancer les PNJ uniquement si le joueur a changé de pièce
            try:
                if self.player and self.player.current_room is not previous_room:
                    self.tick_npcs()
            except Exception:
                pass

    # Print the welcome message
    def print_welcome(self):
        print(f"\nBienvenue {self.player.name} dans ce jeu d'aventure ! Vous êtes une princesse dans un royaume médiéval fantastique et un sorcier maléfique a jeté une malédiction sur votre royaume ! Parviendrez-vous à le vaincre et à restaurer la paix ?\n")
        print("Entrez 'help' si vous avez besoin d'aide.")

        # Affiche la description courte de la pièce de départ (sans la liste d'objets).
        print(self.player.current_room.get_short_description())

    def save_state(self):
        snapshot = {
            "player": copy.deepcopy(self.player),
            "rooms": copy.deepcopy(self.rooms)
        }
        self.history.append(snapshot)

    def restore_state(self):
        if self.history:
            snapshot = self.history.pop()
            self.player = snapshot["player"]
            self.rooms = snapshot["rooms"]
            # Restaurer l'état sans afficher automatiquement l'inventaire de la pièce.
            print(self.player.current_room.get_short_description())
        else:
            print("\nAucune pièce précédente dans l'historique.\n")

    def tick_npcs(self):
        """Fait tenter un déplacement à tous les PNJ du jeu.

        Si un PNJ part de / arrive dans la pièce du joueur, affiche
        un petit message pour que le joueur le remarque.
        """
        npcs = []
        for room in self.rooms:
            for obj in list(room.item.values()):
                # import local to avoid circular import issues
                try:
                    from character1 import Character 
                    from character2 import Character2
                except Exception:
                    Character = None
                    Character2 = None
                if Character or Character2 and isinstance(obj, Character or Character2):
                    npcs.append(obj)

        for npc in npcs:
            old_room = npc.current_room
            moved = False
            try:
                moved = npc.move()
            except Exception:
                moved = False

 
##############################
# Tkinter GUI Implementation #
##############################

class _StdoutRedirector:
    """Redirect sys.stdout writes into a Tkinter Text widget."""
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, msg):
        """Write message to the Text widget."""
        if msg:
            self.text_widget.configure(state="normal")
            self.text_widget.insert("end", msg)
            self.text_widget.see("end")
            self.text_widget.configure(state="disabled")

    def flush(self):
        """Flush method required by sys.stdout interface (no-op for Text widget)."""


class GameGUI(tk.Tk):
    """Tkinter GUI for the text-based adventure game.

    Layout layers:
    L3 (top): Split into left image area (600x400) and right buttons.
    L2 (middle): Scrolling terminal output.
    L1 (bottom): Command entry field.
    """

    IMAGE_WIDTH = 600
    IMAGE_HEIGHT = 400

    def __init__(self):
        super().__init__()
        self.title("TBA")
        self.geometry("900x700")  # Provide enough space
        self.minsize(900, 650)

        # Underlying game logic instance
        self.game = Game()
        self.game.gui = self  # Link GUI to game for access in actions

        # Ask player name via dialog (fallback to 'Joueur')
        name = simpledialog.askstring("Nom", "Entrez votre nom:", parent=self)
        if not name:
            name = "Joueur"
        self.game.setup(player_name=name)  # Pass name to avoid double prompt

        # Build UI layers
        self._build_layout()

        # Redirect stdout so game prints appear in terminal output area
        self.original_stdout = sys.stdout
        sys.stdout = _StdoutRedirector(self.text_output)

        # Print welcome text in GUI
        self.game.print_welcome()

        # Load initial room image
        self._update_room_image()

        # Handle window close
        self.protocol("WM_DELETE_WINDOW", self._on_close)


    # -------- Layout construction --------
    def _build_layout(self):
        # Configure root grid: 3 rows (L3, L2, L1)
        self.grid_rowconfigure(0, weight=0)  # Image/buttons fixed height
        self.grid_rowconfigure(1, weight=1)  # Terminal output expands
        self.grid_rowconfigure(2, weight=0)  # Entry fixed
        self.grid_columnconfigure(0, weight=1)

        # L3 Top frame
        top_frame = ttk.Frame(self)
        top_frame.grid(row=0, column=0, sticky="nsew", padx=6, pady=(6,3))
        top_frame.grid_columnconfigure(0, weight=0)
        top_frame.grid_columnconfigure(1, weight=1)

        # L3L Image area (left)
        image_frame = ttk.Frame(top_frame, width=self.IMAGE_WIDTH, height=self.IMAGE_HEIGHT)
        image_frame.grid(row=0, column=0, sticky="nw", padx=(0,6))
        image_frame.grid_propagate(False)  # Keep requested size
        self.canvas = tk.Canvas(image_frame,
                                width=self.IMAGE_WIDTH,
                                height=self.IMAGE_HEIGHT,
                                bg="#222")
        self.canvas.pack(fill="both", expand=True)

        # Initialize image reference (will be loaded by _update_room_image)
        self._image_ref = "chambre.png"  # Keep reference to prevent garbage collection
        # Initial image will be loaded after welcome message

        # L3R Buttons area (right)
        buttons_frame = ttk.Frame(top_frame)
        buttons_frame.grid(row=0, column=1, sticky="ne")
        for i in range(10):
            buttons_frame.grid_rowconfigure(i, weight=0)
        buttons_frame.grid_columnconfigure(0, weight=0)
        buttons_frame.grid_columnconfigure(1, weight=0)

        # Load button images (keep references to prevent garbage collection)
        assets_dir = Path(__file__).parent / 'assets'
        # Load pre-resized 50x50 PNG images for better quality
        self._btn_help = tk.PhotoImage(file=str(assets_dir / 'help-50.png'))
        self._btn_nord = tk.PhotoImage(file=str(assets_dir / 'up-arrow-50.png'))
        self._btn_sud = tk.PhotoImage(file=str(assets_dir / 'down-arrow-50.png'))
        self._btn_ouest = tk.PhotoImage(file=str(assets_dir / 'left-arrow-50.png'))
        self._btn_est = tk.PhotoImage(file=str(assets_dir / 'right-arrow-50.png'))
        self._btn_quit = tk.PhotoImage(file=str(assets_dir / 'quit-50.png'))
        self._btn_up = tk.PhotoImage(file=str(assets_dir / 'up-arrow-50.png'))
        self._btn_down = tk.PhotoImage(file=str(assets_dir / 'down-arrow-50.png'))
        self._btn_sac = tk.PhotoImage(file=str(assets_dir / 'sac.png'))
        self._btn_look = tk.PhotoImage(file=str(assets_dir / 'look.png'))
        self._btn_quests = tk.PhotoImage(file=str(assets_dir / 'quests.png'))

        # Command buttons
        tk.Button(buttons_frame,
                  image=self._btn_help,
                  command=lambda: self._send_command("help"),
                  bd=0).grid(row=0, column=0, pady=2)
        tk.Button(buttons_frame,
                  image=self._btn_sac,
                  command=lambda: self._send_command("inventory"),
                  bd=0).grid(row=0, column=1, pady=2)
        tk.Button(buttons_frame,
                  image=self._btn_look,
                  command=lambda: self._send_command("look"),
                  bd=0).grid(row=0, column=2, pady=2)
        tk.Button(buttons_frame,
                  image=self._btn_quests,
                  command=lambda: self._send_command("quests"),
                  bd=0).grid(row=0, column=3, pady=2)
        
        # Movement buttons (N,E,S,O,U,D)
        move_frame = ttk.LabelFrame(buttons_frame, text="Déplacements")
        move_frame.grid(row=1, column=0, columnspan=4, sticky="ew", pady=4)
        tk.Button(move_frame,
                  image=self._btn_nord,
                  command=lambda: self._send_command("go N"),
                  bd=0).grid(row=0, column=0, columnspan=2)
        tk.Button(move_frame,
                  image=self._btn_ouest,
                  command=lambda: self._send_command("go O"),
                  bd=0).grid(row=1, column=0)
        tk.Button(move_frame,
                  image=self._btn_est,
                  command=lambda: self._send_command("go E"),
                  bd=0).grid(row=1, column=1)
        tk.Button(move_frame,
                  image=self._btn_sud,
                  command=lambda: self._send_command("go S"),
                  bd=0).grid(row=2, column=0, columnspan=2)
        #Up/Down buttons
        tk.Button(move_frame,
                  image=self._btn_up,
                  command=lambda: self._send_command("go U"),
                  bd=0).grid(row=0, column=2, columnspan=2)
        tk.Button(move_frame,
                  image=self._btn_down,
                  command=lambda: self._send_command("go D"),
                  bd=0).grid(row=2, column=2, columnspan=2)
        
        #Back button
        tk.Button(buttons_frame,
                  image=self._btn_ouest,
                  command=lambda: self._send_command("back"),
                  bd=0).grid(row=2, column=0, columnspan=1)

        # Quit button
        tk.Button(buttons_frame,
                  image=self._btn_quit,
                  command=lambda: self._send_command("quit"),
                  bd=0).grid(row=2, column=3, columnspan=4)

        # L2 Terminal output area (Text + Scrollbar)
        output_frame = ttk.Frame(self)
        output_frame.grid(row=1, column=0, sticky="nsew", padx=6, pady=3)
        output_frame.grid_rowconfigure(0, weight=1)
        output_frame.grid_columnconfigure(0, weight=1)

        scrollbar = ttk.Scrollbar(output_frame, orient="vertical")
        self.text_output = tk.Text(output_frame,
                                   wrap="word",
                                   yscrollcommand=scrollbar.set,
                                   state="disabled",
                                   bg="#111", fg="#eee")
        scrollbar.config(command=self.text_output.yview)
        self.text_output.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # L1 Entry area
        entry_frame = ttk.Frame(self)
        entry_frame.grid(row=2, column=0, sticky="ew", padx=6, pady=(3,6))
        entry_frame.grid_columnconfigure(0, weight=1)

        self.entry_var = tk.StringVar()
        self.entry = ttk.Entry(entry_frame, textvariable=self.entry_var)
        self.entry.grid(row=0, column=0, sticky="ew")
        self.entry.bind("<Return>", self._on_enter)
        self.entry.focus_set()


    # -------- Image update --------
    def _update_room_image(self):
        """Update the canvas image based on the current room."""
        if not self.game.player or not self.game.player.current_room:
            return

        room = self.game.player.current_room
        assets_dir = Path(__file__).parent / 'assets'

        # Use room-specific image if available, otherwise fallback
        if room.image:
            image_path = assets_dir / room.image
        else:
            image_path = assets_dir / 'scene.png'

        try:
            # Load new image
            self._image_ref = tk.PhotoImage(file=str(image_path))
            # Clear canvas and redraw image
            self.canvas.delete("all")
            self.canvas.create_image(
                self.IMAGE_WIDTH/2,
                self.IMAGE_HEIGHT/2,
                image=self._image_ref
            )
        except (FileNotFoundError, tk.TclError):
            # Fallback to text if image not found or cannot be loaded
            self.canvas.delete("all")
            self.canvas.create_text(
                self.IMAGE_WIDTH/2,
                self.IMAGE_HEIGHT/2,
                text=f"Image: {room.name}",
                fill="white",
                font=("Helvetica", 18)
            )


    # -------- Event handlers --------
    def _on_enter(self, _event=None):
        """Handle Enter key press in the entry field."""
        value = self.entry_var.get().strip()
        if value:
            self._send_command(value)
        self.entry_var.set("")


    def _send_command(self, command):
        if self.game.finished:
            return
        # Echo the command in output area
        print(f"> {command}\n")
        self.game.process_command(command)
        # Update room image after command (in case player moved)
        self._update_room_image()
        if self.game.finished:
            # Disable further input and schedule close (brief delay to show farewell)
            self.entry.configure(state="disabled")
            self.after(600, self._on_close)


    def _on_close(self):
        # Restore stdout and destroy window
        sys.stdout = self.original_stdout
        self.destroy()


def main():
    """Entry point.

    If '--cli' is passed as an argument, start the classic console version.
    Otherwise launch the Tkinter GUI.
    Fallback to CLI if GUI cannot be initialized (e.g., headless environment).
    """
    args = sys.argv[1:]
    if '--cli' in args:
        Game().play()
        return
    
    # Test if Tkinter is actually usable before trying to create GUI
    try:
        # Tkinter is available, proceed with GUI
        app = GameGUI()
        app.mainloop()
    except tk.TclError as e:
        # Fallback to CLI if GUI fails (e.g., no DISPLAY, Tkinter not available)
        print(f"GUI indisponible ({e}). Passage en mode console.")
        Game().play()


if __name__ == "__main__":
    main()
