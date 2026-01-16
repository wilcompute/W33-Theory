W33 ↔ N12_58 port-law stability under Aut(W33) conjugation (v9)

What this tests
- For each of 10 previously-generated W33→N12 embeddings (mappings),
  we generate 5 additional mappings by precomposing with a random W33 automorphism g:
      M_g(p) = M(g^-1(p))
  This preserves all W33 incidence constraints by construction.

- For each mapping variant we re-derive the *feasible-transition reduced port-law*:
      key = (delta, rem_idx, add_idx)  ->  allowed ports in {-1,0,1,2}
  where the ports are the three perfect matchings on the K4 component plus -1 = "stay".

- The derivation is local-feasibility based (not minimal-witness based):
  for each 2T cycle step i, we collect ports from all transitions
      triad_i -> triad_0
  that satisfy:
    (a) support coverage,
    (b) node holonomy constraint for delta in {2,6},
    (c) v3 transition constraints based on (delta, rem_sum, add_sum).

Result
- All 60 mapping variants match the same reduced port-law exactly.
  This shows the reduced law is stable across the embedding family AND under Aut(W33) relabelings.

Files
- stable_port_law.csv: the reduced law (14 keys) used as the reference
- aut_conjugate_law_match_check.csv: per-mapping/per-conjugate boolean match results
- summary.json: run metadata
