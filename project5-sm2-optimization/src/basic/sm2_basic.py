from hashlib import sha256
from src.utils import mod_inv
from collections import namedtuple
Point = namedtuple('Point', ['x', 'y'])


p = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
a = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
b = 0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93
n = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123
Gx = 0x32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7
Gy = 0xBC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __repr__(self):
        return f"Point({hex(self.x)}, {hex(self.y)})"

def point_add(P, Q):
    if P is None:
        return Q
    if Q is None:
        return P
    if P.x == Q.x and (P.y != Q.y or P.y == 0):
        return None  # 无穷远点
    if P.x == Q.x:
        # 点加法切线斜率
        lam = (3 * P.x * P.x + a) * mod_inv(2 * P.y, p) % p
    else:
        lam = (Q.y - P.y) * mod_inv(Q.x - P.x, p) % p
    x3 = (lam * lam - P.x - Q.x) % p
    y3 = (lam * (P.x - x3) - P.y) % p
    return Point(x3, y3)


def point_mul(k, P):
    R = None
    addend = P
    while k:
        if k & 1:
            R = point_add(R, addend)
        addend = point_add(addend, addend)
        k >>= 1
    return R

def sm2_keygen():
    import random
    d = random.randint(1, n - 1)
    P = point_mul(d, Point(Gx, Gy))
    return d, P

def sm2_sign(d, msg):
    e = int.from_bytes(sha256(msg).digest(), 'big')
    import random
    while True:
        k = random.randint(1, n - 1)
        P1 = point_mul(k, Point(Gx, Gy))
        r = (e + P1.x) % n
        if r == 0 or r + k == n:
            continue
        s = (mod_inv(1 + d, n) * (k - r * d)) % n
        if s != 0:
            break
    return (r, s)

def sm2_verify(P, msg, sig):
    r, s = sig
    e = int(sha256(msg).hexdigest(), 16)
    t = (r + s) % n
    if t == 0:
        return False
    P1 = point_add(point_mul(s, Point(Gx, Gy)), point_mul(t, P))
    R = (e + P1.x) % n
    return R == r

if __name__ == "__main__":
    d, P = sm2_keygen()
    msg = b'hello sm2'
    sig = sm2_sign(d, msg)
    print("私钥 d:", hex(d))
    print("公钥 P:", P)
    print("消息:", msg)
    print("签名:", sig)
    print("签名验证:", sm2_verify(P, msg, sig))
