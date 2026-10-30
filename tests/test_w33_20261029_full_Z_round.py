"""Long exhaustive W33 full sequential Z-round regression.

Run with:
  W33_EXHAUSTIVE=1 python -m unittest tests/test_w33_20261029_full_Z_round.py -v
Runs 52,659,454 history classes including no-fault, and may use substantial RAM.
"""
import os,unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"analysis"))
class FullZRound(unittest.TestCase):
 @unittest.skipUnless(os.getenv("W33_EXHAUSTIVE")=="1","Opt-in: 52.7M cases, substantial RAM")
 def test_global_readout_uniqueness(self):
  from w33_20261029_seven_flag_full_Z_round_two_fault import run
  r=run()
  self.assertEqual(r["total_histories"],52659454)
  self.assertEqual(r["distinct_observation_records"],1844033)
  self.assertEqual(r["ambiguous_observation_records"],0)
if __name__=="__main__":unittest.main()
