# demo.py
# 运行示例，完整演示三轮交互
from protocol import Party1, Party2
from Crypto.Util.number import getPrime

def main():
    # 1) 选择群参数 p, g（演示用 512-bit）
    bits = 512
    p = getPrime(bits)
    # 选择 g 为 [2, p-2] 中随机数（在真实实现要选 generator）
    import secrets
    g = secrets.randbelow(p - 3) + 2

    # 2) 双方输入
    V = ["alice@example.com", "bob@example.com", "carol@example.com"]  # P1 标识符
    W = [("bob@example.com", 5), ("dan@example.com", 3), ("carol@example.com", 2)]  # P2 (id, value)

    # 3) 初始化双方
    p1 = Party1(V, p, g)
    p2 = Party2(W, p, g)

    # Round1: P1 -> P2
    Z_from_p1 = p1.round1_send()

    # Round2: P2 处理并返回 Z_full 和 (H(w)^k2, Enc(t))
    Z_full, pairs = p2.round2_process(Z_from_p1)

    # Round2 step2: P2 先把 Z_full 发回给 P1
    # Round2 step4 already included in pairs

    # Round3: P1 处理 pairs 和 Z_full，得到 Enc(sum)
    sum_enc = p1.round3_process(Z_full, pairs, p2.pk)

    # Output: P2 解密
    intersection_sum = p2.decrypt_sum(sum_enc)

    print("P1 集合 V:", V)
    print("P2 集合 W (id, value):", W)
    print("交集对应值的和 (P2 解密得到):", intersection_sum)

if __name__ == "__main__":
    main()
