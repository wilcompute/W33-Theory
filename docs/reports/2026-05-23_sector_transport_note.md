# Sector transport note

This note records the point-projected nonbacktracking transport calculation for W33.

Let A be the W33 adjacency matrix.  The adjacency spectrum is 12 with multiplicity 1, 2 with multiplicity 24, and -4 with multiplicity 15.

The one-step point transport is K1 = A/12.  Its sector values are 1 on the constant sector, 1/6 on the 24-dimensional sector, and -1/3 on the 15-dimensional sector.

The two-step nonbacktracking point closure is K2 = (A^2 - 12 I)/(12*11).  Using the SRG identity, A^2 - 12I = 4J - 4I - 2A.  Its sector values are 1 on the constant sector, -2/33 on the 24-dimensional sector, and 1/33 on the 15-dimensional sector.

Thus the 15-dimensional sector returns with positive two-step coefficient 1/33.  The denominator is 33 = 3*11, combining the ternary parameter q = 3 with the nonbacktracking branching number 11.
