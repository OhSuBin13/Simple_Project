import random
import sys
sys.setrecursionlimit(2048)  # default = 1000: sys.getrecursionlimit()

"""
GCD(assume a>=0, b>=0 )
"""
def gcd(a, b):
    if a < b:
        a, b = b, a
    if a == b:
        return a
    elif b == 0:
        return a
    else:
        return gcd(b, a % b)


"""
miller-rabin prime test
Test if n is prime with error probability less than 1/2^n.
"""
Prime = 0
Composite = 1
def miller_rabin(n, s):
    if n == 2:
        return Prime
    elif n % 2 == 0:
        return Composite

    for _ in range(s):
        a = random.randint(1, n-1)
        if test(a, n) == True:
            return Composite

    return Prime

"""
subroutine for miller-rabin prime test
Perform the Fermat test and NSR (nontrivial square root) test.
"""
def test(a, n):
    bits = int_to_bin(n-1)
    k = len(bits) - 1
    t = 0

    while bits[k] == '0':
        t += 1
        k -= 1

    u = (n-1) >> t     # n - 1 is represented as u * (2**t)
    x = exp(a, u, n)
    for _ in range(t):
        _x = x
        x = (_x * _x) % n
        if x == 1 and _x != 1 and _x != n-1:
            return True

    if x != 1:
        return True
    else:
        return False

"""
int_to_bin
convert an integer to a binary representation
(the most significant bit becomes the 0-th bit)
"""
def int_to_bin(num):
    return list(bin(num))[2:]

"""
Modular exponentiation
returns a ** b mod n
"""
def exp(a, b, n):
    c = 0
    f = 1
    bin_b = int_to_bin(b)
    k = len(bin_b)
    for i in range(k):   # Fill this part.
        c = 2 * c
        f = (f * f) % n
        if bin_b[i] == '1':
            c = c + 1
            f = (f * a) % n
    return f

"""
RSA key pair generation
keylen: security parameter (desired number of bits in n)
    (keylen > 4)
"""
def keygen(keylen):
    bound = 1 << keylen//2   # upper bound for p and q.
    p = 2 * random.randint(bound//4, bound//2) - 1       # guarantee that p is odd.
    while miller_rabin(p, 50) == Composite:
        p = 2 * random.randint(bound//4, bound//2) - 1   # select new odd p.
    q = 2 * random.randint(bound//4, bound//2) - 1       # guarantee that q is odd.
    while miller_rabin(q, 50) == Composite:
        q = 2 * random.randint(bound//4, bound//2) - 1   # select new odd q.
    # Now p and q are odd primes.
    # Compute n.
    # find e appropriately.
    # find d appropriately.
    # Hint: You may compute x^-1 mod m by pow(x, -1, m)
    n = p * q
    totient = (p-1) * (q-1)
    e = random.randint(2, totient-1)
    while gcd(totient, e) != 1:
        e = random.randint(2, totient - 1)
    d = pow(e, -1, totient)
    return (e, d, n)


"""
RSA encryption
e, n: public key
M: plaintext < n
"""
def encrypt(M, e, n):
    return exp(M, e, n)

"""
RSA decryption
d, n: private key
C: ciphertext < n
"""
def decrypt(C, d, n):
    return exp(C, d, n)

"""
RSA test
"""
if __name__ == "__main__":
    e, d, n = keygen(128)
    M = 88
    C = encrypt(M, e, n)
    MM = decrypt(C, d, n)
    if M == MM:
        print("Example of RSA Algorithm works successfully")
        print("M={}, PU=({},{}), PR=({},{}), C={}, MM={}".format(M, e, n, d, n, C, MM))
    else:
        print("Example of RSA Algorithm fails")
        print("M={}, PU=({},{}), PR=({},{}), C={}, MM={}".format(M, e, n, d, n, C, MM))
