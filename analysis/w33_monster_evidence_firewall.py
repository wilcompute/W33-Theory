"""Passes 3584-3590: exact Monster/W33 evidence firewall."""
from __future__ import annotations
from dataclasses import asdict,dataclass
import json
from pathlib import Path
MONSTER_ORDER=808017424794512875886459904961710757005754368000000000
PSP43_ORDER=25920; WE6_ORDER=51840; K=12; LAM=2; MU=4; EDGES=240
@dataclass(frozen=True)
class Claim:
    name:str; value:bool; level:str; interpretation:str
claims=[
 Claim('PSp(4,3) order',PSP43_ORDER==2**6*3**4*5,'A','exact order'),
 Claim('W(E6) order',WE6_ORDER==2*PSP43_ORDER,'A','exact extension scale'),
 Claim('Monster divisibility',MONSTER_ORDER%PSP43_ORDER==0,'A','necessary, not sufficient, for embedding'),
 Claim('minimal degree factorization',196883==47*59*71,'A','exact factorization'),
 Claim('first moonshine coefficient',196884==196883+1,'A','trivial plus minimal degree'),
 Claim('Leech correction',196884==196560+18**2,'A','exact identity, not lattice map'),
 Claim('j constant',744==3*248,'A','exact identity only'),
 Claim('elliptic point',1728==K**3,'A','exact identity only'),
 Claim('central charge arithmetic',24==K*LAM,'A','match, not derivation'),
 Claim('E8 edge correction',248==EDGES+2*MU,'A','exact identity only')]
assert all(c.value for c in claims)
firewall={
 'documented_external_facts':[
  'PSp(4,3) is isomorphic to U4(2).',
  'The Monster has documented 5B-type U4(2) subgroups.',
  'For that embedding type, involutions fuse to 2B, order-3 classes to 3B, and order-5 to 5B.',
  'The perfect double cover 2.U4(2) does not embed in the Monster.',
  'The Monster has a degree-196883 irreducible character and a degree-196884 Griess/Moonshine space.'],
 'not_proved_here':['canonical concrete mmgroup embedding','unique class fusion','degree-81 constituent in a specified restriction','Griess/VOA/Majorana multiplication from W33 incidence','physical mechanism from arithmetic identities'],
 'promotion_rule':'No A-level identity may be described as a mechanism until an explicit C-level map is supplied and checked.'}
result={'verified':True,'claims':[asdict(c) for c in claims],'quotients':{'monster_over_psp43':MONSTER_ORDER//PSP43_ORDER,'monster_over_we6':MONSTER_ORDER//WE6_ORDER},'firewall':firewall}
if __name__=='__main__':
 out=Path('data/PART_3584_3590_MONSTER_EVIDENCE_FIREWALL_results.json'); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(result,indent=2)+'\n'); print(json.dumps(result,indent=2))
