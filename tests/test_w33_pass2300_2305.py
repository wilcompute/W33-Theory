from __future__ import annotations
import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

CERTS={
 'data/w33_pass2300_ree_tits_divisible_code.json':'dc6a1b4262e96210af832d098a4140f58e022bea979b7cdf3c030246dbf956e9',
 'data/w33_pass2301_complete_quadratic_hom_bases.json':'26eab93605eeb603e3a899c2ecda2a39e268c65e3286b86dce9449f0540b8c43',
 'data/w33_pass2302_q7_q11_extended_weil_outer_inversion.json':'d850de3ddaad56765d692fcdba838e2e05bd13340da0194f56c7996807b651a7',
 'data/w33_pass2304_known_q27_symplectic_spread_spectra.json':'9d3009f348f5fcb1a287a1451f3dcd34131a36f6df72989ae9c3d68e28385017'}

def digest(d):
    x=dict(d);x.pop('sha256_without_hash_field',None)
    return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def test_frozen_semantic_hashes():
    for path,h in CERTS.items():
        d=json.loads((ROOT/path).read_text(encoding="utf-8"))
        assert d['sha256_without_hash_field']==h==digest(d)
        assert all(d['checks'].values())

def test_ree_code_and_family_spectra():
    r=json.loads((ROOT/'data/w33_pass2300_ree_tits_divisible_code.json').read_text(encoding="utf-8"))
    assert sum(r['complete_hyperplane_intersection_spectrum'].values())==551881
    assert r['projective_code']['weight_gcd']==9
    f=json.loads((ROOT/'data/w33_pass2304_known_q27_symplectic_spread_spectra.json').read_text(encoding="utf-8"))
    assert f['complete_results']['regular']['projective_code']['parameters']=='[730,4]_27'
    assert f['complete_results']['regular']['projective_code']['weight_gcd']==27
    for name in ('kantor','thas_payne','ree_tits'):
        assert f['complete_results'][name]['projective_code']['parameters']=='[730,5]_27'
        assert f['complete_results'][name]['projective_code']['weight_gcd']==9

def test_complete_hom_outer_split():
    d=json.loads((ROOT/'data/w33_pass2301_complete_quadratic_hom_bases.json').read_text(encoding="utf-8"))
    assert d['total_dimensions']=={'Sym2':26,'Lambda2':24,'combined':50}
    for kind in ('Sym','Lambda'):
        for target,m in d['full_PSp_Hom_dimensions'][kind].items():
            assert len(d['compressed_orbit_bases'][kind][target])==m
            assert d['outer_involution_split']['even_PGSp_extendible'][kind][target]+d['outer_involution_split']['odd_outer_twisted'][kind][target]==m

def test_weil_full_replay():
    subprocess.run([sys.executable,str(ROOT/'analysis/w33_pass2302_q7_q11_weil_outer_inversion.py'),'--full'],check=True,capture_output=True,text=True)
