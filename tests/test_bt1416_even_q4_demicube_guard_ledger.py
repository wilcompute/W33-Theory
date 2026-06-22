import importlib.util
from pathlib import Path


def load_module():
    path = Path(__file__).resolve().parents[1] / "tools" / "bt1416_even_q4_demicube_guard_ledger.py"
    spec = importlib.util.spec_from_file_location("bt1416_even_q4_demicube_guard_ledger", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def test_even_layer_is_demicube():
    mod = load_module()
    even_words = [mod.int_to_word(t) for t in mod.BT1412_EVEN_TICKS]
    graph = mod.even_layer_graph(even_words)
    assert graph.number_of_nodes() == 8
    assert graph.number_of_edges() == 24
    assert sorted(dict(graph.degree()).values()) == [6] * 8


def test_q4_faces_biject_to_even_diagonals():
    mod = load_module()
    even_words = [mod.int_to_word(t) for t in mod.BT1412_EVEN_TICKS]
    graph = mod.even_layer_graph(even_words)
    edge_set = {
        tuple(sorted((mod.word_to_int(a), mod.word_to_int(b))))
        for a, b in graph.edges()
    }
    face_edges = set()
    for face in mod.q4_square_faces():
        evens = [v for v in face["vertices"] if sum(v) % 2 == 0]
        assert len(evens) == 2
        face_edges.add(tuple(sorted((mod.word_to_int(evens[0]), mod.word_to_int(evens[1])))))
    assert face_edges == edge_set


def test_guard_and_full_ledger_ranks():
    mod = load_module()
    even_words = [mod.int_to_word(t) for t in mod.BT1412_EVEN_TICKS]
    idx = {w: i for i, w in enumerate(even_words)}
    guard_rows = []
    for face in mod.q4_square_faces():
        evens = [v for v in face["vertices"] if sum(v) % 2 == 0]
        row = [0] * 8
        row[idx[evens[0]]] = 1
        row[idx[evens[1]]] = 1
        guard_rows.append(row)

    singleton_rows = []
    for _cycle in range(27):
        for state_idx in range(8):
            row = [0] * 8
            row[state_idx] = 1
            singleton_rows.append(row)

    assert mod.gf2_rank(guard_rows) == 7
    assert mod.gf2_rank(singleton_rows + guard_rows) == 8
    assert len(singleton_rows) + len(guard_rows) == 240
