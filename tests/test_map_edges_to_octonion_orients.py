import json
import zipfile
from pathlib import Path
import subprocess

def make_zip(src_dir: Path, dst_zip: Path):
    with zipfile.ZipFile(dst_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
        for p in src_dir.rglob('*'):
            if p.is_file():
                zf.write(p, p.relative_to(src_dir))

def test_map_edges_synthetic(tmp_path):
    repo = Path(__file__).resolve().parents[1]
    # build triangle zip as before
    tri_folder = repo / 'TOE_E6pair_SRG_triangle_decomp_v01_20260227_bundle'
    tri_zip = tmp_path / 'tri.zip'
    make_zip(tri_folder, tri_zip)
    # read pairs36 from tri_zip
    with zipfile.ZipFile(tri_zip) as zf:
        text = zf.read('TOE_E6pair_SRG_triangle_decomp_v01_20260227/e6_antipode_pairs_36.json')
        pairs36 = json.loads(text)['pairs']
    # instead of searching pockets we just pick a few valid rootpair triples
    # use the first three antipode pairs repeated
    with zipfile.ZipFile(tri_zip) as zf:
        pairs36 = json.loads(zf.read('TOE_E6pair_SRG_triangle_decomp_v01_20260227/e6_antipode_pairs_36.json'))['pairs']
    # pick first three pairs to form our synthetic triples
    base_triple = [pairs36[0], pairs36[1], pairs36[2]]
    edge_map = [base_triple for _ in range(5)]
    assert len(edge_map) == 5
    # write to json and zip it
    tmp_json = tmp_path / 'edge_map.json'
    json.dump(edge_map, open(tmp_json,'w'))
    edge_zip = tmp_path / 'edge.zip'
    with zipfile.ZipFile(edge_zip,'w',zipfile.ZIP_DEFLATED) as zf:
        zf.write(tmp_json, 'TOE_edge_to_oriented_rootpairs_v01_20260227/edge_to_oriented_rootpair_triple.json')
    # run mapping script
    outpath = tmp_path / 'map.json'
    res = subprocess.run([
        ".venv\\Scripts\\python.exe",
        str(repo / 'tools' / 'map_edges_to_octonion_orients.py'),
        '--tri_zip', str(tri_zip),
        '--edge_zip', str(edge_zip),
        '--out', str(outpath)
    ], cwd=repo)
    assert res.returncode == 0
    data = json.loads(outpath.read_text(encoding="utf-8"))
    assert 'edge_to_orient' in data
    assert len(data['edge_to_orient']) == 5
    # values may be None if orientation not available
    assert all((v is None or isinstance(v, int)) for v in data['edge_to_orient'])
    assert isinstance(data['orientations'], list)


def test_real_mapping_bundle():
    # ensure the bundle we just packaged contains a valid mapping
    bundle = Path('TOE_edge_orient_map_v01_20260227_bundle.zip')
    assert bundle.exists(), f"bundle {bundle} should exist"
    with zipfile.ZipFile(bundle) as zf:
        info = zf.getinfo('TOE_edge_orient_map_v01_20260227/edge_orient_map_real.json')
        assert info.file_size > 0
        data = json.loads(zf.read(info.filename).decode())
    assert 'edge_to_orient' in data
    assert len(data['edge_to_orient']) == 240
    # orientations list should still have length 480
    assert len(data.get('orientations', [])) == 480
    # expect nearly all edges to receive an orientation index
    nonnull = sum(1 for v in data['edge_to_orient'] if v is not None)
    # two edges appear to be unorientable by the available triple data
    assert nonnull >= 236, f"too few oriented edges ({nonnull}); expected at least 236"
