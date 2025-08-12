from petlib.ec import EcGroup
from hashlib import sha256
from phe import paillier
import random

# 选择椭圆曲线群 secp256k1
G = EcGroup(714)

def hash_to_group(val: bytes):
    # 哈希映射到群的点
    digest = sha256(val).digest()
    # 转成int做标量乘法
    h_int = int.from_bytes(digest, "big")
    return G.hash_to_point(digest)

def random_exponent():
    return G.order().random()

# Paillier密钥生成
def paillier_keygen():
    return paillier.generate_paillier_keypair()

# Paillier加密
def paillier_encrypt(pubkey, val):
    return pubkey.encrypt(val)

# Paillier加密的同态加法
def paillier_add(c1, c2):
    return c1 + c2

# Paillier随机化（加密的重新加密）
def paillier_randomize(pubkey, ciphertext):
    # 通过加密0随机化
    r = pubkey.encrypt(0)
    return ciphertext + r

