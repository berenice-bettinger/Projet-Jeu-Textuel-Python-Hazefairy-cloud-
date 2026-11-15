import random

DEBUG = False


class Character():
    def __init__(self, name, description, current_room, msgs, zone=None, follow=False):
        self.name = name
        # zone : noms des pièces où le PNJ a le droit d'aller (None = partout)
        self.zone = list(zone) if zone else None
        # follow : le PNJ suit le joueur de pièce en pièce (ex. Sully)
        self.follow = follow
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

    def move(self, player_room=None):
        # Si pas de pièce connue, ne peut pas bouger
        if self.current_room is None:
            return False

        # Un compagnon rejoint directement la pièce du joueur
        if self.follow:
            if player_room is None or player_room is self.current_room:
                return False
            return self._go_to(player_room)
        if DEBUG:
            print(f"[DEBUG] {self.name} tente de se déplacer depuis {self.current_room.name}")

        # Rassemble les pièces adjacentes valides (en restant dans sa zone)
        adjacent = [r for r in self.current_room.exits.values()
                    if r is not None and (self.zone is None or r.name in self.zone)]
        if not adjacent:
            return False

        # 50% de chance de ne pas bouger
        if random.choice([True, False]) is False:
            return False

        # Choisit une pièce au hasard et effectue le déplacement
        return self._go_to(random.choice(adjacent))

    def _go_to(self, new_room):
        """Déplace le PNJ dans new_room (en le retirant de sa pièce actuelle)."""

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