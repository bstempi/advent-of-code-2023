from aoc_2023 import Solution


class Solution0101(Solution):

    day = 1
    part = 1

    def run(self) -> int:
        total: int = 0
        with self.get_input_file() as f:
            # For each line in the file
            for l in f:
                first_digit = self.find_first_digit(l)
                last_digit = self.find_last_digit(l)
                calibration_value: int = (10 * first_digit) + last_digit
                total += calibration_value
        return total

    @staticmethod
    def find_first_digit(l):
        for c in l:
            if c.isdigit():
                return int(c)

    @staticmethod
    def find_last_digit(l):
        for c in reversed(l):
            if c.isdigit():
                return int(c)


class Solution0102(Solution):

    day = 1
    part = 2

    word_number_map = {
        'one': 1,
        'two': 2,
        'three': 3,
        'four': 4,
        'five': 5,
        'six': 6,
        'seven': 7,
        'eight': 8,
        'nine': 9,
    }

    def run(self) -> int:
        total: int = 0
        with self.get_input_file() as f:
            # For each line in the file
            for l in f:
                first_digit = self.find_first_number(l)
                last_digit = self.find_last_number(l)
                calibration_value: int = (10 * first_digit) + last_digit
                total += calibration_value
        return total

    @staticmethod
    def find_first_digit(l):
        for i, c in enumerate(l):
            if c.isdigit():
                return i, int(c)

    @staticmethod
    def find_last_digit(l):
        i, d = Solution0102.find_first_digit(reversed(l))
        return len(l) - i - 1, d

    @staticmethod
    def find_first_word(l):
        current_index = None
        current_val = None
        for word, num in Solution0102.word_number_map.items():
            i = l.find(word)
            # If we found it and it's eligible
            if i != -1 and (current_index is None or i < current_index):
                current_index = i
                current_val = num

        return current_index, current_val

    @staticmethod
    def find_last_word(l):
        current_index = None
        current_val = None
        for word, num in Solution0102.word_number_map.items():
            i = l.rfind(word)
            # If we found it and it's eligible
            if i != -1 and (current_index is None or i > current_index):
                current_index = i
                current_val = num

        return current_index, current_val

    @staticmethod
    def find_first_number(l):
        i1, d1 = Solution0102.find_first_word(l)
        i2, d2 = Solution0102.find_first_digit(l)

        min_i = min(filter(lambda x: x is not None, [i1, i2]))

        if i1 == min_i:
            return d1
        else:
            return d2

    @staticmethod
    def find_last_number(l):
        i1, d1 = Solution0102.find_last_word(l)
        i2, d2 = Solution0102.find_last_digit(l)

        max_i = max(filter(lambda x: x is not None, [i1, i2]))

        if i1 == max_i:
            return d1
        else:
            return d2
