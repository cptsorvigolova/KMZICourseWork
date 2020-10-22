from math import floor, sqrt
from sympy import isprime


def is_prime_for_short(num):
    divs = list(range(3, floor(sqrt(num)), 2))
    divs.insert(0, 2)
    for div in divs:
        if num % div == 0:
            return False
    return True


def is_prime_for_long(num):
    return isprime(num)
