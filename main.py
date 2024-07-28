import random

def is_prime(n, k=5): # k, num of tests
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False

    def miller_rabin_test(d, n):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            return True
        while d != n - 1:
            x = (x * x) % n
            d *= 2
            if x == 1:
                return False
            if x == n - 1:
                return True
        return False

    d = n - 1
    while d % 2 == 0:
        d //= 2

    for _ in range(k):
        if not miller_rabin_test(d, n):
            return False
    return True

def generate_prime_candidate(length):
    p = random.getrandbits(length)
    p |= (1 << length - 1) | 1
    return p

def generate_prime_number(length=1024):
    p = generate_prime_candidate(length)
    while not is_prime(p):
        p = generate_prime_candidate(length)
    return p

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def extended_gcd(a, b):
    x0, x1, y0, y1 = 1, 0, 0, 1
    while b != 0:
        q, a, b = a // b, b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return a, x0, y0

def mod_inverse(a, m):
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        raise Exception("err")
    else:
        return x % m

def generate_keypair(length=1024):
    p = generate_prime_number(length)
    q = generate_prime_number(length)
    while q == p:
        q = generate_prime_number(length)

    n = p * q
    phi = (p - 1) * (q - 1)

    e = random.randrange(2, phi)
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(2, phi)
        g = gcd(e, phi)

    d = mod_inverse(e, phi)
    return ((e, n), (d, n))

def encrypt(pk, plaintext):
    key, n = pk
    cipher = [pow(ord(char), key, n) for char in plaintext]
    return cipher

def decrypt(pk, ciphertext):
    key, n = pk
    plain = [chr(pow(char, key, n)) for char in ciphertext]
    return ''.join(plain)

public, private = generate_keypair()

print(f"Public key: {public}")
print(f"Private key: {private}")
msg = "Hello, RSA!"
encrypted_msg = encrypt(public, msg)
print(f"Encrypted msg: {encrypted_msg}")

decrypted_msg = decrypt(private, encrypted_msg)
print(f"Decrypted msg: {decrypted_msg}")
