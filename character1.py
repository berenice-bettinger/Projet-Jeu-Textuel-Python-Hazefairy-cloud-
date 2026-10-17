import random

DEBUG = True 


class Character():
    def __init__(self, name, description, current_room, msgs):
        self.name = name
        self.description = description
        self.current_room = current_room
        self.msgs = msgs
        # Index pour parcourir les messages cycliquement
        self._msg_index = 0
        # Pool de messages non encore affichés et liste des messages déjà montrés
        try:
            self._msg_pool = list(msgs) if msgs is not None else []
        except Exception:
            self._msg_pool = []
        self._shown_msgs = []

    def __str__(self):
        return f"{self.name} : {self.description}"

    def move(self):
        # Si pas de pièce connue, ne peut pas bouger
        if self.current_room is None:
            return False
        if DEBUG:
            print(f"[DEBUG] {self.name} tente de se déplacer depuis {self.current_room.name}")

        # Rassemble les pièces adjacentes valides
        adjacent = [r for r in self.current_room.exits.values() if r is not None]
        if not adjacent:
            return False

        # 50% de chance de ne pas bouger
        if random.choice([True, False]) is False:
            return False

        # Choisit une pièce au hasard et effectue le déplacement
        new_room = random.choice(adjacent)

        # Retirer de la pièce actuelle si présent
        try:
            if self.name in self.current_room.item:
                del self.current_room.item[self.name]
        except Exception:
            pass

        # Mettre à jour la pièce courante
        self.current_room = new_room

        # Ajouter dans la nouvelle pièce
        try:
            new_room.item[self.name] = self
        except Exception:
            pass

        return True
    
    def get_msg(self):
        # Aucun message disponible
        if not self.msgs:
            return ""

        # S'assurer que la pool est initialisée
        if not hasattr(self, '_msg_pool') or self._msg_pool is None:
            try:
                self._msg_pool = list(self.msgs)
            except Exception:
                self._msg_pool = []
        # Reconstituer la pool si on a tout épuisé
        if not self._msg_pool:
            # remonter depuis les messages déjà montrés
            try:
                self._msg_pool = list(self._shown_msgs)
            except Exception:
                self._msg_pool = list(self.msgs)
            self._shown_msgs = []

        try:
            # Popper le premier élément (afin de ne plus l'afficher ensuite)
            msg = self._msg_pool.pop(0)
        except Exception:
            return ""

        # Conserver la trace des messages déjà affichés
        try:
            self._shown_msgs.append(msg)
        except Exception:
            pass

        # Afficher pour le joueur et retourner
        try:
            print(f"{self.name} : {msg}")
        except Exception:
            pass
        return msg