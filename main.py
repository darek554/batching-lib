import sys

from batching.batching import split_records_into_batches
from batching.utils import generate_random_length_string


if __name__ == "__main__":
    test_strings = [
        generate_random_length_string(1, 2048) for _ in range(1000)
    ]

    batches = split_records_into_batches(test_strings)

    length = [len(b) for b in batches]
    size = [sum(map(lambda r: sys.getsizeof(r), b)) for b in batches]

    print(batches)
