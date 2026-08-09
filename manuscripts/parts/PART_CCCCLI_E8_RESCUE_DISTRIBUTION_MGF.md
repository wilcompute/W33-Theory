# PART CCCCLI — E8 Rescue Distribution and Generating-Function Law

This part turns the CCCCL lookup law into an exact global distribution theorem.

Let $R(a,b)$ be the third-reference rescue count for unordered doubled E8 root
pairs $(a,b)$ (including diagonal), with total pair count $N=28920$.

## Exact distribution

$$
\#\{R=126\}=360,\qquad
\#\{R=234\}=13440,\qquad
\#\{R=240\}=15120.
$$

## Counting generating function

$$
P(t)=360\,t^{126}+13440\,t^{234}+15120\,t^{240}.
$$

Normalized probability generating function:

$$
G(t)=\frac{P(t)}{28920}.
$$

## Immediate corollary

Weighted rescue total:

$$
\sum_{(a,b)} R(a,b)=6819120.
$$

So all higher rescue moments are computable exactly from this triatomic law.

## Honesty boundary

This is a global distributional corollary of CCCCL’s exact dot-class lookup law,
not an independent derivation of the lookup itself.
