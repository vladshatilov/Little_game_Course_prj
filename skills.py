from abc import ABC
from dataclasses import dataclass


@dataclass
class Skill(ABC):
    name: str
    damage: float
    stamina: float

    def skill_effect(self, user):
        user.health += user.armor - self.damage
        pass

    def use_skill(self, user, target):
        if user.stamina > 0:
            self.skill_effect(target)
            return f'{user.name} использует {user.skill} и наносит {self.damage} урона сопернику.'
        return f'{user.name} попытался использовать {user.skill}, но у него не хватило выносливости.'


Stomp = Skill(
    name="Stomp",
    damage=12,
    stamina=6
)

Stealth_hit = Skill(
    name="Stealth hit",
    damage=15,
    stamina=5
)
