"""Fin de l'aventure : la fée Willow, le prince dragon Cylian et le duel contre Zeph.

Toutes les scènes passent par ce module pour garder actions.py lisible :
- talk Willow : la fée explique comment vaincre Zeph et donne la baguette magique ;
- talk Cylian : le dragon révèle qu'il est le prince et accepte de voler jusqu'au château de Zeph ;
- talk Zeph   : duel en trois sortilèges, chacun contré en résolvant un casse-tête.

Les questions du duel s'affichent dans une boîte de dialogue en mode graphique
et dans le terminal en mode console.
"""

import random
import time
import unicodedata

from character1 import Character
from item import Item

try:
    from tkinter import simpledialog
except ImportError:  # mode console sans Tkinter
    simpledialog = None


WAND_NAME = "baguette_magique"
MAX_HP = 3
CRYSTAL_ORDER = ["bleu", "violet", "blanc"]

SEQUENCES = [
    ("2, 4, 8, 16, ?", "32"),
    ("1, 1, 2, 3, 5, 8, ?", "13"),
    ("3, 6, 9, 12, ?", "15"),
    ("1, 4, 9, 16, ?", "25"),
]

RIDDLES = [
    ("J'ai des touches mais je n'ouvre aucune porte. Qui suis-je ?", ["piano", "clavier"]),
    ("Plus je sèche, plus je suis mouillée. Qui suis-je ?", ["serviette"]),
    ("Je monte et je descends sans jamais bouger. Qui suis-je ?", ["escalier", "escaliers"]),
    ("J'ai un lit mais je ne dors jamais. Qui suis-je ?", ["riviere", "fleuve"]),
]


# ---------------------------------------------------------------- utilitaires

def normalize(text):
    """Met une réponse en minuscules, sans accents ni article ni ponctuation."""
    text = unicodedata.normalize("NFD", (text or "").lower())
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    for char in ",;.!?'-":
        text = text.replace(char, " ")
    words = [w for w in text.split() if w not in ("le", "la", "les", "un", "une", "l", "des", "du")]
    return " ".join(words)


def ask(game, question, title="Combat contre Zeph"):
    """Pose une question au joueur (boîte de dialogue en GUI, input() en console).

    Retourne None si le joueur annule ou quitte.
    """
    if game.gui is not None and simpledialog is not None:
        game.gui.update()
        return simpledialog.askstring(title, question, parent=game.gui)
    try:
        return input(f"{question}\n> ")
    except EOFError:
        return None


def find_room(game, name):
    for room in game.rooms:
        if room.name == name:
            return room
    return None


def move_npc(npc, room):
    """Déplace un PNJ dans une pièce (en le retirant de son ancienne pièce)."""
    if npc.current_room is not None and npc.current_room.item.get(npc.name) is npc:
        del npc.current_room.item[npc.name]
    npc.current_room = room
    room.item[npc.name] = npc


def refresh_gui(game):
    if game.gui is not None:
        game.gui._update_room_image()
        game.gui.update()


# ------------------------------------------------------------ la fée Willow

