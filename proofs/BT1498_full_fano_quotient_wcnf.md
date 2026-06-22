# BT1498 Full Fano Quotient WCNF

This is a full quotient scaffold, not a solved global optimum proof.

Variables:

- 1..540: skew residual identity-edge soft variables.
- 541..547: Fano point anchor one-hot variables.
- 548..568: Fano flag anchor one-hot variables.
- 569..571: local fiber block one-hot variables.

Hard constraints enforce exactly one point, exactly one flag, and exactly one fiber block.
Soft clauses reward identity-edge retention. Future work adds orbit-specific hard compatibility clauses and imports a solver certificate.
