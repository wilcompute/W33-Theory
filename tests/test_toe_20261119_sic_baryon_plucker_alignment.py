"""Independent regression for exact SU3 baryonic SIC and Hesse-line census."""
from pathlib import Path
import subprocess,sys,json,unittest

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"analysis"/"toe_20261119_sic_baryon_plucker_alignment.py"
CERT=ROOT/"data"/"toe_20261119_sic_baryon_plucker_alignment.json"

class TestBaryonHesse(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        r=subprocess.run([sys.executable,str(SCRIPT)],cwd=ROOT,capture_output=True,text=True)
        if r.returncode: raise AssertionError((r.stdout,r.stderr))
        cls.d=json.loads(CERT.read_text(encoding="utf-8"))

    def test_triple_census(self):
        self.assertEqual(self.d["plus"]["baryonic_minor_squared_distribution"],{"0":3,"1":18,"3":54,"4":9})
        self.assertEqual(self.d["minus"]["baryonic_minor_squared_distribution"],{"0":12,"3":72})

    def test_moment_agreement_and_third_split(self):
        self.assertEqual(self.d["plus"]["baryonic_det_squared_moments"],[216,648,2052])
        self.assertEqual(self.d["minus"]["baryonic_det_squared_moments"],[216,648,1944])
        self.assertEqual(self.d["all_84_baryon_minor_third_moment_difference"],108)

    def test_hesse_line_census(self):
        self.assertEqual(self.d["hesse_line_count"],12)
        self.assertEqual(self.d["plus"]["hesse_line_minor_squared_distribution"],{"0":3,"4":9})
        self.assertEqual(self.d["minus"]["hesse_line_minor_squared_distribution"],{"0":12})
        self.assertEqual(self.d["hesse_line_sextic_baryon_sum_plus"],36)
        self.assertEqual(self.d["hesse_line_sextic_baryon_sum_minus"],0)

    def test_physics_boundary(self):
        self.assertIn("not a holomorphic SUSY UV",self.d["limits"])

if __name__=="__main__": unittest.main()
