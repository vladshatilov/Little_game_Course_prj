from dataclasses import dataclass
import random
from typing import Union, Optional

from unit import Person


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


@dataclass
class Arena(metaclass=Singleton):
    stamina_recover: float = 1
    player = None
    enemy = None
    game_running: bool = False
    battle_result: str = ''

    def start_game(self, player: Optional[Person], enemy: Optional[Person]):
        self.player = player
        self.enemy = enemy
        self.game_running = True

    def endgame(self, person: Optional[Person]) -> str:
        self._instances = {}
        self.game_running = False
        return f'{person.name} dead'

    def next_round(self) -> str:
        check_result = self.check_health()
        enemy_move = ''
        if self.game_running:
            if_enemy_cast_spell = int(round(random.uniform(0, 3.5), 0))
            enemy_move = self.enemy.hit_and_run(self.player) if if_enemy_cast_spell else self.enemy.use_skill(
                self.player)
            check_result = self.check_health()
            self.restore_stamina()
        return enemy_move + check_result

    def hero_skip_move(self) -> str:
        if self.game_running:
            player_move = f'{self.player.name} восстанавливает выносливость. '
            self.battle_result = player_move + self.next_round()
        return self.battle_result

    def restore_stamina(self):
        self.player.stamina = min(self.player.unit_class.max_stamina, self.player.stamina + self.stamina_recover)
        self.enemy.stamina = min(self.enemy.unit_class.max_stamina, self.enemy.stamina + self.stamina_recover)
        self.player.skill_used = self.player.skill_used - 1 if self.player.skill_used else 0
        self.enemy.skill_used = self.enemy.skill_used - 1 if self.enemy.skill_used else 0

    def check_health(self) -> str:
        if self.player.health < 0 or self.enemy.health < 0:
            return self.endgame(self.player if self.player.health < 0 else self.enemy)
        return f''

    def hero_hit(self) -> str:
        if self.game_running:
            player_move = self.player.hit_and_run(self.enemy)
            self.battle_result = player_move + self.next_round()
        return self.battle_result

    def hero_use_skill(self) -> str:
        if self.game_running:
            player_move = self.player.use_skill(self.enemy)
            self.battle_result = player_move + self.next_round()
        return self.battle_result
