from aiogram.utils.helper import Helper, HelperMode, ListItem
from aiogram.utils.markdown import text, bold, italic, code
from emoji import emojize

from random import randint


class Warior:
    def __init__(self, name="Warior_1", health=500, damage=50, healmin=0, healmax=25,
                 is_alive=True):
        self.name = name
        self.max_health = health
        self.health = health
        self.damage = damage
        self.healmin = healmin
        self.healmax = healmax
        self.is_alive = is_alive

    def show(self, ty="n", change=0):
        unit_name = bold(f"{self.name}:")
        if ty == "n":
            string1 = f"\nHealth: {self.health}/{self.max_health}"
            string2 = f"\nDamage: {self.damage}"
            message = text(unit_name, italic(string1), italic(string2))
        elif ty == "d":
            string1 = f"Health: {self.health}(-{change})/{self.max_health}"
            string2 = emojize("\n:loudly_crying_face: DAMAGE TAKEN :loudly_crying_face:")
            message = text(unit_name, string1, string2,
                           sep='\n')
        elif ty == "h":
            string1 = f"Health: {self.health}(+{change})/{self.max_health}"
            string2 = emojize("\n:sparkling_heart: SUCCESFULL HEAL :sparkling_heart:")
            message = text(unit_name, string1, string2,
                           sep='\n')
        else:
            message = text(code("Error: Wrong type of show"))
        return message

    def heal(self):
        add = randint(self.healmin, self.healmax)
        if self.health + add < self.max_health:
            self.health += add
        else:
            self.health = self.max_health
        return self.show("h", add)

    def get_damage(self, damage):
        if damage != 0:
            self.health -= damage
            if self.health <= 0:
                self.health = 0
                message = text(bold(f"{self.name} is dead"))
                self.is_alive = False
                return message
            else:
                return self.show("d", damage)
        else:
            return text(code("Error: No enemy or dead"))

    def get_info(self):
        return self.show("n")

    def add_damage(self):
        self.damage += 25
        self.health = self.max_health
        return self.show("n")

    def add_max_health(self):
        self.max_health += 100
        self.health = self.max_health
        return self.show("n")

    def add_heal(self):
        self.healmin += 25
        self.healmax += 25
        self.health = self.max_health
        return self.show("n")

    def reset(self):
        self.max_health = 500
        self.health = self.max_health
        self.damage = 50
        self.healmin = 0
        self.healmax = 25
        self.is_alive = True


class LevelProgress:
    def __init__(self, enemy_index=0, enemy_amount=4, attacked=False, healed=False):
        self.enemy = enemy_index
        self.enemy_amount = enemy_amount
        self.attacked = attacked
        self.healed = healed

    def next_enemy(self):
        self.enemy += 1

    def turn_attack(self):
        self.attacked = not self.attacked

    def turn_heal(self):
        self.healed = not self.healed

    def reset(self):
        self.enemy = 0
        self.attacked = False
        self.healed = False


class States(Helper):
    mode = HelperMode.snake_case

    STATE_0 = ListItem()
    STATE_1 = ListItem()


if __name__ == '__main__':
    print(States.all())
