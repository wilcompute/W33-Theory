from __future__ import annotations
import json
from pathlib import Path

def audit(repo: Path):
    p1080=json.loads((repo/'data/w33_pass1080_contextual_fraction_audit.json').read_text())
    assert abs(p1080['contextual_fraction']['W33']['value']-1.0)<1e-12
    assert abs(p1080['contextual_fraction']['doily']['value'])<1e-12
    manifests=[];bad=[]
    for p in sorted((repo/'hardware').glob('*.json')):
        text=p.read_text();manifests.append(str(p.relative_to(repo)))
        try:obj=json.loads(text)
        except Exception:continue
        stack=[obj]
        while stack:
            x=stack.pop()
            if isinstance(x,dict):
                for k,v in x.items():
                    if 'contextual_fraction' in k.lower() and isinstance(v,(int,float)) and abs(float(v)-0.1)<1e-12:bad.append((str(p),k,v))
                    stack.append(v)
            elif isinstance(x,list):stack.extend(x)
    legacy=(repo/'analysis/bt1901_contextual_fraction_estimator.py').read_text()
    checks={'pass1080_w33_CF_is_one':p1080['contextual_fraction']['W33']['value']==1.0,'pass1080_doily_CF_is_zero':abs(p1080['contextual_fraction']['doily']['value'])<1e-12,'no_hardware_manifest_claims_CF_one_tenth':not bad,'legacy_estimator_has_correction_banner':'does NOT estimate the\nAbramsky-Barbosa contextual fraction' in legacy,'legacy_output_uses_click_rate_name':'corrected_signal_click_rate' in legacy,'legacy_output_does_not_emit_corrected_contextual_fraction':'"corrected_contextual_fraction"' not in legacy,'legacy_target_name_is_click_rate':'TARGET_CLICK_RATE' in legacy}
    assert all(checks.values()),(checks,bad)
    return {'status':'PASS','check_count':len(checks),'checks':checks,'audited_manifests':manifests,'retired_claim':'Abramsky-Barbosa contextual fraction = 1/10','correct_CF':{'W33':1.0,'doily':0.0},'one_tenth_status':'unidentified demonstrator click-rate target; not a contextual fraction and not a valid substrate falsifier until independently derived','scope':'Claim-label firewall. Historical research files may retain the number with explicit correction banners; executable acquisition and analysis surfaces may not label 1/10 as contextual fraction.'}

def main():
    import sys
    repo=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve();out=audit(repo);print(json.dumps(out,indent=2));(repo/'data/w33_pass1086_contextuality_claim_firewall.json').write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
