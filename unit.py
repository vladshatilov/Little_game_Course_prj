from abc import ABC
from dataclasses import dataclass

from classes import UnitClass
from equipment import Equipment, Weapon, Armor


@dataclass
class BaseUnit(ABC):
    name: str
    unit_class: UnitClass
    health: float
    stamina: float
    weapon: Weapon = Equipment().get_weapon('ножик')
    armor: Armor = Equipment().get_armor('футболка')
    skill_used: int = 0

    def _calc_damage(self, target) -> float:
        damage = self.weapon.damage() * self.unit_class.attack
        self.stamina = round(self.stamina - self.weapon.stamina_per_hit, 1)
        return self.deal_damage_to(target, damage)

    def _calc_special_damage(self, target) -> float:
        damage = self.unit_class.skill.damage
        print('mag_uron', damage)
        self.stamina = round(self.stamina - self.unit_class.skill.stamina, 1)
        return self.deal_damage_to(target, damage)

    @staticmethod
    def deal_damage_to(target, damage: float) -> float:
        armor_target = target.armor.defence * target.unit_class.armor
        target.health = round((target.health - max(0, (damage - armor_target))), 1)
        return round(damage - armor_target, 1)

    def use_skill(self, target) -> str:
        if not self.skill_used and self.stamina > self.unit_class.skill.stamina:
            print('self.stamina', self.stamina)
            print('self.unit_class.skill.stamina', self.unit_class.skill.stamina)
            self.skill_used = 2
            damage = self._calc_special_damage(target)
            if damage > 0:
                return f'{self.name} использует {self.unit_class.skill.name} наносит {damage} урона противнику. '
            else:
                return f'{self.name} используя {self.unit_class.skill.name} не пробивает броню противника. '
        else:
            return f'{self.name} попытался использовать {self.unit_class.skill.name}, но умение не перезарядилось.' if self.skill_used else \
                f'{self.name} попытался использовать {self.unit_class.skill.name}, но у него не хватило выносливости.'

    def hit_and_run(self, target):
        if self.stamina >= self.weapon.stamina_per_hit:
            damage = self._calc_damage(target)
            if damage > 0:
                return f'{self.name} используя {self.weapon.name} наносит {damage} урона противнику. '
            else:
                return f'{self.name} используя {self.weapon.name} не пробивает броню противника. '
        return f'{self.name} не хватает выносливости для нанесения удара. '


class Person(BaseUnit):
    pass
