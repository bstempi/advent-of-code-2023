import dataclasses
from typing import List

from aoc_2023 import Solution


@dataclasses.dataclass
class GenericAlmanacMapping:
    left_start: int
    right_start: int
    steps: int

    def does_left_exist(self, left) -> bool:
        if self.left_start <= left <= self.left_start + self.steps - 1:
            return True
        return False

    def does_right_exist(self, right) -> bool:
        if self.right_start <= right <= self.right_start + self.steps - 1:
            return True
        return False


@dataclasses.dataclass
class GenericAlmanacMappingCollection:
    mappings: List[GenericAlmanacMapping]

    def get(self, right_id: int) -> int:
        for m in self.mappings:
            if m.does_right_exist(right_id):
                mapping_offset = right_id - m.right_start
                return m.left_start + mapping_offset

        # If we got this far, we found nothing; assume that there is no mapping because this id maps to itself
        return right_id

    def reverse_get(self, left_id: int) -> int:
        for m in self.mappings:
            if m.does_left_exist(left_id):
                mapping_offset = left_id - m.left_start
                return m.right_start + mapping_offset

        # If we got this far, we found nothing; assume that there is no mapping because this id maps to itself
        return left_id


class SeedMappingParser:
    @staticmethod
    def parse(f):
        sections = []
        unparsed_sections = f.read().split('\n\n')

        seed_section = unparsed_sections.pop(0)
        seed_section = [int(x) for x in seed_section.replace('seeds: ', '').split(' ')]
        for current_unparsed_section in unparsed_sections:
            current_section = []
            for i, l in enumerate(current_unparsed_section.splitlines()):
                if i == 0:
                    continue
                parsed_numbers = [int(x) for x in l.split(' ')]
                entry = GenericAlmanacMapping(parsed_numbers[0], parsed_numbers[1], parsed_numbers[2])
                current_section.append(entry)
            sections.append(GenericAlmanacMappingCollection(current_section))
        return seed_section, sections


class Solution0501(Solution):

    day = 5
    part = 1

    def run(self) -> int:
        with self.get_input_file() as f:
            seed_section, other_sections = SeedMappingParser.parse(f)
        locations = []
        for current_seed in seed_section:
            item_to_find = current_seed
            for current_section in other_sections:
                current_section: GenericAlmanacMappingCollection = current_section
                item_to_find = current_section.get(item_to_find)
            locations.append(item_to_find)
        return min(locations)


class Solution0502(Solution):

    day = 5
    part = 2

    def run(self) -> int:
        with self.get_input_file() as f:
            seed_section, other_sections = SeedMappingParser.parse(f)

        seed_ranges = [range(seed_section[i*2], seed_section[i*2+1]) for i in range(int(len(seed_section) / 2))]
        # This is hard for me to wrap my head around, but I feel like I need to since I'm facing a similar problem
        # elsewhere in my professional life.
        # Brute-forcing using forward lookups is not going to work in a reasonable amount of time. Reverse-brute-forcing
        # is probably more reasonable, but still really, really wasteful.
        # Instead, maybe we can shrink the search space. We could figure out where the seed ids and the next map ids
        # overlaps and throw away the rest of the ranges. We could repeat this process all the way down to the location
        # map. At that point, we're guaranteed that every range in the location map will successfully map back to a
        # seed, so all we'd need to do is scan the location map for its minimum value.
