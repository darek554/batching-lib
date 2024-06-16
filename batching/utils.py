import sys
import random
import string

from multiprocessing import Pool, cpu_count


def generate_random_length_string(a: int, b: int) -> str:
    return "".join(random.choice(string.ascii_letters) for _ in range(random.randint(a, b)))


def is_object_size_less_than_or_equal(obj, size: int) -> bool:
    return sys.getsizeof(obj) <= size


def filter_parallel(arr: list, func, cores: int = cpu_count()):
    with Pool(cores) as p:
        filter_bool_result = p.map(func, arr)
        return [e for e, b in zip(arr, filter_bool_result) if b]
