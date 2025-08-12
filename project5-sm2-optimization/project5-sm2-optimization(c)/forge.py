# forgery.py
from params import p, n, Gx, Gy
from ecc import Point, point_add, point_mul, mod_inv

G = Point(Gx, Gy)

def forge_signature(Q, u, v):
    R = point_add(point_mul(u, G), point_mul(v, Q))
    if R is None:
        raise Exception("R是无穷远点")
    r = R.x % n
    if r == 0:
        raise Exception("r=0无效")
    s = (r * mod_inv(v, n)) % n
    e = (u * s) % n
    return (r, s), e


def verify_signature(Q, e, sig):
    r, s = sig
    if not (1 <= r <= n-1) or not (1 <= s <= n-1):
        return False
    w = mod_inv(s, n)
    u1 = (e * w) % n
    u2 = (r * w) % n
    R = point_add(point_mul(u1, G), point_mul(u2, Q))
    if R is None:
        return False
    # 注意这里先对 p 取模
    x1_mod_p = R.x % p
    # 再和 e 做 mod n 的加法
    return r == (x1_mod_p + e) % n


