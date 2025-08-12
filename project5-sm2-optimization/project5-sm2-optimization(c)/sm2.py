# sm2.py
import hashlib
import random

# SM2 curve parameters (推荐国密 SM2 椭圆曲线参数)
p = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
a = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
b = 0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93
n = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123
Gx = 0x32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7
Gy = 0xBC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0

def mod_inv(a, m):
    """模逆元"""
    return pow(a, m - 2, m)

def point_add(P, Q):
    """椭圆曲线点加"""
    if P is None: return Q
    if Q is None: return P
    if P[0] == Q[0] and (P[1] + Q[1]) % p == 0:
        return None
    if P == Q:
        lam = (3 * P[0] * P[0] + a) * mod_inv(2 * P[1], p) % p
    else:
        lam = (Q[1] - P[1]) * mod_inv(Q[0] - P[0], p) % p
    x_r = (lam * lam - P[0] - Q[0]) % p
    y_r = (lam * (P[0] - x_r) - P[1]) % p
    return (x_r, y_r)

def scalar_mult(k, P):
    """标量乘法"""
    R = None
    while k:
        if k & 1:
            R = point_add(R, P)
        P = point_add(P, P)
        k >>= 1
    return R

def hash_sm3(msg: bytes) -> int:
    """SM2/SM3 简化版用 sha256 代替"""
    return int.from_bytes(hashlib.sha256(msg).digest(), 'big')

def sign(private_key, msg: bytes):
    e = hash_sm3(msg)
    while True:
        k = random.randrange(1, n)
        x1, y1 = scalar_mult(k, (Gx, Gy))
        r = (e + x1) % n
        if r == 0 or r + k == n:
            continue
        s = (mod_inv(1 + private_key, n) * (k - r * private_key)) % n
        if s != 0:
            break
    return (r, s)

def verify(public_key, msg: bytes, signature):
    r, s = signature
    e = hash_sm3(msg)
    t = (r + s) % n
    if t == 0:
        return False
    x1, y1 = point_add(scalar_mult(s, (Gx, Gy)), scalar_mult(t, public_key))
    R = (e + x1) % n
    return R == r
