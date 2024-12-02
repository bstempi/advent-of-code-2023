import dataclasses
import re

from re import Match

from aoc_2023 import Solution


@dataclasses.dataclass(eq=True, order=True, unsafe_hash=False, frozen=True)
class Coordinate:
    x: int
    y: int


@dataclasses.dataclass(eq=True, order=True, unsafe_hash=False, frozen=True)
class PossiblePartNumber:
    coordinate: Coordinate
    value: int


@dataclasses.dataclass(eq=True, order=True, unsafe_hash=False, frozen=True)
class Symbol:
    coordinate: Coordinate
    type: str


class SchematicParser:
    number_pattern = re.compile('(\d+)')
    symbol_pattern = re.compile('([^\d?|\.])')

    @staticmethod
    def parse(f):
        possible_part_numbers = []
        symbols = []

        for y, l in enumerate(f):
            l = l.strip()
            for number_match in SchematicParser.number_pattern.finditer(l):
                number_match: Match = number_match
                ppn = PossiblePartNumber(Coordinate(x=number_match.span()[0], y=y), int(number_match[0]))
                possible_part_numbers.append(ppn)

            for symbol_match in SchematicParser.symbol_pattern.finditer(l):
                symbol_match: Match = symbol_match
                symbol = Symbol(Coordinate(x=symbol_match.span()[0], y=y), symbol_match[0])
                symbols.append(symbol)

        return possible_part_numbers, symbols


class Solution0301(Solution):

    day = 3
    part = 1

    def run(self) -> int:
        total = 0
        with self.get_input_file() as f:
            # Parse our schematic
            possible_part_numbers, symbols = SchematicParser.parse(f)

            # Create a set of symbol coordinates
            symbol_coordinate_set = {s.coordinate for s in symbols}

            # Iterate through each possible part number
            for cppn in possible_part_numbers:
                # Produce a set of coordinates that surround current possible part number
                adjacent_spaces = set()
                num_len = len(str(cppn.value))
                # Lines above and below number
                for i in range(cppn.coordinate.x - 1, cppn.coordinate.x + num_len + 1):
                    adjacent_spaces.add(Coordinate(x=i, y=cppn.coordinate.y - 1))
                    adjacent_spaces.add(Coordinate(x=i, y=cppn.coordinate.y + 1))

                # Either end of the number
                adjacent_spaces.add(Coordinate(x=cppn.coordinate.x - 1, y=cppn.coordinate.y))
                adjacent_spaces.add(Coordinate(x=cppn.coordinate.x + num_len, y=cppn.coordinate.y))

                # Check to see if there is any overlap with the symbol locations
                if not adjacent_spaces.isdisjoint(symbol_coordinate_set):
                    # We have overlap
                    total += cppn.value

        return total


class Solution0302(Solution):

    day = 3
    part = 2

    def run(self) -> int:
        gear_part_map = {}
        with self.get_input_file() as f:
            # Parse our schematic
            possible_part_numbers, symbols = SchematicParser.parse(f)

            gear_symbols = [x for x in filter(lambda x: x.type == '*', symbols)]
            gear_symbol_coordinate_set = {x.coordinate for x in gear_symbols}
            gear_coordinate_dict = {s.coordinate: s for s in gear_symbols}

            # Iterate through each possible part number
            for cppn in possible_part_numbers:
                # Produce a set of coordinates that surround current possible part number
                adjacent_spaces = set()
                num_len = len(str(cppn.value))
                # Lines above and below number
                for i in range(cppn.coordinate.x - 1, cppn.coordinate.x + num_len + 1):
                    adjacent_spaces.add(Coordinate(x=i, y=cppn.coordinate.y - 1))
                    adjacent_spaces.add(Coordinate(x=i, y=cppn.coordinate.y + 1))

                # Either end of the number
                adjacent_spaces.add(Coordinate(x=cppn.coordinate.x - 1, y=cppn.coordinate.y))
                adjacent_spaces.add(Coordinate(x=cppn.coordinate.x + num_len, y=cppn.coordinate.y))

                # Check to see if there is any overlap with the symbol locations
                overlap = adjacent_spaces.intersection(gear_symbol_coordinate_set)
                if len(overlap) > 0:
                    # which gear does this belong to?
                    gear_symbol = gear_coordinate_dict[overlap.pop()]

                    # Update the map of discovered gears
                    if gear_symbol in gear_part_map:
                        gear_part_map[gear_symbol].append(cppn.value)
                    else:
                        gear_part_map[gear_symbol] = [cppn.value, ]

            # Let's go through and calculate our products and totals
            total = 0
            for gear_values in gear_part_map.values():
                if len(gear_values) != 2:
                    continue
                total = total + (gear_values[0] * gear_values[1])

            return total
