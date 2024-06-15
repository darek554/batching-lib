import sys
import random
import string
import unittest

from unittest.mock import patch

from batching import constants
from batching.batching import split_records_into_batches


STR_OBJECT_SIZE = sys.getsizeof("")
MAX_RECORD_SIZE = 1024 + STR_OBJECT_SIZE


def generate_random_length_string(a: int, b: int) -> str:
    return "".join(random.choice(string.ascii_letters) for _ in range(random.randint(a, b)))


@patch.object(constants, "MAX_OUTPUT_RECORD_SIZE", new=MAX_RECORD_SIZE)
class TestSplitRecordsIntoBatches(unittest.TestCase):
    def test_discards_large_records(self):
        test_strings = ["a",
                        generate_random_length_string(constants.MAX_OUTPUT_RECORD_SIZE + 1,
                                                      constants.MAX_OUTPUT_RECORD_SIZE + 3),
                        "b",
                        generate_random_length_string(constants.MAX_OUTPUT_RECORD_SIZE + 1,
                                                      constants.MAX_OUTPUT_RECORD_SIZE + 3),
                        "c",
                        generate_random_length_string(constants.MAX_OUTPUT_RECORD_SIZE + 1,
                                                      constants.MAX_OUTPUT_RECORD_SIZE + 3),
                        "d"]

        batches = split_records_into_batches(test_strings)

        self.assertEqual(len(batches), 1)
        self.assertListEqual(batches[0], ["a", "b", "c", "d"])

    @patch.object(constants, "MAX_OUTPUT_BATCH_SIZE", new=5*MAX_RECORD_SIZE)
    def test_split_when_batch_size_exceeds(self):
        test_strings = ["c" * 1024] * 6

        batches = split_records_into_batches(test_strings)

        self.assertEqual(len(batches), 2)
        self.assertEqual(len(batches[0]), 5)
        self.assertEqual(len(batches[1]), 1)

    @patch.object(constants, "MAX_OUTPUT_BATCH_RECORDS_COUNT", new=2)
    def test_split_when_batch_records_count_exceeds(self):
        test_strings = ["c"] * 5

        batches = split_records_into_batches(test_strings)

        self.assertEqual(len(batches), 3)
        self.assertListEqual(batches[0], batches[1])
        self.assertListEqual(batches[2], ["c"])

    def test_batching_preserves_records_order(self):
        test_strings = [str(i) for i in range(10000)]

        batches = split_records_into_batches(test_strings)
        concatenated_batches = [
            record for batch in batches for record in batch]

        self.assertListEqual(test_strings, concatenated_batches)
