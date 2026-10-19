# Pass 12089: spin-statistics from Kramers squared

Claude track. Builds on 12077, 12081 and 12085.

## Results

Adjoin a split involution sigma (Kramers squared, 12085) to the E6 Klein clock vacuum. Checked on two Klein planes:

- For exactly **27 of the 135** splits the result is **so(10)**. The other 108 give a5 + a1.
- In every one of the 27 cases, sigma is **odd on all 128 spinor-weight roots** (the 16s) and **even on all 60
  vector-weight roots** (the 10s) and on the 12 singlet roots.

## Reading

With fermion parity taken to be Kramers squared, the SO(10) reached from the E6 clock vacuum has the right
spin-statistics: matter in the 16 is fermionic, and the Higgs (10) and gauge sectors are bosonic.

## Prior art

Once the so(10) lies inside sigma's so(16), the parity pattern follows from the classical branching
E8 > SO(16) > SO(10) x SO(6), with 128 = (16,4) + (16bar,4bar). What is new is that the clock vacuum plus Kramers^2
lands there, for exactly 27 splits.

Producer: `analysis/w33_pass12089_fermion_parity_makes_the_16_fermionic.py`.
