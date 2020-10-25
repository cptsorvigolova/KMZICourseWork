from math import gcd
from sympy import isprime, factorint


def is_prime(num):
    return isprime(num)


def factorize_int(num):
    muls = factorint(num)
    return muls


def is_coprime(num1, num2):
    return gcd(num1, num2) == 1


def fast_pow(x, y):
    if y == 0:
        return 1
    if y == -1:
        return 1. / x
    p = fast_pow(x, y // 2)
    p *= p
    if y % 2:
        p *= x
    return p
