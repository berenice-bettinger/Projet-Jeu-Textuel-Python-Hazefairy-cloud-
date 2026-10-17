#Character2 qui ne bouge pas et reste dans la pièce dans laquelle ils sont affectés
from character1 import Character

class Character2(Character):
    def move(self):
        # Un PNJ statique qui ne bouge pas
        return False