from w33.arithmetic import apply_operator_chain, divisor_sum, euler_totient, prime_factorization, radical
from w33.shift_tower import build_shift_tower, shift_tower_primitives


def test_shift_tower_values_q3_to_q7():
    tower = build_shift_tower()
    assert tower[3] == {"v": 40, "k": 12, "lambda": 2, "mu": 4, "Phi3": 13, "Phi4": 10, "Phi6": 7}
    assert tower[4] == {"v": 85, "k": 20, "lambda": 3, "mu": 5, "Phi3": 21, "Phi4": 17, "Phi6": 13}
    assert tower[5] == {"v": 156, "k": 30, "lambda": 4, "mu": 6, "Phi3": 31, "Phi4": 26, "Phi6": 21}
    assert tower[6] == {"v": 259, "k": 42, "lambda": 5, "mu": 7, "Phi3": 43, "Phi4": 37, "Phi6": 31}
    assert tower[7] == {"v": 400, "k": 56, "lambda": 6, "mu": 8, "Phi3": 57, "Phi4": 50, "Phi6": 43}


def test_phi6_shift_identity():
    for q in range(3, 7):
        assert shift_tower_primitives(q + 1)["Phi6"] == shift_tower_primitives(q)["Phi3"]


def test_persistent_commutation_patterns():
    tower = build_shift_tower()

    for q in [3, 5, 6]:
        assert euler_totient(tower[q]["Phi3"]) == tower[q]["k"]

    for q in [4, 6, 7]:
        assert euler_totient(tower[q]["Phi6"]) == tower[q - 1]["k"]

    for q in [3, 4, 6]:
        assert divisor_sum(tower[q]["lambda"]) == tower[q + 1]["lambda"]

    for q in [3, 4, 5, 6]:
        assert radical(tower[q]["Phi3"]) == tower[q + 1]["Phi6"]

    for q in [4, 5, 6, 7]:
        assert radical(tower[q]["Phi6"]) == tower[q - 1]["Phi3"]


def test_operator_composition_families_on_local_window():
    tower = build_shift_tower()

    for q in [3, 5, 7]:
        assert apply_operator_chain(tower[q]["Phi6"], ("phi", "d")) == tower[q]["mu"]

    for q in [3, 4, 5, 6]:
        assert apply_operator_chain(tower[q]["k"], ("cot", "sigma_1", "Omega")) == tower[q]["lambda"]

    for q in [3, 5, 6, 7]:
        assert apply_operator_chain(tower[q]["v"], ("phi", "d", "d")) == tower[q]["lambda"]

    for q in [3, 4, 5]:
        assert apply_operator_chain(tower[q]["k"], ("J2", "Omega")) == tower[q + 2]["mu"]


def test_extended_radical_ladder_and_first_cube_defect():
    for q in range(3, 21):
        phi3 = shift_tower_primitives(q)["Phi3"]
        if q == 18:
            assert phi3 == 343
            assert radical(phi3) == 7
            assert apply_operator_chain(phi3, ("rad", "rad")) == 7
        else:
            assert radical(phi3) == shift_tower_primitives(q + 1)["Phi6"]
            assert apply_operator_chain(phi3, ("rad", "rad")) == phi3

    for q in range(4, 21):
        phi6 = shift_tower_primitives(q)["Phi6"]
        if q == 19:
            assert phi6 == 343
            assert radical(phi6) == 7
            assert apply_operator_chain(phi6, ("rad", "rad")) == 7
        else:
            assert radical(phi6) == shift_tower_primitives(q - 1)["Phi3"]
            assert apply_operator_chain(phi6, ("rad", "rad")) == phi6


def test_repeated_defect_primes_live_on_split_mod_3_class():
    repeated_primes = set()

    for q in range(3, 201):
        packet = shift_tower_primitives(q)
        for name in ("Phi3", "Phi6"):
            for p, exponent in prime_factorization(packet[name]).items():
                if exponent > 1:
                    repeated_primes.add(p)

    assert repeated_primes
    assert all(p % 3 == 1 for p in repeated_primes)