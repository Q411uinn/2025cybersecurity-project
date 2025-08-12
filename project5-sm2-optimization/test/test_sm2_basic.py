import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))


import unittest
from sm2_poc_forgery import leak_private_key_from_reused_k, sign_with_fixed_k
from sm2_basic import sm2_keygen, sm2_sign, sm2_verify



class TestSM2Basic(unittest.TestCase):
    def test_sign_verify(self):
        d, P = sm2_keygen()
        msg = b"test message"
        sig = sm2_sign(d, msg)
        self.assertTrue(sm2_verify(P, msg, sig))

if __name__ == "__main__":
    unittest.main()
