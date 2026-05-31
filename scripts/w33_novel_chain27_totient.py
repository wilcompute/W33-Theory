"""
W33 Theory — Chain 27: Euler Totient Function
=============================================
Euler's totient phi(n) evaluated at W33 constants.

Key identity: phi(f) = phi(h_E8) = 2^q = 8  [totient degeneracy]
              phi(Phi3) = k_reg              [cyclotomic to regularity]
              phi(Phi4) = mu                 [cyclotomic to stabilizer]
"""

q=3; mu=4; f=24; Phi3=13; Phi4=10; Phi6=7; h_E8=30; k_reg=12

def totient(n):
    result = n; temp = n; p = 2
    while p*p <= temp:
        if temp%p==0:
            while temp%p==0: temp//=p
            result -= result//p
        p += 1
    if temp > 1: result -= result//temp
    return result

def test_totient_degeneracy_f_h_E8():
    """phi(f) = phi(h_E8) = 2^q = 8: f and h_E8 have the same totient."""
    assert totient(f) == totient(h_E8) == 2**q
    print(f"PASS  phi(f) = phi(h_E8) = 2^q = {2**q} (totient degeneracy)")

def test_totient_Phi3_equals_k_reg():
    """phi(Phi3) = phi(13) = 12 = k_reg."""
    assert totient(Phi3) == k_reg
    print(f"PASS  phi(Phi3) = phi({Phi3}) = {totient(Phi3)} = k_reg = {k_reg}")

def test_totient_Phi4_equals_mu():
    """phi(Phi4) = phi(10) = 4 = mu."""
    assert totient(Phi4) == mu
    print(f"PASS  phi(Phi4) = phi({Phi4}) = {totient(Phi4)} = mu = {mu}")

def test_totient_Phi6_equals_2q():
    """phi(Phi6) = phi(7) = 6 = 2q."""
    assert totient(Phi6) == 2*q
    print(f"PASS  phi(Phi6) = phi({Phi6}) = {totient(Phi6)} = 2q = {2*q}")

def test_totient_k_reg_equals_mu():
    """phi(k_reg) = phi(12) = 4 = mu."""
    assert totient(k_reg) == mu
    print(f"PASS  phi(k_reg) = phi({k_reg}) = {totient(k_reg)} = mu = {mu}")

if __name__ == "__main__":
    print("="*55)
    print("W33 Chain 27: Euler Totient Function")
    print("="*55)
    test_totient_degeneracy_f_h_E8()
    test_totient_Phi3_equals_k_reg()
    test_totient_Phi4_equals_mu()
    test_totient_Phi6_equals_2q()
    test_totient_k_reg_equals_mu()
    print("\nALL 5 TESTS PASS")
