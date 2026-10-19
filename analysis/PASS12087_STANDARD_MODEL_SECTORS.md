# Pass 12087: the Standard-Model content of the 16-clock gradings

Claude track. Builds on 12081.

## Setup

Take a flag-built Standard-Model subspace (16 clocks, 15 splits). Hypercharge comes from the flag's su(5), normalised so
that the X/Y bosons carry Y = +-5/6.

## Results

| Sector | Count | Content |
|---|---|---|
| gauge | 1 | su(3)+su(2) roots |
| X/Y | 1 | X/Y bosons, Y = +-5/6 |
| Q | 5 | (3,2)_{1/6} |
| u, e | 5 | (3bar)_{-2/3} + (1)_{1} |
| d, N | 10 | (3bar)_{1/3} + 2 neutral singlets |
| L | 10 | (1,2)_{-1/2} |

Each sector carries its pieces with their conjugates.

## Reading

The Wilson-line sectors carry exactly the Standard-Model representations, with the correct hypercharges, split the
way orbifold GUT breaking splits them. The multiplicities are 5 and 10, inherited from the commutant SU(5)', **not 3**.
Every sector is vector-like.

Producer: `analysis/w33_pass12087_standard_model_sectors.py`.
