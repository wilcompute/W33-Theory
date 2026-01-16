Clifford reduction of N12_58 2T cycles inside W33 four-center triad transport (v10)

Inputs:
- cycle_witness_v3_holonomy_solver.csv from the port-law rewrite bundle (v7)

Construction:
- Each step has a port index in {0,1,2} (or -1 for 'stay'), corresponding to one of the three perfect matchings on the K4 component.
- Treat port indices 0,1,2 as Clifford generators e0,e1,e2 with e_i^2 = 1 and e_i e_j = - e_j e_i (i≠j).
- Reduce each cycle’s moved-step port word into a signed blade (sign, mask).

Result:
- Every nontrivial 2T cycle reduces to ±(e0*e1*e2), the Cl(3) pseudoscalar (mask=7).
- This is a strong “outside-the-box” structural statement: the transport loops generate a complex unit internally.

Files:
- cycle_clifford_summary.csv : per-cycle reduced Clifford element + phase products
- cycle_step_ports_and_phases.csv : per-step ports and ray-holonomy phases
- summary.json : short narrative summary
