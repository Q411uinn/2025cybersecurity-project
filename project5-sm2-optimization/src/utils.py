def mod_inv(a, m):
    # 扩展欧几里得算法
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise ValueError("No modular inverse")
    else:
        return x % m

def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    else:
        g, x1, y1 = extended_gcd(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return g, x, y
