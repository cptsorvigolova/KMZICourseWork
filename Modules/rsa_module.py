from Modules.math_module import is_coprime, is_prime


def get_open_exp_candidates(r):
    primes = [i for i in range(r, max(-1, r - 100000), -1) if is_coprime(r, i) and is_prime(i)]
    primes = sorted(primes, key=lambda x: (str(bin(x)).count('1'), -x))
    if len(primes) > 10:
        primes = primes[0:10]
    return [str(i) for i in primes]
