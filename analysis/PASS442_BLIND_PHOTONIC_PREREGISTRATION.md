# Pass 442 — blind transfer-matrix photonic preregistration

Pass 439's discriminator is now wrapped in a blinded preregistration protocol.

## Frozen protocol

- 16 Ramsey/echo phase steps.
- 16,384 binary shots per phase.
- Fixed 16×16 circulant optical transfer matrix.
- Affine nuisance fit for visibility and dark offset.
- Minimum transferred-template residual classifier.
- Abstention threshold `0.0025`.
- Primary endpoint: balanced accuracy on a sealed 192-sample holdout.
- No post-sealing exclusion rule.

Each truth label is committed as `SHA256(salt | sample_id | label)` before
prediction. Predictions and margins are recorded before the salt is revealed.
The reveal then verifies every commitment and scores the frozen classifier.

## Dry-run result

- 192 commitments verified.
- 192 decisions, zero abstentions.
- 192/192 correct.
- Minimum residual margin: `0.0033035860060288205`, above the frozen threshold.

## Boundary

This is a deterministic synthetic preregistration rehearsal, not measured
optical data. The exact replacement boundary is exposed: substitute a measured
transfer matrix for the synthetic kernel without changing the phase schedule,
classifier, threshold, label commitment, or endpoint.
