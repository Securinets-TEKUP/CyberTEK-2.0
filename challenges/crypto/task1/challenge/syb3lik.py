#!/usr/bin/env python3
from Crypto.Util.number import inverse
from Crypto.Cipher import AES
from collections import namedtuple
import random, sys, os, hashlib

FLAG = open("flag.txt", "r").read().strip() if os.path.exists("flag.txt") else "None"
if not FLAG:
    print("Flag file not found!")
    sys.exit(1)

WELCOME = """
Welcome to my Invincible Game!

If you can decrypt all my messages, you win the flag.
"""

Point = namedtuple("Point", "x y")

class EllipticCurve:
    INF = Point(0, 0)

    def __init__(self, a, b, Gx, Gy, p):
        self.a = a
        self.b = b
        self.p = p
        self.G = Point(Gx, Gy)

    def add(self, P, Q):
        if P == self.INF:
            return Q
        if Q == self.INF:
            return P
        if P.x == Q.x and P.y == (-Q.y % self.p):
            return self.INF
        if P != Q:
            tmp = (Q.y - P.y) * inverse(Q.x - P.x, self.p) % self.p
        else:
            tmp = (3 * P.x**2 + self.a) * inverse(2 * P.y, self.p) % self.p
        Rx = (tmp**2 - P.x - Q.x) % self.p
        Ry = (tmp * (P.x - Rx) - P.y) % self.p
        return Point(Rx, Ry)

    def multiply(self, P, n):
        R = self.INF
        while n > 0:
            if n & 1:
                R = self.add(R, P)
            n >>= 1
            P = self.add(P, P)
        return R
p = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
a = -0x3
Gx = 0x55b40a88dcabe88a40d62311c6b300e0ad4422e84de36f504b325b90c295ec1a
Gy = 0xf8efced5f6e6db8b59106fecc3d16ab5011c2f42b4f8100c77073d47a87299d8
b = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b
E = EllipticCurve(a, b, Gx, Gy, p)

class RNG:
    def __init__(self, seed, P, Q):
        self.seed = seed
        self.P = P
        self.Q = Q

    def next(self):
        s = E.multiply(self.P, self.seed).x
        self.seed = s
        r = E.multiply(self.Q, s).x
        return r & ((1 << 128) - 1)

def encrypt(msg, key, iv):
    aes = AES.new(key, AES.MODE_CBC, iv)
    return iv + aes.encrypt(msg)

def main():
    try:
        print(WELCOME)
        print(b"Point x: ")
        Px = int(input().strip())
        print(b"Point y: ")
        Py = int(input().strip())

        P = Point(Px, Py)
        if P == E.INF or Px == 0 or Py == 0:
            print(b"Don't cheat.\n")
            return

        print(f"Your point: ({P.x}, {P.y})\n")
        Q = E.multiply(E.G, random.randrange(1, p-1))
        print(f"My point: ({Q.x}, {Q.y})\n")
        rng = RNG(random.getrandbits(128), P, Q)

        
        for _ in range(3):  
            key = hashlib.sha1(str(rng.next()).encode()).digest()[:16]
            iv = os.urandom(16)
            msg = os.urandom(64)
            cipher = encrypt(msg, key, iv)
            print(f"Ciphertext: {cipher.hex()}\n")

            print(b"Enter decrypted message: ")
            try:
                your_dec = bytes.fromhex(input().strip())
                if your_dec == msg:
                    print(b"Correct!\n")
                else:
                    print(b"Wrong!\n")
                    return
            except:
                print(b"Invalid input!\n")
                return

        
        print(f"Congratulations! Here's your flag: {FLAG}\n")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()