"""Intake11663: the actual time-odd invariant defeats the proposed radial action."""
import sys
from fractions import Fraction
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'analysis'))
import w33_pass11649_maximal_arrow_state as P


def test_actual_arrow_has_degree_twelve():
    h=P.h6(P.STAR)
    assert np.isclose(h*h,float(Fraction(1,1289945088)),rtol=1e-12,atol=1e-20)
    for radius in [.5,2,10]:
        assert np.isclose(P.h6(radius*P.STAR),radius**12*h,rtol=1e-10,atol=1e-20)


def test_proposed_radial_action_runs_away():
    # Directly evaluate the imported invariant; do not normalize the field.
    leading=-P.h6(P.STAR)**2
    values=[]
    for radius in [10.,100.,1000.]:
        energy=(radius**2-1)**2-P.h6(radius*P.STAR)**2
        values.append(energy)
        assert energy<0
        assert np.isclose(energy/radius**24,leading,rtol=1e-10,atol=1e-20)
    assert values[2]<values[1]<values[0]
