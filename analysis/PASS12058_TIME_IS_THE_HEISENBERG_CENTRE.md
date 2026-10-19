# Pass 12058: time is the central charge of space translations

* **Producer:** `analysis/w33_pass12058_time_is_the_heisenberg_centre.py` (4/4 checks)
* **Certificate:** `data/w33_pass12058_time_is_the_heisenberg_centre.json`
* **Regression:** `tests/test_w33_pass12058.py`
* **Track:** Claude. Reservation `f6ace095e`.
* **Continues:** 12052-12053.
* **Paper:** Theorem 7.4.

## Results (exact)

H is the stabiliser of the clock real form at p, of order 432.

1. **U is a Heisenberg group with the tick as its centre.** U, the set of elements of 3-power order, has 27 elements. It
   is normal, of exponent 3 and nonabelian, with **Z(U) = [U,U] = <t_p>**, the tick.
2. **Translations commute only up to a tick.** For all 27 x 27 pairs, [T_u, T_v] = t_p^(c omega(u,v)), where omega is
   the symplectic area on U/Z = F_3^2. So two space translations commute only up to a tick.
3. **The quotients.**
   * H/U = 2 x Q8, with element orders 1:1, 2:3, 4:12.
   * H/Z(H) = 3^2:Q8, with element orders 1:1, 2:9, 3:8, 4:54.
   * Choosing one of the three tick lines at p breaks SL(2,3) (the binary tetrahedral group) to Q8.
4. **Orbits on the 40 points: 1 + 12 + 27.** U is **regular** on the 27 far points, so they form a Heisenberg torsor:
   two space coordinates and one time coordinate. On the 12 neighbours, U has orbits of size 3, one along each line.

## Reading

**A finite Galilei group with spin.** The one-time real form's symmetry group is a finite, spinful analogue of the
centrally extended (Bargmann) Galilei group. Its central charge is **time**, the tick that chose the real form, where
Bargmann's is mass.

**Space, time and spin.**
* **Space translations:** the Heisenberg group.
* **Time:** its commutator.
* **Spin:** the quaternion group.
* **Spacetime of the event p:** the 27 events not collinear with p.

**Status.** This is an interpretation, not a derivation of continuum kinematics.

## Prior art

**Classical, and cited:**
* W(q) is an elation generalized quadrangle. Its Heisenberg elation group about a base point acts regularly on the q^3
  non-collinear points, with centre the symmetries about the point (Payne-Thas, *Finite Generalized Quadrangles*, ch. 8;
  Kantor).
* The point stabiliser of Sp(4,q) is the Jacobi group.

**New:**
* the elation centre *is* the tick that fixes the clock real form (12052-12053);
* the real form's symmetry group is that elation group extended by +-1 x Q8;
* the tick-line choice breaks SL(2,3) to Q8.

**The parallel track.** The 2026-10-19 all-five note sets a firewall: a projector minimum does not by itself derive a
physical arrow of time. That holds here too; this pass is structure, not an arrow.
