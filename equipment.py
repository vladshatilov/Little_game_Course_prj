import json
import random
from dataclasses import dataclass
from typing import List
import marshmallow_dataclass

import marshmallow as marshmallow


@dataclass
class Weapon:
    id: int
    name: str
    min_damage: float
    max_damage: float
    stamina_per_hit: float

    def damage(self) -> float:
        return round(random.uniform(self.min_damage, self.max_damage), 1)


@dataclass
class Armor:
    id: int
    name: str
    defence: float
    stamina_per_turn: float


@dataclass
class EquipmentData:
    weapons: List[Weapon]
    armors: List[Armor]

    class Meta:
        unknown = marshmallow.EXCLUDE


class Equipment:
    def __init__(self):
        self.inventory = self._get_all_inventory()

    def get_weapon(self, name_of_weapon: str) -> Weapon:
        return next(filter(lambda x: x.name == name_of_weapon, self.inventory.weapons))

    def get_armor(self, name_armor: str) -> Armor:
        return next(filter(lambda x: x.name == name_armor, self.inventory.armors))

    def get_weapon_names(self) -> List[str]:
        return [x.name for x in self.inventory.weapons]

    def get_armor_names(self) -> List[str]:
        return [x.name for x in self.inventory.armors]

    @staticmethod
    def _get_all_inventory():
        with open('data/equipment.json', encoding='utf-8') as json_data:
            data = json.load(json_data)
            try:
                return marshmallow_dataclass.class_schema(EquipmentData)().load(data)
            except marshmallow.exceptions.ValidationError:
                return ValueError
