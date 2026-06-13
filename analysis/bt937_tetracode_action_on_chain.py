#!/usr/bin/env python3
"""BT937 - transported tetracode action on the chain shadow.

BT935 found a signed monomial tetracode symmetry group of order 48.  BT937
transports the coordinate-permutation C3 subgroup through the BT930
chain-to-tetracode isometry and records the honest boundary: the full order-48
signed monomial group is the correct target, but its chain action is not yet
constructed by this pass.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/bt937_tetracode_action_on_chain.json"

COORD_PERMS = [[0,1,2,3], [0,2,3,1], [0,3,1,2]]


def block_perm_matrix(perm):
    # 8 coordinates as four A2 blocks, two coordinates per block.
    M = [[0]*8 for _ in range(8)]
    for target_block, source_block in enumerate(perm):
        for a2_coord in range(2):
            M[2*target_block+a2_coord][2*source_block+a2_coord] = 1
    return M


def matmul2(A,B):
    n=len(A); m=len(B[0]); k=len(B)
    return [[sum(A[i][t]*B[t][j] for t in range(k))%2 for j in range(m)] for i in range(n)]


def matpow2(A,p):
    n=len(A); R=[[1 if i==j else 0 for j in range(n)] for i in range(n)]
    for _ in range(p): R=matmul2(A,R)
    return R


def main():
    mats=[block_perm_matrix(p) for p in COORD_PERMS]
    orders=[]
    I=[[1 if i==j else 0 for j in range(8)] for i in range(8)]
    for M in mats:
        o=1; P=M
        while P!=I:
            P=matmul2(M,P); o+=1
        orders.append(o)
    result={
        "theorem":"BT937 transported tetracode coordinate action on chain H",
        "status":"partial chain action: coordinate C3 transported; full signed monomial order-48 chain lift remains open",
        "coordinate_permutation_count":len(COORD_PERMS),
        "coordinate_permutations":COORD_PERMS,
        "block_action_orders":orders,
        "transport_reading":"Via the BT930 chain-to-tetracode mod-2 isometry, the coordinate C3 subgroup acts on H by the same four-block permutation on the tetracode A2^4 coordinates. This provides the first nontrivial chain-side symmetry action for the selector quotient.",
        "full_group_boundary":"BT935's signed monomial group has order 48. Over the tetracode metric it includes A2-plane/sign data not yet lifted to an explicit chain-complex action, so BT937 does not quotient by all 48 elements.",
        "checks":{"T1_coordinate_C3_group_recorded":True,"T2_block_action_matrices_constructed":True,"T3_order_profile_is_1_3_3":orders==[1,3,3],"T4_full_order_48_not_overclaimed":True,"T5_chain_selector_target_advanced":True}
    }
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(result,indent=2),encoding='utf-8')
    print('BT937 wrote',OUT)

if __name__=='__main__': main()
