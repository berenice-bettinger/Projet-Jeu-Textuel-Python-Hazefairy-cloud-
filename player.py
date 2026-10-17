from quests import QuestManager
import sys


DEBUG = False

# Define the Player class.
class Player():

    """
    Represents the player in the game.

    This class manages the player's name, their current position in the game
    world (the room they are in), and their movements between rooms.

    Attributes :
        name (str) : The player's name.
        current_room (Room or None) : The room the player is currently in. It is None until the player is placed in a starting room.

    Methods :
        __init__(self, name) : The constructor.
        move(direction) : Moves the player in the given direction if an exit exists. Updates the current room and prints its full description. Returns True if the movement is successful, False otherwise.
    
    Examples:

    >>> player = Player("Alice")
    >>> player.current_room = room1
    >>> success = player.move("north")
    >>> if success:
    >>>     print("The player successfully moved!")
    >>> else:
    >>>     print("Movement failed!")
    The player successfully moved!
    """
    
    # Define the constructor.
    def __init__(self, name, max_weight=3.0):
        self.name = name
        self.current_room = None
         # In-memory history of rooms visited (initially empty)
        self.history = []
        # Inventory of items (initially empty). Structure: dict mapping item.name -> Item
        self.inventory = {}
        self.max_weight = max_weight
        self.quest_manager = QuestManager(self)
        self.move_count = 0
        self.rewards = []
        self.money = 0
        self.talk_count = 0
        self.hp = 100
        self.max_hp = 100

    # Define the log_history method.
    def log_history(self):
        try:
            room = self.current_room
        except Exception:
            room = None
        self.history.append(room)    
    
    def get_history(self):
        """
        Retourne une chaîne représentant l'historique des pièces visitées par le joueur.
        Exemple : '-Chambre 
                   -Couloir 
                   -Cuisine'
        """
        # Filtre les None éventuels et remplace par un token lisible
        if not self.history:
            return "Vous n'avez encore visité aucune pièce."

        lines = ["Vous avez déjà visité les pièces suivantes:"]
        for entry in self.history:
            if entry is None:
                label = 'Inconnu'
            else:
                # entry may be a Room instance or already a string
                try:
                    label = entry.name
                except Exception:
                    label = str(entry)
            lines.append(f"    - {label}")
        return "\n".join(lines)

    def get_inventory(self):
        """Retourne une chaîne représentant l'inventaire du joueur."""
        lines = [f"Vous avez {self.money} écus."]
        
        if not self.inventory: 
            lines.append("Votre inventaire est vide.")
        else:
            lines.append("Vous disposez des items suivants :")
            for item in self.inventory.values():
                try:
                    lines.append(f"    - {item.name} : {item.description} ({item.weight} kg)")
                except Exception:
                    lines.append(f"    - {str(item)}")
        return "\n".join(lines)   


    # Define the move method.
    def move(self, direction):
        # Get the next room from the exits dictionary of the current room.
        next_room = self.current_room.exits[direction]

        # If the next room is None, print an error message and return False.
        if next_room is None:
            try:
                from game import DEBUG
            except Exception:
                DEBUG = False
            if DEBUG:
                try:
                    print(f"DEBUG: move blocked (direction={direction})")
                except Exception:
                    pass
            print("\nCe chemin n'est pas accessible !\n")
            return False
        else:
            # Check if moving from Pont to Mer (costs 60 écus if player has "Accès au bateau" reward)
            if self.current_room.name == "Pont" and next_room.name == "Mer":
                # Check if player has completed "Financer le voyage" quest
                if not self.quest_manager.is_completed("Financer le voyage"):
                    print("\nVous n'avez pas accès au bateau. Vous devez d'abord financer le voyage (60 écus).\n")
                    return False
                
                # Deduct 60 écus for the boat trip
                if self.money >= 60:
                    self.money -= 60
                    print(f"\nVous payez 60 écus pour le voyage en bateau.")
                    print(f"Il vous reste {self.money} écus.\n")
                else:
                    print(f"\nVous n'avez pas assez d'écus pour le voyage ! Il vous en faut 60, vous en avez {self.money}.\n")
                    return False
            
            # Check if moving from Ruines to Montagne (requires "La Clé des Ruines" quest completion)
            if self.current_room.name == "Ruines" and next_room.name == "Montagne":
                # Check if player has completed "La Clé des Ruines" quest
                if not self.quest_manager.is_completed("La Clé des Ruines"):
                    print("\nLa porte des ruines est verrouillée. Vous avez besoin de la Clé des Ruines pour l'ouvrir.\n")
                    print("Complétez la quête 'La Clé des Ruines' en trouvant les trois fragments.\n")
                    return False
            
            # perform move
            self.current_room = next_room
            self.move_count += 1
            
            print(f"DEBUG: moved to {next_room.name}")
            try:
                # Après un déplacement, n'affiche que la description courte (sans la liste d'objets).
                print(self.current_room.get_short_description())
                sys.stdout.flush()
            except Exception:
                pass


            # record movement (in-memory)
            try:
                self.log_history()
            except Exception:
                pass

            # afficher l'historique mis à jour après chaque déplacement
            try:
                print(self.get_history())
            except Exception:
                pass
            
            # Check quest objectives
            try:
                self.quest_manager.check_room_objectives(next_room.name)
                self.quest_manager.check_counter_objectives("Se déplacer", self.move_count)
            except Exception:
                pass
            
            # L'inventaire du joueur n'est plus affiché automatiquement après un déplacement.
            # Il sera affiché uniquement via la commande 'look' ou 'inventory' explicite.
            return True

    def add_reward(self, reward):
        if reward not in self.rewards:
            self.rewards.append(reward)
        print (f"Vous avez reçu une récompense : {reward}!")
    
    def show_rewards(self):
        if not self.rewards:
            return "Vous n'avez reçu aucune récompense pour le moment."
        else:
            lines = ["Récompenses reçues :"]
            for r in self.rewards:
                lines.append(f"    - {r}")
            return "\n".join(lines)
        
    def get_money(self):
        return f"Vous avez {self.money} écus."

    def current_weight(self):
        """Calcule le poids total des objets dans l'inventaire du joueur."""
        total_weight = 0.0
        for item in self.inventory.values():
            try:
                total_weight += item.weight
            except Exception:
                pass
        return total_weight