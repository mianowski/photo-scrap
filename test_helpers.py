import unittest
from photo_scrap.helpers import split_even, parallelize


class SplitEvenTest(unittest.TestCase):
    def test_correctness_for_indivisible(self):
        self.assertEquals(split_even(
            [0, 1, 2, "three", {4}], 3), [[0, 1], [2, "three"], [{4}]])

    def test_correctness_for_divisible(self):
        self.assertEquals(split_even(
            [0, 1, 2, 3, 4, 5], 3), [[0, 1], [2, 3], [4, 5]])

    def test_too_short_list_is_split_to_correct_number_of_parts(self):
        self.assertEquals(split_even(
            [0, 1], 3), [[0], [1], []])

    def test_empty_list_is_split_to_empty_lists(self):
        self.assertEquals(split_even(
            [], 3), [[], [], []])

    def test_negative_parts_count_result_in_empty_result(self):
        self.assertEquals(split_even(
            [1, 2, 3], -1), [])


class ParallelizeTest(unittest.TestCase):
    def _foo_l(self, _):
        return [1, 2, 3]

    def _foo_d(self, _):
        return {1: 'a', 2: 'b'}

    def _foo_s(self, _):
        return 'abc'

    def test_result_correctness_list(self):
        self.assertEquals(parallelize([], 3, self._foo_l),
                          [1, 2, 3, 1, 2, 3, 1, 2, 3])

    def test_result_correctness_dict(self):
        self.assertEquals(parallelize([], 2, self._foo_d),
                          [1, 2, 1, 2])

    def test_result_correctness_string(self):
        self.assertEquals(parallelize([], 2, self._foo_s),
                          ['a', 'b', 'c', 'a', 'b', 'c'])
