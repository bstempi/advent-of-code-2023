import dataclasses
from typing import List

from aoc_2023 import Solution


@dataclasses.dataclass
class ScratchCard:
    winning_numbers: List[int]
    candidate_numbers: List[int]


class ScratchCardParser:
    @staticmethod
    def parse(f):
        cards = []

        for l in f:
            # Step 1: parse out the card identifier
            card_parts = l.split(':')
            card_id = card_parts[0]
            card_numbers = card_parts[1]

            # Step 2: parse out the numbers
            card_number_parts = card_numbers.split('|')
            winning_numbers = card_number_parts[0].split(' ')
            winning_numbers = [int(x) for x in filter(lambda x: x != '', winning_numbers)]
            candidate_numbers = card_number_parts[1].split(' ')
            candidate_numbers = [int(x) for x in filter(lambda x: x != '', candidate_numbers)]

            cards.append(ScratchCard(winning_numbers=winning_numbers, candidate_numbers=candidate_numbers))

        return cards


class Solution0401(Solution):

    day = 4
    part = 1

    def run(self) -> int:
        total = 0
        with self.get_input_file() as f:
            cards = ScratchCardParser.parse(f)
            for card in cards:
                winning_num_set = set(card.winning_numbers)
                candidate_num_set = set(card.candidate_numbers)

                winning_num_count = len(winning_num_set.intersection(candidate_num_set))
                if winning_num_count == 0:
                    continue
                total += 2 ** (winning_num_count - 1)

        return total


class Solution0402(Solution):

    day = 4
    part = 2

    def run(self) -> int:
        with self.get_input_file() as f:
            cards = ScratchCardParser.parse(f)
            totals = {i + 1: 1 for i in range(len(cards))}
            for i, card in enumerate(cards):
                card_id = i + 1
                winning_num_set = set(card.winning_numbers)
                candidate_num_set = set(card.candidate_numbers)

                current_card_count = totals[card_id]
                winning_num_count = len(winning_num_set.intersection(candidate_num_set))
                if winning_num_count == 0:
                    continue
                for i in range(winning_num_count):
                    totals[card_id + i + 1] += current_card_count

        total = sum(totals.values())
        return total
