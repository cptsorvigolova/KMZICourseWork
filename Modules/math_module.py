from math import gcd
from sympy import isprime, factorint


def is_prime(num):
    return isprime(num)


def factorize_int(num):
    muls = factorint(num)
    return muls


def is_coprime(num1, num2):
    return gcd(num1, num2)
