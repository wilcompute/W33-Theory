# Toroidal Metric Parity-Sector Split

## Executive result

The parity-Taylor histogram is

\[
c_1,c_2,c_3,c_4,c_5,c_6=12,48,0,4,1,3.
\]

Split it by odd and even multiplicity.

Odd multiplicities:

\[
c_1+c_3+c_5=12+0+1=13.
\]

Even multiplicities:

\[
c_2+c_4+c_6=48+4+3=55.
\]

So:

\[
\boxed{\text{odd metric classes}=13=\Phi_3.}
\]

\[
\boxed{\text{even metric classes}=55=5\cdot11.}
\]

Their difference is

\[
55-13=42.
\]

But \(42\) is exactly one toroidal chart's flag count:

\[
42=v+e+f=2e.
\]

Therefore:

\[
\boxed{\text{even}-\text{odd}=42=\text{one toroidal realization flag count}.}
\]

## Boolean lift split

The Boolean lift is

\[
\sum_m c_m2^m=504=7\cdot72.
\]

The odd/even split is:

\[
\text{odd Boolean lift}=56=7\cdot8,
\]

\[
\text{even Boolean lift}=448=7\cdot64.
\]

So per realization:

\[
56/7=8,
\]

\[
448/7=64.
\]

Thus the middle eigenvalue decomposes as

\[
\boxed{72=8+64.}
\]

Since

\[
8=1+\Phi_6,
\]

this is

\[
\boxed{72=8(1+8).}
\]

So the middle eigenvalue is the sum of a tomotope-cell packet and its square.

## Edge-instance split

Odd edge instances:

\[
1\cdot12+3\cdot0+5\cdot1=17.
\]

Even edge instances:

\[
2\cdot48+4\cdot4+6\cdot3=130.
\]

So

\[
17+130=147.
\]

And

\[
130=10\cdot13=\Phi_4\Phi_3.
\]

Thus:

\[
\boxed{\text{even edge instances}=\Phi_4\Phi_3.}
\]

The odd sector leaves a prime residue:

\[
\boxed{17.}
\]

This is interesting because the previous cyclotomic norm found

\[
N_{\Phi_3}(P)=11^2\cdot21.
\]

Now the parity split exposes both

\[
11
\]

and

\[
17
\]

inside the metric packet.

## Kernel split

The phase-kernel contribution is

\[
\sum_m(m-1)c_m=79.
\]

Odd sector:

\[
(1-1)12+(3-1)0+(5-1)1=4.
\]

Even sector:

\[
(2-1)48+(4-1)4+(6-1)3=75.
\]

So

\[
4+75=79.
\]

The odd kernel contribution is exactly

\[
\boxed{4=d_Z=q+1.}
\]

The even sector carries the remaining

\[
75=3\cdot25.
\]

## Raw second moment split

The raw second moment was

\[
\sum_m m^2c_m=401=320+81.
\]

The parity split is:

\[
\text{odd raw second}=37,
\]

\[
\text{even raw second}=364=28\cdot13.
\]

So the even quadratic sector is again controlled by \(\Phi_3=13\):

\[
\boxed{364=28\Phi_3.}
\]

## The theorem

**Toroidal Metric Parity-Sector Theorem.** The parity-Taylor histogram

\[
c_m=(12,48,0,4,1,3)
\]

splits into odd and even metric sectors with

\[
\boxed{13=\Phi_3}
\]

odd classes and

\[
\boxed{55=5\cdot11}
\]

even classes.  Their difference is

\[
\boxed{42,}
\]

exactly one toroidal chart flag count.  The Boolean lift splits as

\[
56+448=7\cdot8+7\cdot64=7(8+64),
\]

so the middle eigenvalue decomposes per realization as

\[
\boxed{72=8+64.}
\]

Odd edge instances give \(17\), while even edge instances give

\[
130=\Phi_4\Phi_3.
\]

The odd kernel excess is

\[
4=d_Z,
\]

leaving \(75\) in the even sector for the full kernel \(79\).

## Why this matters

The metric edge data now has a parity-sector architecture:

\[
\boxed{\text{odd classes}=\Phi_3}
\]

\[
\boxed{\text{even classes}=5p_{\mathrm{Ih}}}
\]

\[
\boxed{\text{even}-\text{odd}=42\text{ flags}}
\]

\[
\boxed{72=8+64}
\]

\[
\boxed{79=4+75}
\]

So the metric packet simultaneously exposes \(13\), \(11\), \(17\), \(42\), \(72\), and \(79\), all from one parity split of the Taylor ladder.

## Honesty boundary

This is an exact finite parity-sector identity for the toroidal metric edge packet. It does not by itself infer physical dynamics, continuum geometry, or empirical observables.
