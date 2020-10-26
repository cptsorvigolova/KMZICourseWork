from Modules.math_module import is_coprime, is_prime, fast_pow


def get_exponent_candidates(r):
    primes = [r * i + 1 for i in range(1, 11)]
    primes = sorted(primes, reverse=True)
    if len(primes) > 10:
        primes = primes[0:10]
    return [str(i) for i in primes]


def encrypt(e, n, key):
    return fast_pow(key, e) % n
