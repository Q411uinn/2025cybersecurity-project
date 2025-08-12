def mod_inv(a, m):
    """模逆元，使用费马小定理"""
    return pow(a, m - 2, m)
