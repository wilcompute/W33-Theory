# Pass 1146 Parallel-Track Audit

## Draft PR #162

The reusable exact content is valid and has been imported under the collision-free Pass 1135/1142-1143 line:

- complete 2240 A2-triple carrier;
- exact W(E6) class-algebra character table;
- 45-support cubic incidence;
- nine-term firewall boundary correctly treated as a selected restriction rather than a W(E6)-submodule.

The new computations extend that work:

- each 432 orbit has the same rank-26 noncommutative S5 Hecke algebra;
- every inter-orbit Hom space has dimension 26;
- `Lambda^2(Aug26)` contains one `81_minus`;
- an explicit rank-81 intertwiner has been constructed;
- the A2 Coxeter element centralizing W(E6) cycles the three 432 carriers.

## PR #160 defect-locus branch

The proposed numerical verifier is not admissible evidence.

1. It calls the target a 40-ray qutrit SIC, but a SIC in complex dimension 3 has `d^2=9` rays. The Witting/Penrose configuration has 40 rays in complex dimension 4 (`CP(3)`), not a qutrit SIC.
2. The script generates nine Heisenberg displacements and Fourier iterates of a qutrit vector, then treats deduplicated output as the Witting configuration without an exact equivalence proof.
3. Its map from those rays to `F_3^4` labels is explicitly described as approximate.
4. Its second script falls back to arbitrary indices `[0,1,2,3]`.
5. A four-point totally isotropic line in `W(3,3)` is not a Fano subplane; a projective line over `F_3` has four points, whereas a Fano plane has seven.

Accordingly, the claimed four-ray defect locus and `CF=1/10` are not imported. The exact replacement is the A2 color torsor: the three 432 orbits are distinguished by their common positive/negative 27-shell color and are cyclically permuted by the order-three A2 Coxeter element.
