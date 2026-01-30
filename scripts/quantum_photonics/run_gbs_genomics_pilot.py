"""Small genomics pilot for TDA analogy.
Generates synthetic sequence populations under varying mutation rates, computes k-mer
frequency vectors (k=3) and applies ripser on the k-mer vector point cloud.
Computes JS divergence between k-mer distributions across conditions and Wasserstein
between persistence diagrams.
Saves JSON and plots to bundles.
"""

import json
import random
from pathlib import Path

import matplotlib
import numpy as np
from persim import wasserstein
from ripser import ripser

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import entropy

repo = Path(__file__).resolve().parents[2]
out_dir = repo / "bundles" / "v23_toe_finish" / "v23"
out_dir.mkdir(parents=True, exist_ok=True)

# synthetic genomes: start from a reference and generate mutated variants
ref_len = 1000
bases = ["A", "C", "G", "T"]
ref = "".join(random.choices(bases, k=ref_len))
mutation_rates = [0.01, 0.03, 0.1]
per_condition = 200
k = 3


def mutate(seq, rate):
    s = list(seq)
    for i in range(len(s)):
        if random.random() < rate:
            s[i] = random.choice(bases)
    return "".join(s)


def kmer_freqs(seq, k=3):
    counts = {}
    total = max(1, len(seq) - k + 1)
    for i in range(len(seq) - k + 1):
        kmer = seq[i : i + k]
        counts[kmer] = counts.get(kmer, 0) + 1
    # normalized vector (sorted by kmer key)
    all_kmers = ["".join(p) for p in __import__("itertools").product(bases, repeat=k)]
    vec = np.array([counts.get(km, 0) / total for km in all_kmers], dtype=float)
    return vec


results = []
diagrams = {}
for rate in mutation_rates:
    X = []
    for i in range(per_condition):
        s = mutate(ref, rate)
        v = kmer_freqs(s, k=k)
        X.append(v)
    X = np.array(X)
    dgms = ripser(X, maxdim=1)["dgms"]
    diagrams[rate] = dgms
    # compute average kmer distribution over condition
    mean_kmer = X.mean(axis=0)
    top5 = list(np.argsort(mean_kmer)[-5:])
    top5 = [int(x) for x in top5]
    results.append(
        {"rate": float(rate), "mean_kmer_top5": top5, "h1_features": int(len(dgms[1]))}
    )
    print("rate", rate, "h1 features", len(dgms[1]))

# compute Wasserstein between diagrams and JS between mean kmers
ws = {}
js = {}
for i in range(len(mutation_rates) - 1):
    a = mutation_rates[i]
    b = mutation_rates[i + 1]
    ws[f"{a}-{b}"] = float(wasserstein(diagrams[a][1], diagrams[b][1], matching=False))
    mk_a = X.mean(axis=0) if a == mutation_rates[-1] else None

    # compute mean_kmer from earlier: recompute
    def mean_kmer_for(r):
        # regenerate quickly (cheap)
        Y = []
        for _ in range(per_condition):
            s = mutate(ref, r)
            Y.append(kmer_freqs(s, k=k))
        return np.array(Y).mean(axis=0)

    mk_a = mean_kmer_for(a)
    mk_b = mean_kmer_for(b)
    m = 0.5 * (mk_a + mk_b)
    js_val = 0.5 * (
        entropy(np.maximum(mk_a, 1e-12), np.maximum(m, 1e-12))
        + entropy(np.maximum(mk_b, 1e-12), np.maximum(m, 1e-12))
    )
    js[f"{a}-{b}"] = float(js_val)

out = {"results": results, "wasserstein": ws, "js_between_means": js}
open(out_dir / "genomics_tda_pilot.json", "w").write(json.dumps(out, indent=2))

# simple plot: H1 counts vs mutation rate
rates = [r["rate"] for r in results]
h1s = [r["h1_features"] for r in results]
plt.figure()
plt.plot(rates, h1s, marker="o")
plt.xlabel("mutation rate")
plt.ylabel("H1 feature count")
plt.title("Genomics pilot: H1 counts vs mutation rate")
plt.grid(True)
plt.savefig(out_dir / "genomics_tda_pilot_h1.png")
print("Saved genomics pilot outputs")
