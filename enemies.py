import game_classes as gc
from emoji import emojize

enemy_name = [
    emojize(":ghost: Ghost"),
    emojize(":ogre: Ogre"),
    emojize(":zombie: Zombie"),
    emojize(":dragon_face: Dragon")
]

enemy = [
    gc.Warior(enemy_name[0], 250, 110),
    gc.Warior(enemy_name[1], 200, 160),
    gc.Warior(enemy_name[2], 150, 200),
    gc.Warior(enemy_name[3], 700, 100)
]
