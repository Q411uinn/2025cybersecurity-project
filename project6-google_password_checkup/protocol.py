# protocol.py
# DDH-based Private Intersection-Sum simplified demo (按 Figure 2 流程)
import hashlib, secrets, random
from paillier import generate_keypair

# 选用大素数 p 和生成元 g，作为乘法群 (Z_p^*)
# 为 demo 目的我们用安全素数生成（实际可用固定安全参数）
from Crypto.Util.number import getPrime

def hash_to_int(x: bytes, p: int):
    """把标识符哈希到 [0, p-1) 上，再用 g^h 得到群元素表示"""
    h = hashlib.sha256(x).digest()
    i = int.from_bytes(h, "big") % (p - 1)  # 指数用 p-1 的模
    return i

class Party1:
    def __init__(self, V, p, g):
        self.V = V  # 标识符列表（字符串）
        self.p = p
        self.g = g
        self.k1 = secrets.randbelow(p - 1)  # 私钥 exponent

    def round1_send(self):
        # 对每个 v 计算 H(v)^{k1} = g^{hash(v) * k1}
        Z = []
        for v in self.V:
            h = hash_to_int(v.encode(), self.p)
            z = pow(self.g, (h * self.k1) % (self.p - 1), self.p)
            Z.append(z)
        random.shuffle(Z)
        return Z

    def round3_process(self, Z_full, pairs_from_p2, pk):
        """
        pairs_from_p2: list of (h_w_k2, Enc(tj)) 其中 h_w_k2 = g^{hash(w_j)*k2} mod p
        Z_full: list of H(v)^{k1*k2} returned by P2 in Round2 (the Z set)
        """
        # 对 pairs 中的第一个分量再指数 k1，得到 H(w_j)^{k1*k2}
        transformed = []
        for h_w_k2, enc_t in pairs_from_p2:
            h_w_k1k2 = pow(h_w_k2, self.k1, self.p)
            transformed.append((h_w_k1k2, enc_t))

        # 计算交集索引 J：h_w_k1k2 在 Z_full 中的那些
        setZ = set(Z_full)
        J = [i for i, (val, _) in enumerate(transformed) if val in setZ]

        # 同态求和对应的密文
        if not J:
            # 返回 Enc(0)
            return pk.encrypt(0)

        sum_enc = transformed[J[0]][1]
        for idx in J[1:]:
            sum_enc = pk.add(sum_enc, transformed[idx][1])
        # 随机化后发送回去
        sum_enc = pk.randomize(sum_enc)
        return sum_enc


class Party2:
    def __init__(self, W_pairs, p, g):
        """
        W_pairs: list of tuples (w_j (str), t_j (int))
        """
        self.W = W_pairs
        self.p = p
        self.g = g
        self.k2 = secrets.randbelow(p - 1)
        self.pk, self.sk = generate_keypair(bits=1024)

    def round2_process(self, Z_from_p1):
        # 对 P1 发来的 H(v)^{k1} 每个再指数 k2 -> H(v)^{k1*k2}
        Z_full = [pow(z, self.k2, self.p) for z in Z_from_p1]

        # 对自己的 (w_j, t_j) 计算 (H(w_j)^{k2}, AEnc(t_j))
        pairs = []
        for w, t in self.W:
            h = hash_to_int(w.encode(), self.p)
            h_w_k2 = pow(self.g, (h * self.k2) % (self.p - 1), self.p)
            enc_t = self.pk.encrypt(t)
            pairs.append((h_w_k2, enc_t))
        random.shuffle(pairs)
        return Z_full, pairs

    def decrypt_sum(self, sum_enc):
        return self.sk.decrypt(sum_enc)
