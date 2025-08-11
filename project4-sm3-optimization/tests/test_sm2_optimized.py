import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from optimized import sm2_optimized as sm2
import unittest

ID = b"1234567812345678"  # 这里统一写ID

class TestSM2Optimized(unittest.TestCase):

    def test_keygen_and_sign_verify(self):
        d, P = sm2.sm2_keygen()
        msg = b"hello optimized sm2"
        sig = sm2.sm2_sign(d, P, msg, ID=ID)
        self.assertTrue(sm2.sm2_verify(P, msg, sig, ID=ID))

    def test_wrong_signature(self):
        d, P = sm2.sm2_keygen()
        msg = b"message"
        sig = sm2.sm2_sign(d, P, msg, ID=ID)
        fake_sig = (sig[0], (sig[1] + 1) % sm2.n)
        self.assertFalse(sm2.sm2_verify(P, msg, fake_sig, ID=ID))

    def test_deterministic_properties(self):
        d1, P1 = sm2.sm2_keygen()
        d2, P2 = d1, sm2.point_mul_naf(d1, sm2.G).to_affine()
        self.assertEqual(P1, P2)

if __name__ == "__main__":
    unittest.main()
