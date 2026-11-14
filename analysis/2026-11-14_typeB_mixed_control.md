# Mixed-state control for the four-qubit regulus experiment

The [five-circuit experiment](PASS12664_TYPE_B_CERTAINTY_RELATION_AS_AN_EXPERIMENT.md) uses a pure-state collision floor of 713/2000. A rank-two mixed state can reach the absolute floor of 5/16 exactly. This control matters when testing the certainty relation with unknown preparation noise.

Using the two-ququart Pauli chart, take labels 17, 35 and 72, with x in the low four bits and z in the high four. Let N be the product of I+P over these three labels. The executable verifies N is Hermitian, N squared equals 8N, and its trace is 16, so rho=N/16 is half of a rank-two projector. In each of the five measurement bases the diagonal of rho is exactly uniform. The check uses Gaussian-integer arithmetic with scaled Hadamard matrices. Consequently these measurements cannot distinguish this state of purity 1/2 from the maximally mixed state of purity 1/16.

## A floor from independent purity data

Let F be the collision sum minus 5/16. The centered probability map sends rho to the 80 measured probabilities minus 1/16. Mutual unbiasedness makes the five traceless diagonal operator spaces orthogonal in the Hilbert-Schmidt inner product. Therefore the norm of the centered probability vector is sqrt(F), and its squared norm is at most Tr(rho squared)-1/16. In particular the norm is at most sqrt(15/16) for any state.

Let lambda be the largest eigenvalue and write rho=lambda times its top pure eigenprojector plus (1-lambda) times the normalized remainder. The reverse triangle inequality and the exact pure-state floor give

    F >= max(0, lambda sqrt(11/250) - (1-lambda) sqrt(15/16))^2.

If a separately measured purity lower bound is p>=1/2, then lambda >= (1+sqrt(2p-1))/2. Indeed lambda is at least the purity, and the sum of the squares of the other eigenvalues is at most (1-lambda)^2. At p=0.95 the collision floor is at least 0.344733, without assuming a depolarizing channel. The formula gives 0.3565 at purity one.

For finite shots, use the fraction of unordered pairs with matching outcomes in each basis. Its expectation is the collision probability exactly for independent identically distributed outcomes. The earlier roughly 750 shots is a plug-in bias estimate. A statistical test still needs confidence bounds on the collision statistic and independent purity estimate. [Collision U-statistics](https://pmc.ncbi.nlm.nih.gov/articles/PMC9955260/)

Replay with py -3 analysis/toe_20261114_typeB_mixed_control.py.
