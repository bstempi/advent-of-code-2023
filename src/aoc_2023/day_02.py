import dataclasses
from functools import reduce
from typing import List

from aoc_2023 import Solution


@dataclasses.dataclass
class GameRound:
    blue: int
    red: int
    green: int


@dataclasses.dataclass
class Game:
    id: int
    rounds: List[GameRound]


class GameIterator:

    def __init__(self, file):
        self._file = file

    def __iter__(self):
        return self.__next__()

    def __next__(self) -> Game:
        for l in self._file:
            colon_parts = l.split(':')
            game_id_part = colon_parts[0]
            game_results_part = colon_parts[1]

            game_id_parts = game_id_part.split(' ')
            game_id = int(game_id_parts[1])

            game = Game(id=game_id, rounds=[])

            game_results_parts = game_results_part.split(';')
            for current_grp in game_results_parts:
                color_result_parts = current_grp.strip().split(',')
                round_dict = {
                    'red': 0,
                    'blue': 0,
                    'green': 0,
                }
                for current_crp in color_result_parts:
                    result_parts = current_crp.strip().split(' ')
                    count = int(result_parts[0])
                    color = result_parts[1]
                    round_dict[color] = count

                game_round = GameRound(**round_dict)
                game.rounds.append(game_round)

            yield game


class Solution0201(Solution):

    day = 2
    part = 1

    limits = {
        'red': 12,
        'green': 13,
        'blue': 14,
    }

    def run(self) -> int:
        total = 0
        with self.get_input_file() as f:
            game_iterator = GameIterator(f)
            for current_game in game_iterator:
                is_possible = True

                for current_round in current_game.rounds:
                    if Solution0201.limits['red'] < current_round.red \
                            or Solution0201.limits['blue'] < current_round.blue \
                            or Solution0201.limits['green'] < current_round.green:
                        is_possible = is_possible and False

                if is_possible:
                    total += current_game.id

        return total


class Solution0202(Solution):

    day = 2
    part = 2

    def run(self) -> int:
        total = 0

        with self.get_input_file() as f:
            game_iterator = GameIterator(f)
            for current_game in game_iterator:
                current_mins = {
                    'red': 0,
                    'blue': 0,
                    'green': 0,
                }
                for current_round in current_game.rounds:
                    for color in current_mins.keys():
                        current_mins[color] = max(current_mins[color], getattr(current_round, color))

                power_of_cubes = reduce(lambda a, b: a * b, current_mins.values(), 1)
                total += power_of_cubes

        return total
