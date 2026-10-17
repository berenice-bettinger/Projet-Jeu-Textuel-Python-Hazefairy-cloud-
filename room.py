# Define the Room class.

from item import Item
from character1 import Character
from character2 import Character2


class Room:
    """
    Represents a location in the game world.

    A Room has a name, a description, and a set of exits that connect it to other rooms. Exits are stored in a dictionary mapping directions
    (e.g., "north", "east") to other Room instances.

    Attributes :
    name (str) : The name of the room.
    description (str) : A textual description of the room, used to inform the player of their surroundings.
    exits (dict[str, Room]) : A dictionary mapping directions to the connected rooms. A direction with value None indicates that no room exists in that direction.

    Methods : 
    get_exit(direction): Returns the room connected in the given direction, or None if no exit exists.
    
    get_exit_string(): Returns a formatted string listing the available exits in this room.
    
    get_long_description(): Returns a full description of the room, including its text description and the list of exits.
    """
    # Define the constructor. 
    def __init__(self, name, description, image):
        self.name = name
        self.description = description
        self.image = image  # Path to image file (PNG/JPG) for this room
        self.exits = {}
        self.item = {}

    
    # Define the get_exit method.
    def get_exit(self, direction):

        # Return the room in the given direction if it exists.
        if direction in self.exits.keys():
            return self.exits[direction]
        else:
            return None
    
    # Return a string describing the room's exits.
    def get_exit_string(self):
        exit_string = "Sorties: " 
        for exit in self.exits.keys():
            if self.exits.get(exit) is not None:
                exit_string += exit + ", "
        exit_string = exit_string.strip(", ")
        return exit_string

    # Return a long description of this room including exits.
    def get_long_description(self):
        # La description longue inclut la description courte puis l'inventaire.
        desc = self.get_short_description()
        try:
            desc += "\n" + self.get_inventory()
        except Exception:
            pass
        return desc


    def get_short_description(self):
        """
        Retourne la description courte de la pièce (description + sorties),
        sans afficher la liste des objets présents dans la pièce.
        """
        return f"\nVous êtes dans {self.description}\n\n{self.get_exit_string()}\n"


    
    def get_inventory(self):
        # Sépare les objets et les personnages présents dans la pièce
        if not self.item:
            return "Il n'y a rien ici."

        items = [obj for obj in self.item.values() if isinstance(obj, Item)]
        characters = [obj for obj in self.item.values() if isinstance(obj, (Character, Character2))]

        if not items and not characters:
            return "Il n'y a rien ici."

        lines = ["On voit:"]

        # Affiche d'abord les objets
        for it in items:
            try:
                weight_str = f"{it.weight:g}"
                lines.append(f"        - {it.name} : {it.description} ({weight_str} kg)")
            except Exception:
                lines.append(f"        - {str(it)}")

        # Puis les personnages
        for ch in characters:
            try:
                lines.append(f"        - {ch.name} : {ch.description}")
            except Exception:
                lines.append(f"        - {str(ch)}")

        return "\n".join(lines)
        
    def characters(self):
        """Retourne la liste des personnages présents dans la pièce."""
        return [obj for obj in self.item.values() if isinstance(obj, (Character, Character2))]
