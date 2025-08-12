# paillier.py
# 简单 Paillier 实现（教学/demo 用）
from Crypto.Util.number import getPrime, inverse, GCD
import secrets

def lcm(a, b):
    return a // GCD(a, b) * b

class PaillierPublicKey:
    def __init__(self, n, g):
        self.n = n
        self.g = g
        self.n2 = n * n

    def encrypt(self, m):
        """加密整数 m"""
        if not (0 <= m < self.n):
            raise ValueError("m out of range")
        while True:
            r = secrets.randbelow(self.n)
            if r > 0 and GCD(r, self.n) == 1:
                break
        c = (pow(self.g, m, self.n2) * pow(r, self.n, self.n2)) % self.n2
        return c

    def randomize(self, c):
        """对密文重新随机化（等价于乘上 Enc(0)）"""
        while True:
            r = secrets.randbelow(self.n)
            if r > 0 and GCD(r, self.n) == 1:
                break
        return (c * pow(r, self.n, self.n2)) % self.n2

    def add(self, c1, c2):
        """同态加法（密文乘法）"""
        return (c1 * c2) % self.n2

class PaillierPrivateKey:
    def __init__(self, public_key, lam, mu):
        self.public_key = public_key
        self.lam = lam
        self.mu = mu

    def decrypt(self, c):
        n = self.public_key.n
        n2 = self.public_key.n2
        u = pow(c, self.lam, n2)
        L = (u - 1) // n
        m = (L * self.mu) % n
        return m

def generate_keypair(bits=1024):
    """生成 Paillier 密钥对"""
    p = getPrime(bits // 2)
    q = getPrime(bits // 2)
    n = p * q
    lam = lcm(p - 1, q - 1)
    g = n + 1  # 常用选择
    n2 = n * n
    # mu = (L(g^lambda mod n^2))^{-1} mod n
    u = pow(g, lam, n2)
    L = (u - 1) // n
    mu = inverse(L, n)
    pk = PaillierPublicKey(n, g)
    sk = PaillierPrivateKey(pk, lam, mu)
    return pk, sk
