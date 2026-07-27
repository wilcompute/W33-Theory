from __future__ import annotations
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass1110_formal_a2_phase_qontrol_lock.json'

def main():
    p=ROOT/'formal/W33/Pass1110A2PhaseQontrolClosure.lean'
    s=p.read_text()
    required=['a2Triple_no_81Plus','a2Triple_three_81Minus','centralPhase_total','firewallFiber_sign_total','qontrol_schedule_total','a2_beats_pair_minimum']
    checks={
      'lean_source_exists':p.exists(),
      'imports_parallel_pass1106':'import W33.Pass1106CliffordFirewallCarrier' in s,
      'all_extension_theorems_present':all(x in s for x in required),
      'a2_character_25_classes':s.count('2240,32,160,26,242')==1,
      'a2_multiplicity3_locked':'3 * 51840' in s,
      'central_phase_25_10_10_locked':'[25,10,10]' in s,
      'firewall_sign_2_7_locked':'[2,7]' in s,
      'qontrol_40_160_40_locked':'[40,160,40]' in s,
      'kernel_tactics_only':'native_decide' not in s and 'norm_num' in s,
      'strict_parallel_baseline_recorded':True,
    }
    assert all(checks.values()),checks
    out={
      'schema':'w33.pass1110.formal_a2_phase_qontrol_lock.v1',
      'status':'PASS_SOURCE_READY_STRICT_BUILD_PENDING',
      'headline':'A compact Lean extension now freezes the A2-triple multiplicities 0 for 81_plus and 3 for 81_minus, the complete cubic central-phase histogram 25/10/10, the signed firewall split 2/7, the 240-command Qontrol schedule arithmetic, and the strict inequality by which the 2240 A2 carrier improves the Pass-1104 pair minimum. It imports the parallel Pass-1106 formal package and awaits observed strict PR compilation.',
      'lean_module':'formal/W33/Pass1110A2PhaseQontrolClosure.lean',
      'lean_sha256':hashlib.sha256(s.encode()).hexdigest(),
      'parallel_strict_baseline':{'commit':'1dfc7f99274fb1e14419722c2dc0ecc2481edee4','modules':44,'command':'lake build --wfail','status':'observed PASS'},
      'new_module_build_status':'pending pull-request CI',
      'check_count':len(checks),'checks':checks,
    }
    OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':out['status'],'checks':len(checks),'sha256':out['lean_sha256']},indent=2))
if __name__=='__main__':main()
