from math import gcd, sqrt
from sympy import isprime, factorint


def is_prime(num):
    return isprime(num)


def factorize_int(num):
    if num == 0 or num == 1:
        return {num: 1}
    res = factorint(num)
    muls = []
    for i in res:
        for el in [i] * int(res[i]):
            muls.append(el)
    first = int(sqrt(num))
    while num % first != 0:
        first -= 1
    second = num // first
    muls = [str(first), str(second)]
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
