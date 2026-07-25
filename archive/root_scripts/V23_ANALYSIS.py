"""V23 l8 deep analysis — streaming through the 3.7GB file."""
import json, sys, os, time
from collections import Counter

JSONL = r"V23_output\l8_patch_octuples_full.jsonl"
META  = r"extracted_v13\W33-Theory-master\artifacts\e8_root_metadata_table.json"
SC_JSON = r"artifacts\e8_structure_constants_w33_discrete.json"

def load_grade_map(meta_path, sc_path):
    """Map basis index -> grade label (robust to metadata root ordering)."""
    with open(meta_path) as f:
        meta = json.load(f)
    grade_by_root = {
        tuple(int(x) for x in row["root_orbit"]): row["grade"] for row in meta["rows"]
    }

    with open(sc_path) as f:
        sc = json.load(f)
    roots = sc["basis"]["roots"]
    cartan_dim = int(sc["basis"]["cartan_dim"])
    if cartan_dim != 8:
        raise RuntimeError(f"Unexpected cartan_dim={cartan_dim} (expected 8)")

    gmap = {}
    for i in range(cartan_dim):
        gmap[i] = "cartan"
    for idx, rt in enumerate(roots):
        gmap[cartan_dim + idx] = grade_by_root[tuple(int(x) for x in rt)]
    return gmap

def main():
    t0 = time.time()
    max_lines = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    gmap = load_grade_map(META, SC_JSON)
    
    # Counters
    total = 0
    single = 0
    multi = 0
    coeff_counter = Counter()   # for single-term
    max_abs_coeff = 0
    max_coeff_entry = None
    multi_max_terms = 0
    multi_max_entry = None
    
    # Grade distribution of outputs (single-term)
    grade_out = Counter()  # grade -> count
    
    # Multi-term analysis
    multi_term_counts = Counter()  # number of terms -> count
    multi_output_grades = Counter()  # which grades appear in multi-term outputs
    multi_all_cartan = 0
    multi_has_root = 0
    multi_coeff_max = 0
    
    # Support tracking
    output_indices = set()

    # Input tracking (sanity)
    input_grade = Counter()
    input_indices = set()
    
    with open(JSONL, 'r') as f:
        for line in f:
            if max_lines and total >= max_lines:
                break
            total += 1
            entry = json.loads(line)

            for x in entry.get("in", []):
                xi = int(x)
                input_indices.add(xi)
                input_grade[gmap.get(xi, "?")] += 1
            
            if "coeff" in entry:
                # Single-term
                single += 1
                c = entry["coeff"]
                out = entry["out"]
                coeff_counter[c] += 1
                output_indices.add(out)
                grade_out[gmap.get(out, "?")] += 1
                ac = abs(c)
                if ac > max_abs_coeff:
                    max_abs_coeff = ac
                    max_coeff_entry = entry
            else:
                # Multi-term
                multi += 1
                terms = entry["terms"]
                n_terms = len(terms)
                multi_term_counts[n_terms] += 1
                if n_terms > multi_max_terms:
                    multi_max_terms = n_terms
                    multi_max_entry = entry
                
                all_cartan = True
                for idx_c in terms:
                    idx = idx_c[0]
                    c = idx_c[1]
                    output_indices.add(idx)
                    g = gmap.get(idx, "?")
                    multi_output_grades[g] += 1
                    if g != "cartan":
                        all_cartan = False
                    ac = abs(c)
                    if ac > multi_coeff_max:
                        multi_coeff_max = ac
                
                if all_cartan:
                    multi_all_cartan += 1
                else:
                    multi_has_root += 1
            
            if total % 5_000_000 == 0:
                elapsed = time.time() - t0
                print(f"  [{total:,}] elapsed={elapsed:.1f}s", flush=True)
    
    elapsed = time.time() - t0
    
    print(f"\n{'='*70}")
    print(f"V23 l8 DEEP ANALYSIS")
    print(f"{'='*70}")
    print(f"\nTotal entries: {total:,} (single={single:,} multi={multi:,})")
    print(f"Output support: {len(output_indices)} / 248")
    uniq_in_grade = Counter(gmap.get(i, "?") for i in input_indices)
    print(f"Unique input indices seen: {len(input_indices)} (grades={dict(uniq_in_grade)})")
    print(f"Input grade totals: {dict(input_grade)}")
    print(f"Analysis time: {elapsed:.1f}s")
    
    print(f"\n--- SINGLE-TERM COEFFICIENTS ---")
    print(f"Max |coeff|: {max_abs_coeff}")
    print(f"Max coeff entry: {max_coeff_entry}")
    print(f"\nTop 20 by frequency:")
    for c, cnt in coeff_counter.most_common(20):
        print(f"  coeff {c:+d}: {cnt:,}")
    print(f"\nCoeffs with |c| > 10:")
    big = {c: cnt for c, cnt in coeff_counter.items() if abs(c) > 10}
    for c in sorted(big.keys(), key=lambda x: -abs(x)):
        print(f"  coeff {c:+d}: {big[c]:,}")
    
    print(f"\n--- GRADE DISTRIBUTION (single-term outputs) ---")
    for g in ["cartan", "g0", "g1", "g2"]:
        cnt = grade_out.get(g, 0)
        pct = 100.0 * cnt / single if single else 0
        print(f"  {g}: {cnt:,} ({pct:.2f}%)")
    
    print(f"\n--- MULTI-TERM ANALYSIS ---")
    print(f"Total multi: {multi:,}")
    print(f"All-Cartan multi: {multi_all_cartan:,} ({100*multi_all_cartan/multi:.1f}%)" if multi else "N/A")
    print(f"Has-root multi:   {multi_has_root:,} ({100*multi_has_root/multi:.1f}%)" if multi else "N/A")
    print(f"Max terms in one entry: {multi_max_terms}")
    print(f"Max |coeff| in multi: {multi_coeff_max}")
    print(f"Multi-term entry with most terms: {multi_max_entry}")
    print(f"\nTerm count distribution:")
    for n, cnt in sorted(multi_term_counts.items()):
        print(f"  {n} terms: {cnt:,}")
    print(f"\nMulti-term output grade distribution:")
    for g in ["cartan", "g0", "g1", "g2"]:
        cnt = multi_output_grades.get(g, 0)
        print(f"  {g}: {cnt:,}")

if __name__ == "__main__":
    main()
