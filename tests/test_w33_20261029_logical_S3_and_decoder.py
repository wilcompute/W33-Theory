"""Regression for W33 logical S3 and ideal weight-2 Pauli correction."""
import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"analysis"))
from w33_20261029_logical_S3_and_ideal_t2_decoder import main
class TestNativeGateAndDecoder(unittest.TestCase):
    def test_all(self):
        x=main()
        self.assertEqual(x["status"],"PASS")
        self.assertEqual(x["ideal_decoder"]["syndromes"],821)
        self.assertEqual(x["ideal_decoder"]["checked_pauli_errors"],7141)
        self.assertEqual(x["uniform_H_S_logical_group"]["order"],6)
if __name__=="__main__":unittest.main()
