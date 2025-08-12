from params import p

class Point:
    def __init__(self, x, y, curve=None):
        self.x = x
        self.y = y
        self.curve = curve

    def __eq__(self, other):
        return isinstance(other, Point) and self.x == other.x and self.y == other.y

# 模逆
def mod_inv(a, m):
    return pow(a % m, -1, m)


# 点加法
def point_add(P, Q):
    if P is not None and not isinstance(P, Point):
        raise TypeError(f"P不是Point类型：{type(P)}")
    if Q is not None and not isinstance(Q, Point):
        raise TypeError(f"Q不是Point类型：{type(Q)}")

    if P is None:
        return Q
    if Q is None:
        return P
    if P.x == Q.x and (P.y != Q.y or P.y == 0):
        return None  # 无穷远点

    if P.x == Q.x:  # P == Q
        lam = ((3 * (P.x % p) * (P.x % p)) % p) * mod_inv((2 * (P.y % p)) % p, p) % p
    else:
        lam = ((Q.y - P.y) % p) * mod_inv((Q.x - P.x) % p, p) % p

    x_r = (lam * lam - P.x - Q.x) % p
    y_r = (lam * (P.x - x_r) - P.y) % p
    return Point(x_r, y_r)

# 标量乘法
def point_mul(k, P):
    if not isinstance(k, int) or k < 0:
        raise ValueError(f"k必须是非负整数，当前k={k}")
    if P is not None and not isinstance(P, Point):
        raise TypeError(f"P不是Point类型：{type(P)}")

    R = None
    addend = P

    while k > 0:
        if k & 1:
            R = point_add(R, addend)
        addend = point_add(addend, addend)
        k >>= 1
    return R

