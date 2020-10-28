from Modules.math_module import is_coprime, is_prime, fast_pow


def get_exponent_candidates(r):
    primes = [i for i in range(1, min(r, 5000000)) if is_coprime(r, i) and not is_prime(i)]
    primes = sorted(primes, reverse=True)
    if len(primes) > 10:
        primes = primes[0:10]
    return [str(i) for i in primes]


def encrypt(e, n, key):
    print(fast_pow(key, e))
    return fast_pow(key, e) % n
