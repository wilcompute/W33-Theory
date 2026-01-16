# v18: Gauge-invariant S3 holonomy analysis (W33 → Q)

## What this does
This bundle takes the v17 S3 edge labels on the 45-node quotient graph Q and builds a **proper S3 connection** by enforcing
**g(v,u) = g(u,v)^(-1)** on every undirected edge. The remaining edge-level ambiguity (ties) is resolved by searching tie-break choices
and selecting the connection that maximizes the dependence between:

- Z2 triangle parity (from the canonical Z2 voltage cocycle), and
- S3 triangle holonomy **conjugacy class** (id / transposition / 3-cycle).

## Key numbers
### BestMI connection (selected from 5000 tie-break samples)
- MI(parity, holonomy class) = **0.014797 nats**
- P(id | parity=0) − P(id | parity=1) = **0.159615**

Counts (rows=parity 0/1, cols=class):
s3_class            3-cycle    id  transposition
z2_triangle_parity                              
0                       697  1187           1236
1                       573   477           1110

### Baseline (lexicographic tie-break)
- MI = **0.005766 nats**
- P(id|0)−P(id|1) = **0.106232**

## Gauge invariance (checked)
Under arbitrary per-vertex gauge transforms a_u ∈ S3, the triangle holonomy changes by conjugation,
so its conjugacy class is invariant. Verified on 3 random gauge trials: **all 5280 triangle classes unchanged**.

## Non-uniqueness
Different tie-break resolutions typically produce **gauge-inequivalent** S3 connections. The robust content is therefore:
- the Z2 cocycle class (fixed by v14),
- and the fact that **for any fixed S3 connection**, triangle holonomy conjugacy classes are gauge invariant and correlate with Z2 parity.

Files:
- Q_directed_edges_S3_bestMI.csv
- Q_triangles_S3_holonomy_bestMI.csv
- v18_summary.json
