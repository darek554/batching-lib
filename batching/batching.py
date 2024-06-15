import sys

from . import constants
from .utils import is_object_size_less_than_or_equal


def split_records_into_batches(records: list[str]) -> list[list[str]]:
    records_smaller_than_megabyte = [record for record in records if is_object_size_less_than_or_equal(
        record, constants.MAX_OUTPUT_RECORD_SIZE)]

    batches = []
    new_batch = []

    new_batch_current_size = 0

    for record in records_smaller_than_megabyte:
        if new_batch_current_size + sys.getsizeof(record) > constants.MAX_OUTPUT_BATCH_SIZE or \
            len(new_batch) == constants.MAX_OUTPUT_BATCH_RECORDS_COUNT:

            batches.append(new_batch)
            new_batch = []
            new_batch_current_size = 0
        
        new_batch.append(record)
        new_batch_current_size += sys.getsizeof(record)
    
    if len(new_batch) > 0:
        batches.append(new_batch)

    return batches