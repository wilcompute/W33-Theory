from __future__ import annotations
import importlib.util
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/"analysis/w33_physical_fi_alt5_prime_shadow_torsor.py"

def load():
    spec=importlib.util.spec_from_file_location("fi_prime_shadow",SRC)
    assert spec and spec.loader
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod

def test_physical_fi_alt5_prime_shadow_torsor():
    out=load().main(False)
    assert out["status"]=="PASS_PHYSICAL_FI_ALT5_PRIME_SHADOW_TORSOR"
    assert out["integral_orbit"]["S5_orbit_size"]==60
    assert out["integral_orbit"]["Alt5_stabilizer_order"]==1
    assert out["distinct_value_discriminant"]["collision_primes"]==[2,3,5,11]
    assert [out["prime_shadows"][str(p)]["orbit_size"] for p in (2,3,5,11)]==[5,10,30,20]
    assert [out["prime_shadows"][str(p)]["integral_orbit_fiber_size"] for p in (2,3,5,11)]==[12,6,2,3]
    assert out["mod3_selector"]["residue"]==[1,0,1,1,0]
    assert len(out["mod3_selector"]["selected_three"])==3
    assert len(out["mod3_selector"]["complementary_two"])==2
