"""F(n) = 1 при n = 1;
F(n) = n × F(n − 1), если n > 1.
Чему равно значение выражения F(2023) / F(2020)?
"""

from functools import lru_cache


@lru_cache
def F(n):
    if n == 1:
        return 1
    if n > 1:
        return n * F(n-1)

print(F(2023) / F(2020))