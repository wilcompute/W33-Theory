import base64, gzip, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def test_frozen_complete_cover_signature_certificate():
 p=json.loads((ROOT/'data'/'w33_pass1821_1825_complete_cover_signature.json').read_text(encoding="utf-8"))
 assert p['status']=='PASS' and all(p['checks'].values())
 assert p['pass1821_complete_cover_census']['global_covers']==3_547_800
 assert p['pass1821_complete_cover_census']['cover_orbits']==327
 assert p['pass1822_nonlinear_signature_classification']['global_signature_vectors']==720
 assert p['pass1823_packing_signature_obstruction']['exact_meet_in_the_middle']['completion_exists'] is False
 q=json.loads(gzip.decompress(base64.b64decode((ROOT/'data'/'w33_pass1825_signatures720.json.gz.b64').read_text(encoding="utf-8"))).decode())
 assert q['shape']==[720,45] and len(q['signatures'])==720 and len(q['class_labels'])==720
