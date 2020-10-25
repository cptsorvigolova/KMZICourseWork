from Modules.math_module import is_coprime, is_prime, fast_pow


def get_open_exp_candidates(r):
    primes = [i for i in range(min(r, 200000), -1, -1) if is_coprime(r, i) and is_prime(i)]
    primes = sorted(primes, key=lambda x: (str(bin(x)).count('1'), -x))
    if len(primes) > 10:
        primes = primes[0:10]
    return [str(i) for i in primes]


def encrypt(e, n, key):
    return fast_pow(key, e) % n
