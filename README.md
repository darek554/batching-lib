# Batching Library

Batching library is a python package that allows splitting data
into batches with predefined characteristics.


## Installation

This library requires Python >= 3.12.


## Example


```python
from batching import batching

test_records = ["record1", "record2", "record3"]
batches = batching.split_records_into_batches(test_records)

for i, batch in enumerate(batches):
    print(f"{i + 1}: {batch}")