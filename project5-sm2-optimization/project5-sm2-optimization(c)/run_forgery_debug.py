# run_forgery_debug.py
import random
from params import n
from ecc import Point, point_mul
from forge import forge_signature, verify_signature, G

def debug_once(seed=None):
    if seed is not None:
        random.seed(seed)
    # 选择一个私钥并计算 Q（测试用）
    d = 123456789  # 固定私钥以便重现
    Q = point_mul(d, G)
    # 随机 u, v
    u = random.randint(1, n-1)
    v = random.randint(1, n-1)
    (r, s), e = forge_signature(Q, u, v)
    ok = verify_signature(Q, e, (r, s))
    print("final verify result:", ok)
    return {
        "d": d, "u": u, "v": v, "r": r, "s": s, "e": e, "verify_ok": ok
    }

if __name__ == "__main__":
    debug_once(seed=42)
