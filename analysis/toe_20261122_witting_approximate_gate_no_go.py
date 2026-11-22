"""Exact process-fidelity no-go for low-OSR Witting two-ququart gates.

Independent SymPy certificate derived from the canonical chart circuit in
toe_20261121_relational_reference_pareto.py. The prior repository establishes
that all 45 chart gates are conjugate by S tensor S, preserving the spectrum.

Scope: deterministic bipartite unitaries, arbitrary local gates and at most
k operator-Schmidt-rank <=2 entanglers. Excludes measurements, ancillas,
heralding, CPTP noise and higher-rank entanglers. Bounds are necessary,
not guaranteed to be achievable.
"""
from __future__ import annotations
from pathlib import Path
import json
import sympy as sp

D = 16

def cnot(control, target):
    matrix = sp.zeros(D)
    for column in range(D):
        bits = [(column >> (3-j)) & 1 for j in range(4)]
        if bits[control]:
            bits[target] ^= 1
        row = sum(bits[j] << (3-j) for j in range(4))
        matrix[row, column] = 1
    return matrix

def tensor(*matrices):
    result = sp.eye(1)
    for matrix in matrices:
        result = sp.kronecker_product(result, matrix)
    return result

def canonical_chart_gate():
    eye = sp.eye(2)
    h = sp.Matrix([[1, 1], [1, -1]]) / sp.sqrt(2)
    prep = tensor(eye, h, eye, eye) * cnot(1, 3) * cnot(0, 2)
    phases = []
    for index in range(D):
        b = [(index >> (3-j)) & 1 for j in range(4)]
        phase = -sp.I if b[2] == 0 else sp.Integer(1)
        if b[2] == 0 and b[1] == b[3] == 1:
            phase *= sp.I
        phases.append(phase)
    gate = sp.simplify(prep.H * sp.diag(*phases) * prep)
    assert (gate.H * gate - sp.eye(D)).applyfunc(sp.simplify) == sp.zeros(D)
    return gate

def realign(gate):
    # R(U)[(a,c),(b,d)] = U[(a,b),(c,d)].
    return sp.Matrix(D, D, lambda row, col:
        gate[4*(row//4) + (col//4), 4*(row%4) + (col%4)])

def verify():
    U = canonical_chart_gate()
    R = realign(U)
    gram = sp.simplify(R * R.H)
    x = sp.Symbol("x")
    expected = x**8*(x-sp.Rational(17,2))*(x-sp.Rational(9,2))*(x-sp.Rational(1,2))**6
    assert sp.simplify(gram.charpoly(x).as_expr() - expected) == 0
    assert sp.simplify(sp.trace(gram) - D) == 0
    assert R.rank() == 8
    spectrum = [sp.Rational(17,2), sp.Rational(9,2)] + [sp.Rational(1,2)]*6
    bounds = []
    for k in range(4):
        budget = min(2**k,8)
        S = sum(spectrum[:budget])
        # For V unitary, ||V||_F^2=D and OSR(V)<=budget:
        # |Tr(U†V)|² <= D * sum_{j<=budget} s_j².
        process_ceiling = S / D
        mean_ceiling = (S+1)/(D+1)
        diamond_floor = sp.simplify(2*sp.sqrt(1-process_ceiling))
        frobenius_sq_floor = sp.simplify(2*D - 2*sp.sqrt(D*S))
        bounds.append(dict(k=k, rank_budget=budget,
            process_fidelity_ceiling=str(process_ceiling),
            average_gate_fidelity_ceiling=str(mean_ceiling),
            diamond_distance_floor=str(diamond_floor),
            phase_aligned_Frobenius_squared_floor=str(frobenius_sq_floor)))
    assert [b["average_gate_fidelity_ceiling"] for b in bounds] == [
        "19/34", "14/17", "15/17", "1"]
    assert bounds[2]["diamond_distance_floor"] == "sqrt(2)/2"
    return dict(status="PASS_EXACT_SYMBOLIC", date="2026-11-22",
        canonical_chart_unitary_dimension=16, operator_Schmidt_rank=8,
        squared_Schmidt_spectrum=[str(z) for z in spectrum],
        exact_realign_gram_polynomial=str(sp.factor(expected)), bounds=bounds,
        theorem="For U with realignment singular values s_j and any bipartite unitary V of OSR<=r, |Tr(U†V)|² <= d sum_(j<=r) s_j². Since OSR is submultiplicative and local OSR=1, k rank-two entanglers give r<=2^k. F_avg=(|Tr(U†V)|²/d+1)/(d+1).",
        caveat="45-chart extension relies on previously checked S tensor S local conjugacy. No physical device or TOE claim; not a no-go for ancilla, adaptive, postselected, or noisy channels.")

def main():
    result = verify()
    output = Path(__file__).resolve().parents[1]/"data"/"toe_20261122_witting_approximate_gate_no_go.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n", encoding="utf-8")
    print("PASS exact approximate Witting gate fidelity ceilings:", [x["average_gate_fidelity_ceiling"] for x in result["bounds"]])

if __name__ == "__main__":
    main()
