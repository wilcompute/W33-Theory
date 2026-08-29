#!/usr/bin/env python3
"""Repair the subgroup rank-witness audit with independent deterministic coefficients.

The v2 audit used a linear-congruential stream.  Because each cross-orbit is
filled by one successive stream value, that recurrence itself imposed severe
low-rank structure (even the trivial subgroup only reached rank 3).  This
wrapper keeps the exact group/orbital construction and S5 character ceiling,
but replaces the specialization by SHA-256-derived nonzero field elements.
Any observed rank 40 is an explicit exact witness and therefore proves the
rectangular maximum 40 for that subgroup.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

import w33_20260829_pg34_subgroup_zero_split as base

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_20260829_PG34_SUBGROUP_ZERO_SPLIT_V3.json'


def sha_coeff(seed:int, orbit:int)->int:
    h=hashlib.sha256(f'w33-subgroup-v3:{seed}:{orbit}'.encode()).digest()
    return 1+(int.from_bytes(h,'big')%(base.P-1))


def witness_rank(idx,norb,seed):
    coeff=[sha_coeff(seed,k) for k in range(norb)]
    M=[[coeff[idx[(i,j)]] for j in range(45)] for i in range(40)]
    return base.rank_mod(M)


def main():
    # Monkey-patch only the specialization; all geometry, subgroup generation,
    # orbit construction, character decomposition, and exact rank arithmetic
    # remain the v2 implementation.
    base.witness_rank=witness_rank
    base.OUT=OUT
    base.main()
    d=json.loads(OUT.read_text())
    d['schema']='w33.20260829.pg34-subgroup-zero-split.v3'
    d['witnessMethod']='orbit coefficients are SHA-256(seed,orbit) reduced to nonzero elements of F_1000003'
    d['repair']='v2 LCG coefficients were algebraically correlated and produced rank 3 even for the trivial subgroup; v3 removes that artifact.'
    d['chainCompact']=[{k:r[k] for k in ('subgroup','order','crossPairOrbits','rankWitness','witnessSeed','provenMaximumRank','minimumChiralZeroModes')} for r in d['chain']]
    full=[r for r in d['chain'] if r['provenMaximumRank']==40]
    d['firstFullRankSubgroup']=full[0]['subgroup'] if full else None
    # Sanity control: with no symmetry, the orbital space is the full 40x45
    # matrix space, so failure to exhibit rank 40 means the specialization is
    # still defective and must not be promoted.
    assert d['chain'][-1]['subgroup']=='1' and d['chain'][-1]['rankWitness']==40
    d['theorem']=('PSp(4,3) has exact maximum equivariant rank 25 and S5 has exact maximum 30. '
                  'Every subgroup in the chain for which v3 exhibits rank 40 has exact maximum rank 40 and leaves only the five rectangular-index zero modes.')
    OUT.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','schema':d['schema'],'chain':d['chainCompact'],'firstFullRankSubgroup':d['firstFullRankSubgroup']},sort_keys=True))

if __name__=='__main__': main()