def talk_fairy(game, fairy):
    player = game.player
    if WAND_NAME in player.inventory:
        print("\nWillow : Souviens-toi : trois sortilèges, trois réponses.")
        print("Willow : Pour le bouclier, touche les cristaux dans l'ordre : bleu, violet, puis blanc.")
        print("Willow : Le dragon t'attend. Parle-lui (talk Cylian).\n")
        return True

    print("\nWillow, la fée du lac, s'approche dans un nuage de lumière.")
    print("Willow : Princesse, je t'attendais. Écoute-moi bien.")
    print("Willow : Ce dragon n'en est pas vraiment un... C'est le prince Cylian !")
    print("Willow : Zeph l'a transformé pour que personne ne puisse l'arrêter.")
    print("Willow : Prends cette baguette magique. Elle seule peut contrer les sortilèges de Zeph.")
    print("Willow : Pendant le duel, il te lancera trois sortilèges. Pour chacun, résous son casse-tête :")
    print("   1. Pour lever ton bouclier, touche les cristaux dans l'ordre : bleu, violet, puis blanc.")
    print("   2. Pour briser sa chaîne de chiffres, trouve le nombre qui manque.")
    print("   3. Pour dissiper son brouillard, réponds à sa devinette.")
    print("Willow : Chaque erreur te coûte un cœur. Tu en as trois. Courage !\n")

    player.inventory[WAND_NAME] = Item(
        WAND_NAME, "une baguette de cristal offerte par la fée Willow, seule arme contre Zeph.", 0.5)
    print("✨ Vous recevez la baguette magique !\n")
    player.quest_manager.complete_objective("Obtenir la baguette magique", "Vaincre le Sorcier")
    print("Parlez au dragon pour qu'il vous emmène (talk Cylian).\n")
    return True


# ------------------------------------------------------- le prince dragon

def talk_dragon(game, dragon):
    player = game.player
    if getattr(player, "dragon_ally", False):
        print("\nCylian : Accroche-toi bien, princesse ! Direction le château de Zeph.\n")
        return True

    if WAND_NAME not in player.inventory:
        print("\nLe dragon gronde doucement et tourne la tête vers la fée...")
        print("Il semble vouloir que vous parliez d'abord à Willow (talk Willow).\n")
        return True

    print("\nLe dragon baisse la tête. Dans ses yeux, vous reconnaissez un regard familier...")
    print("Cylian : Princesse... c'est bien moi, Cylian. Zeph m'a jeté un sort et m'a enfermé dans ce corps.")
    print("Cylian : Avec la baguette de la fée, tu peux le vaincre. Monte sur mon dos !")
    print("Cylian : Je t'emmène au-dessus des nuages, jusqu'au château de Zeph.\n")
    player.dragon_ally = True
    dragon.follow = True
    dragon.description = "le prince Cylian, transformé en dragon par Zeph."
    player.quest_manager.complete_objective("Retrouver le prince Cylian", "Vaincre le Sorcier")
    print("Le prince dragon vous suit désormais. Montez sur son dos avec go U.\n")
    return True


# ------------------------------------------------------------- le duel

def _check_crystals(answer):
    colors = [w for w in normalize(answer).split() if w in CRYSTAL_ORDER]
    return colors == CRYSTAL_ORDER


def _rounds():
    sequence, sequence_answer = random.choice(SEQUENCES)
    riddle, riddle_answers = random.choice(RIDDLES)
    return [
        {
            "spell": "Zeph lève les bras : une pluie d'éclairs s'abat sur vous !",
            "question": "Pour lever ton bouclier, touche les trois cristaux de ta baguette dans le bon ordre "
                        "(ex. : rouge vert jaune).",
            "check": _check_crystals,
            "hint": "Indice : la fée t'a donné l'ordre des cristaux. Parle-lui si tu l'as oublié.",
            "success": "Les cristaux s'illuminent et un bouclier de lumière arrête les éclairs !",
        },
        {
            "spell": "Zeph fait jaillir une chaîne de chiffres enflammés qui s'enroule autour de vous !",
            "question": f"Quel nombre complète la suite ?  {sequence}",
            "check": lambda a, s=sequence_answer: normalize(a) == s,
            "hint": "Indice : regarde comment on passe d'un nombre au suivant.",
            "success": "Vous criez le bon nombre : la chaîne se brise en mille étincelles !",
        },
        {
            "spell": "Zeph souffle un brouillard noir qui murmure une devinette...",
            "question": riddle,
            "check": lambda a, r=riddle_answers: normalize(a) in r,
            "hint": "Indice : un seul mot suffit.",
            "success": "Vous donnez la réponse : le brouillard se dissipe et Zeph recule, affaibli !",
        },
    ]


