from time import perf_counter, sleep
from functools import wraps
import random


class Profiler:
    def __init__(self, fn):
        self.counter = 0
        self.total_elapsed = 0
        self.fn = fn

    def __call__(self, *args, **kwargs):
        self.counter += 1
        start = perf_counter()
        result = self.fn(*args, **kwargs)
        end = perf_counter()
        self.total_elapsed += (end - start)
        return result

    @property
    def avg_time(self):
        return self.total_elapsed / self.counter


@Profiler
def func_1(a, b):
    sleep(random.random())
    return (a, b)


func_1 = Profiler(func_1)
print(func_1(1, 2))
print(func_1(2, 3))
print(func_1(3, 4))
print(func_1.counter)
print(func_1.avg_time)
