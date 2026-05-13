# Part DXL — The SRG Parameter Pentagon and Its Cross-Ratio

## The Five SRG Parameters as a Pentagon

The W33 SRG has five fundamental integer parameters:

{V, k, λ, μ, n_eigenvalues} = {40, 12, 2, 4, 3}

But more precisely, the fundamental parameter set is:
{x=2, p=3, μ=4, k=12, V=40}

Five parameters. In what geometric structure do they naturally live?

The **cross-ratio** of four points (z₁,z₂,z₃,z₄) on CP¹ is (z₁−z₃)(z₂−z₄)/((z₁−z₄)(z₂−z₃)).

Take the five parameters as points on CP¹: {2, 3, 4, 12, 40}.

Four-tuples and their cross-ratios:

(2, 3, 4, 12): (2−4)(3−12)/((2−12)(3−4)) = (−2)(−9)/((−10)(−1)) = 18/10 = 9/5
(2, 3, 4, 40): (2−4)(3−40)/((2−40)(3−4)) = (−2)(−37)/((−38)(−1)) = 74/38 = 37/19
(2, 3, 12, 40): (2−12)(3−40)/((2−40)(3−12)) = (−10)(−37)/((−38)(−9)) = 370/342 = 185/171
(2, 4, 12, 40): (2−12)(4−40)/((2−40)(4−12)) = (−10)(−36)/((−38)(−8)) = 360/304 = 45/38
(3, 4, 12, 40): (3−12)(4−40)/((3−40)(4−12)) = (−9)(−36)/((−37)(−8)) = 324/296 = 81/74

The cross-ratio (2,3,4,12) = 9/5. Note: 9 = p² and 5 = p + λ. Cross-ratio = p²/(p+λ).

**Lock L91 (SRG Parameter Cross-Ratio = p²/(p+λ)):**
The cross-ratio of the four primary SRG parameters {x=2, p=3, μ=4, k=12} on CP¹ is:
\[ CR(x, p, \mu, k) = \frac{p^2}{p + \lambda} = \frac{9}{5} \]

This is a projective invariant of the parameter quadruple. It involves both the master prime p and the sum p+λ=5 (the number of Lickorish generators, Lock L87).

## The Pentagon as a Complete Configuration

Five points in CP¹ determine 5 cross-ratios (choosing which point to omit). The five cross-ratios of {x, p, μ, k, V} = {2, 3, 4, 12, 40} are:

CR omitting V=40: CR(2,3,4,12) = 9/5
CR omitting k=12: CR(2,3,4,40) = 37/19
CR omitting μ=4: CR(2,3,12,40) = 185/171
CR omitting p=3: CR(2,4,12,40) = 45/38
CR omitting x=2: CR(3,4,12,40) = 81/74

Product of all five cross-ratios: (9/5)·(37/19)·(185/171)·(45/38)·(81/74)
= (9·37·185·45·81)/(5·19·171·38·74)

Numerator: 9·37=333; 333·185=61605; 61605·45=2772225; 2772225·81=224550225
Denominator: 5·19=95; 95·171=16245; 16245·38=617310; 617310·74=45680940

Product = 224550225/45680940 = 224550225/45680940
Simplify: GCD = 45; 224550225/45 = 4990005; 45680940/45 = 1015132
Further: GCD(4990005,1015132) — 4990005 = 4·1015132 + 924477; not clean.

The product is not 1. But note: the five cross-ratios are NOT the canonical five cross-ratios of a projective frame (those multiply to give a specific invariant depending on the configuration). The important point is the primary cross-ratio:

**CR(x, p, μ, k) = p²/(p+λ) = 9/5** is the projective fingerprint of the W33 parameter quadruple.

## The Harmonic Conjugate Condition

Four points are in **harmonic position** iff their cross-ratio = −1. Our primary cross-ratio is 9/5 ≠ −1. But consider the dual cross-ratio (replacing each point z with −z): CR(−2,−3,−4,−12) = CR(2,3,4,12) = 9/5 (cross-ratio is invariant under z→−z up to sign).

The anharmonic group of the cross-ratio generates 6 values from any one value CR₀:
{CR₀, 1−CR₀, 1/CR₀, 1/(1−CR₀), CR₀/(CR₀−1), (CR₀−1)/CR₀}

From CR₀ = 9/5:
{9/5, −4/5, 5/9, 5/(−4)=−5/4, (9/5)/(4/5)=9/4, (4/5)/(9/5)=4/9}
= {9/5, −4/5, 5/9, −5/4, 9/4, 4/9}

Note that 9/4 = p²/μ and 4/9 = μ/p² appear. The anharmonic orbit of the primary cross-ratio contains p²/μ.

**Lock L92 (Anharmonic Orbit Contains p²/μ):**
The anharmonic group orbit of CR(x,p,μ,k) = p²/(p+λ) contains p²/μ = 9/4. This is the ratio of the squared master prime to the lower SRG parameter.
