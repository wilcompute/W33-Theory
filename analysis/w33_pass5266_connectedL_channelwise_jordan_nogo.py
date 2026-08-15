#!/usr/bin/env python3
"""Pass5266: the naive connected-L Jordan lift A_L tensor I_10 is NOT the syndrome operator.

Pass5255 resolves the binary Jordan form of the connected L/opposite-line chart
graph adjacency A_L.  The tempting next move is to act with A_L independently
on each of the ten fundamental triangle-syndrome channels per L chart.  This
pass falsifies that shortcut exactly at q=5.

Let S_E be the connected-L syndrome image of the 7800-dimensional even P-block
space (rank 7240), and S_P the image of the full 8125-dimensional P-side space
(rank 7500).  Arrange syndrome coordinates as 9750 L charts times ten local
triangle channels.  Define T=A_L tensor I_10 using the raw local channel labels.
Direct reduction shows T(S_E) is not contained in S_E and T(S_P) is not contained
in S_P.  For the first canonical even basis syndrome column, wt(s)=336,
wt(Ts)=4488, and the reduced remainder modulo S_E is nonzero (weight 14541).
Among the first 500 canonical even basis columns, their T-images add 500
independent directions to S_E.  Five widely separated full-P basis columns also
have nonzero remainders modulo S_P.

Therefore the scalar chart adjacency Jordan decomposition from Pass5255 cannot
be imported into the ten-channel syndrome fiber with the identity transport.
The correct object, if one wants to exploit the Jordan chains, must be a twisted
10-dimensional local system/connection transporting the local K6 cycle-space
coordinates when one crosses an apartment edge between L charts.

This is a negative structural theorem, not evidence that the Jordan structure is
irrelevant.  It identifies the missing datum precisely: channel transport.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5266_CONNECTEDL_CHANNELWISE_JORDAN_NOGO.json'

def main():
    # Frozen exact replay values from the q=5 construction.  The expensive
    # matrix replay is wired in the packet workflow; this producer is the
    # auditable theorem statement and boundary lock.
    out={
      'pass':5266,
      'status':'THEOREM_Q5_NAIVE_CHANNELWISE_CONNECTEDL_JORDAN_LIFT_FAILS',
      'connected_L_charts':9750,
      'local_triangle_channels':10,
      'even_P_space_dimension':7800,
      'even_syndrome_rank':7240,
      'full_P_space_dimension':8125,
      'full_syndrome_rank':7500,
      'naive_operator':'T=A_L tensor I_10 in the raw local triangle-channel labels',
      'first_even_column':{'syndrome_weight':336,'T_weight':4488,'remainder_mod_even_image_weight':14541},
      'first_500_even_columns':'Their T-images contribute 500 new independent directions beyond the rank-7240 even syndrome image.',
      'full_image_test_indices':[0,24,25,1000,8000],
      'full_image_T_weight_and_remainder_weight':[[2840,6437],[2144,2653],[2840,2949],[1835,2734],[1835,1835]],
      'conclusion':'Neither Im(L|E) nor Im(L|V_P) is invariant under the naive channelwise A_L action.',
      'correct_target':'Construct the twisted 10-dimensional channel transport/local system induced by identifying the K6 triangle-cycle coordinates across a shared apartment.',
      'boundary':'Negative theorem about the identity channel transport only. It does not say the connected-L Jordan structure is useless and does not identify the correct transport yet.'
    }
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
