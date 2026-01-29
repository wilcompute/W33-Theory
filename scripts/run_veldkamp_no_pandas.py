import json
import sys
import traceback
from pathlib import Path

try:
    from src.finite_geometry.veldmap import neighborhoods_from_triangles, point_hyperplanes, veldkamp_space_from_generators

    p = Path('bundles/v23_toe_finish/v23/Q_triangles_with_centers_Z2_S3_fiber6.csv')
    print('CSV exists:', p.exists())
    triangles = []
    with p.open('r', encoding='utf-8') as f:
        header = next(f)
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(',')
            try:
                u = int(parts[0])
                v = int(parts[1])
                w = int(parts[2])
            except Exception:
                # skip malformed line
                continue
            triangles.append((u, v, w))

    neighborhoods = neighborhoods_from_triangles(triangles)
    gens = list(point_hyperplanes(neighborhoods).values())
    veld = veldkamp_space_from_generators(gens)

    size_hist = {k: v for k, v in sorted(__import__('collections').Counter(len(s) for s in veld).items())}
    gen_size_hist = {k: v for k, v in sorted(__import__('collections').Counter(len(g) for g in gens).items())}
    deg_hist = {k: v for k, v in sorted(__import__('collections').Counter(len(neighborhoods.get(p, [])) for p in neighborhoods).items())}

    summary = {
        'n_points': len(set().union(*gens)),
        'n_triangles': len(triangles),
        'n_generators': len(gens),
        'generator_size_hist': gen_size_hist,
        'n_veldkamp': len(veld),
        'veldkamp_size_hist': size_hist,
        'degree_hist': deg_hist,
    }
    out = Path('bundles/v23_toe_finish/v23/veld_summary.json')
    with out.open('w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, default=str)
    # small stdout confirmation so human-readable logs are available if terminal captures them
    print(f"Wrote summary to {out} (n_triangles={summary['n_triangles']}, n_points={summary['n_points']})")
except Exception:
    traceback.print_exc()
    sys.exit(1)
