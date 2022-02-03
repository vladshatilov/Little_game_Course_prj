from dataclasses import dataclass
from typing import Union

from skills import Stomp, Stealth_hit, Skill


@dataclass
class ConcreteSkill:
    skill: Union[str, None] = None


@dataclass
class UnitClass:
    name: str
    max_health: float
    max_stamina: float
    attack: float
    stamina: float = 0
    armor: float = 0
    skill: Union[Skill, None] = None


Warrior = UnitClass(
    name='Warrior',
    max_health=60.0,
    max_stamina=30.0,
    attack=1.8,
    stamina=0.9,
    armor=1.2,
    skill=Stomp
)

Thief = UnitClass(
    name='Thief',
    max_health=50.0,
    max_stamina=25.0,
    attack=1.5,
    stamina=1.2,
    armor=1.0,
    skill=Stealth_hit
)

unit_classes = {Warrior.name: Warrior, Thief.name: Thief}
