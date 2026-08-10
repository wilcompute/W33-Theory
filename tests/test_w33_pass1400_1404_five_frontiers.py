import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CERT=ROOT/'data'/'w33_pass1400_1404_five_frontiers.json'
REPORT=ROOT/'analysis'/'BT1400_BT1404_five_frontiers.md'
DIGEST='6a6f5e3fb2eb441214057186c974573e99e983e9b665994842538b2647587b2b'
def load(): return json.loads(CERT.read_text(encoding="utf-8"))
def test_frozen():
 d=load(); assert d['schema']=='w33.pass1400_1404.five_frontiers.v1' and d['status']=='PASS'
 assert hashlib.sha256(CERT.read_bytes()).hexdigest()==DIGEST
 assert set(d['workers'])=={'1400','1401','1402','1403','1404'}
def test_1400():
 p=load()['pass1400']; assert p['localization']['2']=={'collapsed_projectors':13,'localizable_projectors':1}
 assert p['localization']['3']=={'collapsed_projectors':14,'localizable_projectors':0}
 assert p['localization']['5']=={'collapsed_projectors':0,'localizable_projectors':14}
 assert p['radicals']=={'2':[45,16,0],'3':[72,49,27,14,4,0],'5':[0]}
def test_1401():
 p=load()['pass1401']; assert p['sizes']==[1,2,4,4,8,8] and p['axis']==[1,0,1]
 assert p['quadratic_form']==[[2,0],[0,2]]
def test_1402():
 p=load()['pass1402']; assert sum(p['blocks'])==120 and p['U']['den']==54 and p['Uinv']['den']==3
 assert set(p['operators'])=={'A','D','S'}
def test_1403():
 p=load()['pass1403']; assert p['sheet']==[2160,160,81,True]
 assert {v[0] for v in p['bridges'].values()}=={81} and all(v[1] for v in p['bridges'].values())
 assert p['mackey_ranks']==[1,2,2,4,4,8,8,2,4,12,12,24,32,5]
def test_1404():
 p=load()['pass1404']; assert p['containment']==[False,False] and p['intersection_indices'][1]=='4'
 assert p['levels']==[2,108] and p['disc_factors']=={'2':72,'3':226}
 assert p['local']=={'2':False,'3':False,'5':True}
def test_sources():
 parts=sorted((ROOT/'analysis'/'_selector_five_frontiers_impl.src').glob('part*.pyfrag'))
 assert len(parts)==9 and sum(len(p.read_text(encoding="utf-8").splitlines()) for p in parts)==678
def test_report_digest_is_current():
 text=REPORT.read_text(encoding="utf-8")
 assert DIGEST in text
 assert 'a2e8a580576d6c38cb584f402c1d16ee49a029a4fe545cf239d39043fc890afd' not in text
 assert (ROOT/'tools'/'check_pass1400_1404_worker.py').exists()
