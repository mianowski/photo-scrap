from __future__ import annotations  # for type hints of typed lists
import concurrent.futures
import itertools
from collections.abc import Iterable


def split_even(l: list, parts: int):
    size = len(l)//parts + 1 if len(l) % parts else len(l)//parts
    return [l[i*size: (i+1)*size] for i in range(parts)]


def parallelize(args: list, threads: int, fun: callable[[Iterable], Iterable]):
    """Can use given threads count to run in parallel a function 
    taking and returning iterable and merge results"""
    assert(threads > 0), "Number of threads must be positive"
    split_args = split_even(args, threads)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(fun, arg)
                   for arg in split_args]
    return list(itertools.chain.from_iterable([f.result() for f in futures]))
