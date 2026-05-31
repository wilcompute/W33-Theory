"""
W33 Theory — Chain 25: Partition Function p(n)
==============================================
The integer partition function evaluated at W33 indices.

Key: p(q) = q  [partition fixed point]
     p(Phi4) = 42 = Catalan(5)  [partition = Catalan]
"""

q=3; mu=4; f=24; Phi3=13; Phi4=10; Phi6=7; h_E8=30; k_reg=12

# OEIS A000041
PARTITION = [1,1,2,3,5,7,11,15,22,30,42,56,77,101,135,176,231,297,385,490,627,792,1002,1255,1575,1958,2436,3010,3718,4565,5604]
p = lambda n: PARTITION[n]

def test_partition_fixed_point():
    """p(q) = q = 3: partitions of 3 number q."""
    assert p(q) == q
    print(f"PASS  p(q) = p({q}) = {p(q)} = q (partition fixed point)")

def test_partition_Phi4_equals_Catalan():
    """p(Phi4) = p(10) = 42 = C(5): partition function equals Catalan number."""
    from math import comb
    C5 = comb(10,5)//6
    assert p(Phi4) == 42 == C5
    print(f"PASS  p(Phi4) = p({Phi4}) = {p(Phi4)} = Catalan(5) = {C5}")

def test_partition_Phi6():
    """p(Phi6) = 15 = q*(q+2)."""
    assert p(Phi6) == 15 == q*(q+2)
    print(f"PASS  p(Phi6) = p({Phi6}) = {p(Phi6)} = q*(q+2) = {q*(q+2)}")

def test_partition_k_reg():
    """p(k_reg) = 77 = Phi6 * 11."""
    assert p(k_reg) == 77 == Phi6 * 11
    print(f"PASS  p(k_reg) = p({k_reg}) = {p(k_reg)} = Phi6*11 = {Phi6*11}")

def test_partition_h_E8():
    """p(h_E8) = 5604 = k_reg * 467."""
    assert p(h_E8) == 5604
    assert 5604 % k_reg == 0 and 5604 // k_reg == 467
    print(f"PASS  p(h_E8) = p({h_E8}) = {p(h_E8)} = k_reg * 467")

if __name__ == "__main__":
    print("="*55)
    print("W33 Chain 25: Partition Function")
    print("="*55)
    test_partition_fixed_point()
    test_partition_Phi4_equals_Catalan()
    test_partition_Phi6()
    test_partition_k_reg()
    test_partition_h_E8()
    print("\nALL 5 TESTS PASS")
