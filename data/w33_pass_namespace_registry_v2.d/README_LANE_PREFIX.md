# Reservation protocol: use a lane prefix

Four collisions in one session (5744, 5776, 5792, 5816) all had the same cause:
**both lanes write the same path**, `<lo>-<hi>.json`. A reservation cannot be claimed by
writing a file whose name the other lane will also choose.

**Fix — prefix the filename with the lane:**

    data/w33_pass_namespace_registry_v2.d/A_5840-5847.json    (Track A)
    data/w33_pass_namespace_registry_v2.d/B_5840-5847.json    (Track B)

Two lanes can then both claim a number without an add/add conflict, and the *earlier
pushed commit* owns the block — resolvable by `git log --diff-filter=A`, not by whoever
rebases last.

**And verify the push landed**, which is not the same as verifying the file exists:

    git branch -r --contains $(git rev-parse HEAD) | grep -c origin/master   # must be >= 1

Checking that the registry *path* exists on origin is what failed at Pass 5800 — it did
exist, as the other lane's file.

**Check `git status -sb` first.** One batch lost several push cycles to a detached HEAD
that every other diagnostic missed.
