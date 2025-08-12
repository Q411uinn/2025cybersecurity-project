from hashlib import sha256
from src.utils import mod_inv
from sm2_basic import point_mul, point_add, Point, Gx, Gy, n

def int_from_hash(msg):
    return int.from_bytes(sha256(msg).digest(), 'big')

def sign_with_fixed_k(d, msg, k):
    e = int.from_bytes(sha256(msg).digest(), 'big')
    P1 = point_mul(k, Point(Gx, Gy))
    r = (e + P1.x) % n
    s = (mod_inv(1 + d, n) * (k - r * d)) % n
    return (r, s)

def leak_private_key_from_reused_k(msg1, sig1, msg2, sig2):
    r1, s1 = sig1
    r2, s2 = sig2
    numerator = (s1 - s2) % n
    denominator = (r2 - r1 - (s1 - s2)) % n
    inv_denominator = mod_inv(denominator, n)
    d = (numerator * inv_denominator) % n
    return d





if __name__ == "__main__":
    import random
    d, P = sm2_keygen()
    print("真实私钥:", hex(d))
    k = 123456789  # 固定随机数，模拟重用k
    msg1 = b"message1"
    msg2 = b"message2"
    sig1 = sign_with_fixed_k(d, msg1, k)
    sig2 = sign_with_fixed_k(d, msg2, k)
    print("签名1:", sig1)
    print("签名2:", sig2)
    leaked_d = leak_private_key_from_reused_k(msg1, sig1, msg2, sig2)
    print("原始d:", d)
    print("泄露d:", leaked_d)
    print("d % n:", d % n)
    print("leaked_d % n:", leaked_d % n)
    print("相等吗？", (d % n) == (leaked_d % n))
