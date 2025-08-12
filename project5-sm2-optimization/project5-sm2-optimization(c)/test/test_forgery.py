import unittest
import random
from params import Gx, Gy, n
from ecc import Point, point_mul
from forge import forge_signature, verify_signature, G

class TestForgery(unittest.TestCase):
    def setUp(self):
        self.Q = point_mul(123456789, G)  # 用私钥生成公钥

    def test_forgery(self):
        u = random.randint(1, n-1)
        v = random.randint(1, n-1)
        (r, s), e = forge_signature(self.Q, u, v)
        self.assertTrue(verify_signature(self.Q, e, (r, s)))

if __name__ == "__main__":
    unittest.main()
