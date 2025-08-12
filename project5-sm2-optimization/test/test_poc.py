import sys
import os
from src.sm2_basic import n
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))


import unittest
from sm2_poc_forgery import leak_private_key_from_reused_k, sign_with_fixed_k
from sm2_basic import sm2_keygen, sm2_sign, sm2_verify


class TestSM2PoC(unittest.TestCase):
    def test_leak_private_key(self):
        d, P = sm2_keygen()
        k = 987654321
        msg1 = b"msg1"
        msg2 = b"msg2"
        sig1 = sign_with_fixed_k(d, msg1, k)
        sig2 = sign_with_fixed_k(d, msg2, k)
        leaked_d = leak_private_key_from_reused_k(msg1, sig1, msg2, sig2)
        self.assertEqual(d % n, leaked_d % n)


if __name__ == "__main__":
    unittest.main()
