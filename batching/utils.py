import sys
import random

from multiprocessing import Pool, cpu_count


def generate_random_string() -> str:
    return "".join("c" for _ in range(random.randint(1, 10)))


def is_object_size_less_than_or_equal(obj, size: int) -> bool:
    return sys.getsizeof(obj) <= size


def filter_parallel(arr: list, func, cores: int = cpu_count()):
    with Pool(cores) as p:
        filter_bool_result = p.map(func, arr)
        return [e for e, b in zip(arr, filter_bool_result) if b]