def _retreat(game, message):
    """Renvoie la princesse dans le couloir du sorcier."""
    print(message)
    corridor = find_room(game, "Couloir du sorcier")
    if corridor is not None:
        game.player.current_room = corridor
        print(corridor.get_short_description())
    print("Reprenez votre souffle, puis retentez le duel avec talk Zeph.\n")


def talk_zeph(game, zeph):
    player = game.player
    quests = player.quest_manager

    if WAND_NAME not in player.inventory:
        print("\nZeph éclate de rire : « Sans arme magique ? Tu n'as aucune chance ! »")
        _retreat(game, "Une rafale de vent vous projette hors de la salle de rituel.\n")
        return True

    if not quests.is_active("Le Secret du Sorcier") and not quests.is_completed("Le Secret du Sorcier"):
        quests.activate_quest("Le Secret du Sorcier")
    print("\nZeph : Ainsi, la petite princesse a retrouvé son dragon...")
    print("Zeph : Oui, c'est moi qui ai changé ton prince en bête ! Et c'est moi qui régnerai sur ce royaume !")
    quests.complete_objective("Découvrir le secret de Zeph", "Le Secret du Sorcier")
    quests.complete_objective("Atteindre le repaire du sorcier", "Vaincre le Sorcier")

    print("\n⚔️  LE DUEL COMMENCE ! Vous brandissez la baguette magique.")
    hp = MAX_HP
    for number, rnd in enumerate(_rounds(), start=1):
        print(f"\n--- Sortilège {number}/3 ---   Cœurs : {'❤️ ' * hp}")
        print(rnd["spell"])
        while True:
            answer = ask(game, rnd["question"])
            if answer is None or normalize(answer) in ("fuir", "quit", "quitter", "abandonner"):
                _retreat(game, "\nVous battez en retraite hors de la salle de rituel.\n")
                return True
            if rnd["check"](answer):
                print(f"\n✨ {rnd['success']}")
                break
            hp -= 1
            print(f"\n💥 Raté ! Le sortilège vous frappe. Cœurs restants : {'❤️ ' * hp if hp else '0'}")
            if hp == 0:
                _retreat(game, "\nZeph ricane pendant que vous vous effondrez... "
                               "Il vous rejette hors de la salle de rituel.\n")
                return True
            print(rnd["hint"])

    _victory(game, zeph)
    return True


def _victory(game, zeph):
    player = game.player
    print("\n🌟 Vous pointez la baguette vers Zeph. Les trois cristaux brillent ensemble")
    print("et un rayon de lumière frappe le sorcier, qui disparaît dans un cri !")
    if zeph.current_room is not None:
        zeph.current_room.item.pop(zeph.name, None)
    player.quest_manager.complete_objective("Vaincre le sorcier", "Vaincre le Sorcier")

    print("\nLe sortilège se brise. Le dragon se met à briller... et à sa place se tient le prince Cylian !")
    print("Cylian : Tu m'as délivré, princesse. Rentrons au château.\n")

    castle = find_room(game, "Chateau")
    if castle is not None:
        player.current_room = castle
        for room in game.rooms:
            for npc in list(room.item.values()):
                if isinstance(npc, Character) and npc.follow:
                    move_npc(npc, castle)
                    npc.follow = False
        cylian = castle.item.get("Cylian")
        if cylian is not None:
            cylian.description = "le prince Cylian, enfin libéré du sortilège."
    refresh_gui(game)

    print("De retour au château, tout le royaume est réuni dans la cour.")
    print("Le prince Cylian s'agenouille devant vous :")
    print(f"Cylian : {player.name}, tu as vaincu Zeph et tu m'as délivré du mal. Veux-tu m'épouser ?")
    print("\n💍 Vous dites oui ! Les cloches sonnent, Sully aboie de joie et le royaume fête le mariage.")
    print("\n===== VICTOIRE ! Le royaume est sauvé et la malédiction est levée. =====\n")

    if game.gui is not None:
        game.gui.update()
        time.sleep(5)
    game.finished = True
