from hashlib import sha256
from basic.utils import mod_inv
from optimized import sm2_optimized as sm2
ID = b"1234567812345678"  # 标准SM2默认ID示例，16字节

# SM2参数（和基础版一致）
p = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
a = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
b = 0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93
n = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123
Gx = 0x32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7
Gy = 0xBC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0

# 雅可比坐标点
class PointJacobi:
    def __init__(self, X, Y, Z):
        self.X = X
        self.Y = Y
        self.Z = Z

    def to_affine(self):
        if self.Z == 0:
            return None  # 无穷远点
        z_inv = mod_inv(self.Z, p)
        z_inv2 = (z_inv * z_inv) % p
        z_inv3 = (z_inv2 * z_inv) % p
        x = (self.X * z_inv2) % p
        y = (self.Y * z_inv3) % p
        return (x, y)

# 生成基点雅可比坐标形式
G = PointJacobi(Gx, Gy, 1)

# 点加法（雅可比坐标，不用模逆）
def point_add_jacobi(P, Q):
    if P.Z == 0:
        return Q
    if Q.Z == 0:
        return P

    U1 = (P.X * pow(Q.Z, 2, p)) % p
    U2 = (Q.X * pow(P.Z, 2, p)) % p
    S1 = (P.Y * pow(Q.Z, 3, p)) % p
    S2 = (Q.Y * pow(P.Z, 3, p)) % p

    if U1 == U2:
        if S1 != S2:
            return PointJacobi(0, 1, 0)  # 无穷远点
        else:
            return point_double_jacobi(P)

    H = (U2 - U1) % p
    R = (S2 - S1) % p
    H2 = (H * H) % p
    H3 = (H * H2) % p
    U1H2 = (U1 * H2) % p

    X3 = (R * R - H3 - 2 * U1H2) % p
    Y3 = (R * (U1H2 - X3) - S1 * H3) % p
    Z3 = (H * P.Z * Q.Z) % p

    return PointJacobi(X3, Y3, Z3)

# 点倍运算（雅可比坐标）
def point_double_jacobi(P):
    if P.Z == 0:
        return P

    W = (3 * P.X * P.X + a * pow(P.Z, 4, p)) % p
    S = (P.Y * P.Z) % p
    B = (P.X * P.Y * S) % p
    H = (W * W - 8 * B) % p
    X3 = (2 * H * S) % p
    Y3 = (W * (4 * B - H) - 8 * pow(P.Y, 4, p) * pow(S, 2, p)) % p
    Z3 = (8 * S * S * S) % p

    return PointJacobi(X3, Y3, Z3)




# 窗口NAF（w=4）预计算和标量乘法
def window_naf(k, width=4):
    """
    返回窗口NAF表示的列表，方便快速标量乘法
    """
    naf = []
    while k > 0:
        if k & 1:
            mod = k % (1 << width)
            if mod > (1 << (width - 1)):
                val = mod - (1 << width)
            else:
                val = mod
            k -= val
            naf.append(val)
        else:
            naf.append(0)
        k >>= 1
    return naf

def precompute_points(P, width=4):
    # 预计算 [1*P, 3*P, 5*P, ..., (2^{w-1}-1)*P]
    precomp = []
    precomp.append(P)
    twoP = point_double_jacobi(P)
    for i in range(1, (1 << (width - 1)) - 1):
        precomp.append(point_add_jacobi(precomp[-1], twoP))
    return precomp

def point_mul_naf(k, P, width=4):
    naf = window_naf(k, width)
    precomp = precompute_points(P, width)
    R = PointJacobi(0, 1, 0)  # 无穷远点

    for i in reversed(naf):
        R = point_double_jacobi(R)
        if i != 0:
            if i > 0:
                R = point_add_jacobi(R, precomp[(i - 1) // 2])
            else:
                neg_point = PointJacobi(precomp[(-i - 1) // 2].X, p - precomp[(-i - 1) // 2].Y, precomp[(-i - 1) // 2].Z)
                R = point_add_jacobi(R, neg_point)
    return R

def get_ZA(ID, P):
    ENTLA = len(ID) * 8
    a_bytes = a.to_bytes(32, 'big')
    b_bytes = b.to_bytes(32, 'big')
    Gx_bytes = Gx.to_bytes(32, 'big')
    Gy_bytes = Gy.to_bytes(32, 'big')
    Px_bytes = P[0].to_bytes(32, 'big')
    Py_bytes = P[1].to_bytes(32, 'big')
    data = ENTLA.to_bytes(2, 'big') + ID + a_bytes + b_bytes + Gx_bytes + Gy_bytes + Px_bytes + Py_bytes
    return sha256(data).digest()
# 密钥生成
def sm2_keygen():
    import random
    d = random.randint(1, n - 1)
    P = point_mul_naf(d, G)
    return d, P.to_affine()

def sm2_sign(d, P_affine, msg, ID=b"1234567812345678"):
    e = int(sha256(get_ZA(ID, P_affine) + msg).hexdigest(), 16)
    import random
    PA = PointJacobi(P_affine[0], P_affine[1], 1)  # 转雅可比坐标
    while True:
        k = random.randint(1, n - 1)
        P1 = point_mul_naf(k, G).to_affine()
        r = (e + P1[0]) % n
        if r == 0 or r + k == n:
            continue
        s = (mod_inv(1 + d, n) * (k - r * d)) % n
        if s != 0:
            break
    return (r, s)


def sm2_verify(P, msg, sig, ID=b"1234567812345678"):
    r, s = sig
    if not (1 <= r <= n - 1) or not (1 <= s <= n -1):
        return False
    e = int(sha256(get_ZA(ID, P) + msg).hexdigest(), 16)

    t = (r + s) % n
    if t == 0:
        return False
    Px, Py = P
    PA = PointJacobi(Px, Py, 1)
    sG = point_mul_naf(s, G)
    tP = point_mul_naf(t, PA)
    P1 = point_add_jacobi(sG, tP)
    x1, _ = P1.to_affine()
    R = (e + x1) % n

    # 打印调试信息（改成仿射坐标）
    print("sG:", sG.to_affine())
    print("tP:", tP.to_affine())
    print("P1:", P1.to_affine())
    print("r:", r)
    print("R:", R)

    return R == r

