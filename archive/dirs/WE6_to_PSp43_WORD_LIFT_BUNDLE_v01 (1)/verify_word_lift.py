import os
from pathlib import Path
os.chdir(Path(__file__).resolve().parent)  # Pass 5548: JSONs opened by bare filename
\
import json
from collections import deque

def compose(p,q):
    return [p[i] for i in q]

def inv_perm(p):
    inv=[0]*len(p)
    for i,pi in enumerate(p):
        inv[pi]=i
    return inv

def perm_bytes(p):
    return bytes(p)

def conjugate_perm(p, sigma, sigma_inv):
    return [sigma[p[sigma_inv[j]]] for j in range(len(p))]

def eval_word(word, gens_dict):
    n = len(next(iter(gens_dict.values())))
    cur = list(range(n))
    # build inverses lazily
    inv_cache = {}
    for token in word:
        if token.endswith("^-1"):
            base = token[:-3]
            if base not in inv_cache:
                inv_cache[base] = inv_perm(gens_dict[base])
            g = inv_cache[base]
        else:
            g = gens_dict[token]
        cur = compose(g, cur)
    return cur

# load artifacts
sigma_dat = json.load(open("sigma_we6coset_to_w33line.json"))
sigma = sigma_dat["sigma_we6coset_to_w33line"]
sigma_inv = sigma_dat["sigma_inv_w33line_to_we6coset"]

we6_gens = json.load(open("we6coset_generators_10.json"))["generators"]
psp_gens_dict = json.load(open("psp43_line_generators_6.json"))["generators"]
mapping = json.load(open("we6_generators_as_words_in_psp43_line_action.json"))

# verify each generator
bad = []
for i,g in enumerate(we6_gens):
    conj = conjugate_perm(g, sigma, sigma_inv)
    word = mapping["we6_generator_word_in_psp"][f"we6_gen_{i}"]
    val = eval_word(word, psp_gens_dict)
    if val != conj:
        bad.append(i)

if bad:
    raise SystemExit(f"FAILED: word mismatch for generators {bad}")
print("ALL CHECKS PASSED: words evaluate exactly to σ ∘ we6_gen_i ∘ σ^{-1} for all 10 generators.")
