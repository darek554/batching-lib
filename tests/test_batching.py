import sys
import random
import unittest

from unittest.mock import patch

from batching import constants
from batching.batching import split_records_into_batches


def generate_random_length_string(a: int, b: int) -> str:
    return "".join("c" for _ in range(random.randint(a, b)))


@patch.object(constants, 'MAX_OUTPUT_RECORD_SIZE', new=1024)
class TestSplitRecordsIntoBatches(unittest.TestCase):
    def test_split_into_batches(self):
        test_strings = [generate_random_length_string(1, 2048) for _ in range(10000)]

        batches = split_records_into_batches(test_strings)

        self.assertTrue(
            all(
                [
                    sys.getsizeof(record) <= constants.MAX_OUTPUT_RECORD_SIZE
                    for batch in batches
                    for record in batch
                ]
            )
        )
        self.assertTrue(
            all(
                [
                    len(batch) <= constants.MAX_OUTPUT_BATCH_RECORDS_COUNT
                    for batch in batches
                ]
            )
        )
        self.assertTrue(
            all(
                [
                    sum(map(lambda record: sys.getsizeof(record), batch)) <= constants.MAX_OUTPUT_BATCH_SIZE
                    for batch in batches
                ]
            )
        )

    def test_all_records_discarded_size_exceeds(self):
        test_strings = [generate_random_length_string(
            constants.MAX_OUTPUT_RECORD_SIZE + 1, constants.MAX_OUTPUT_RECORD_SIZE + 3) for _ in range(10000)]
        
        batches = split_records_into_batches(test_strings)

        self.assertEqual(len(batches), 0)
    
    @patch.object(constants, 'MAX_OUTPUT_BATCH_SIZE', new=5*1024)
    def test_split_into_two_batches_size_exceeds(self):
        test_strings = ["c" * 900] * 6

        batches = split_records_into_batches(test_strings)

        self.assertEqual(len(batches), 2)
    
    @patch.object(constants, 'MAX_OUTPUT_BATCH_RECORDS_COUNT', new=2)
    def test_batch_records_count_exceeds(self):
        test_strings = ["c"] * 5
        
        batches = split_records_into_batches(test_strings)

        self.assertEqual(len(batches), 3)