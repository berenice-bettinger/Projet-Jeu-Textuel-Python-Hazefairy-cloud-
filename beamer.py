from item import Item

DEBUG = False

class Beamer(Item):
    def __init__(self, name="beamer", description="un beamer magique pour vous téléporter.", weight=2, max_slots=3):
        """Un beamer est un item qui peut mémoriser des pièces (slots) et téléporter le joueur vers elles."""
        super().__init__(name, description, weight)
        self.slots = {}        # dictionnaire {nom_slot: room}
        self.max_slots = max_slots

    def charge(self, player, slot_name):
        """Charge le beamer avec la pièce actuelle du joueur dans un slot nommé."""
        if len(self.slots) >= self.max_slots and slot_name not in self.slots:
            print(f"\n Le beamer est plein (max {self.max_slots} slots).\n")
            return
        self.slots[slot_name] = player.current_room
        print(f"\n🔮 Le beamer est chargé dans le slot '{slot_name}' avec la pièce '{player.current_room.name}'.\n")

    def fire(self, player, slot_name):
        """Téléporte le joueur dans la pièce mémorisée dans le slot choisi."""
        if slot_name not in self.slots:
            print(f"\n Aucun slot '{slot_name}' n'est chargé.\n")
        else:
            # Effectuer la téléportation et enregistrer l'historique comme pour un déplacement normal.
            player.current_room = self.slots[slot_name]
            try:
                player.log_history()
            except Exception:
                pass
            print(f"\n✨ Vous êtes téléporté dans la pièce '{self.slots[slot_name].name}' grâce au beamer (slot '{slot_name}').\n")
            # Afficher la description courte de la pièce d'arrivée (sans inventaire).
            try:
                print(player.current_room.get_short_description())
            except Exception:
                pass

    def list_slots(self):
        """Affiche les slots mémorisés."""
        if not self.slots:
            print("\nLe beamer n'a aucun slot chargé.\n")
        else:
            print("\nSlots mémorisés :")
            for name, room in self.slots.items():
                print(f" - {name} : {room.name}")