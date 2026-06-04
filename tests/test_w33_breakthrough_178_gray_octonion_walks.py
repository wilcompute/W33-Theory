"""Tests for BT178: q! Gray-octonion walks counted"""
import math

q, mu, lam = 3, 4, 2
q_fac = math.factorial(q)

def hamming(n): return bin(n).count('1')
def even_adj(a, b): return bin(a^b).count('1') == 2

even_class = [v for v in range(16) if hamming(v) % 2 == 0]
even_graph = {v: [u for u in even_class if u!=v and even_adj(u,v)] for v in even_class}

FANO_LINES = [
    frozenset({0,1,2}), frozenset({0,3,4}), frozenset({0,5,6}),
    frozenset({1,3,5}), frozenset({1,4,6}), frozenset({2,3,6}), frozenset({2,4,5})
]
fano_verts = [v for v in even_class if v != 0]
fano_to_q4 = {i+1: fano_verts[i] for i in range(7)}
q4_to_fano = {v: k for k,v in fano_to_q4.items()}

def on_fano_line(a, b):
    fa, fb = q4_to_fano.get(a), q4_to_fano.get(b)
    if fa is None or fb is None: return False
    return any(fa in L and fb in L for L in FANO_LINES)

def fano_mult_pos(a, b):
    fa, fb = q4_to_fano.get(a), q4_to_fano.get(b)
    if fa is None or fb is None: return False
    for L in FANO_LINES:
        if fa in L and fb in L:
            pts = sorted(L); i,j,k = pts
            return (fa,fb) in [(i,j),(j,k),(k,i)]
    return False

def find_paths(start, graph, length):
    paths = []
    def dfs(path, visited):
        if len(path) == length+1: paths.append(tuple(path)); return
        for u in graph[path[-1]]:
            if u not in visited:
                visited.add(u); path.append(u)
                dfs(path, visited)
                path.pop(); visited.remove(u)
    dfs([start], {start})
    return paths

paths_from_0 = find_paths(0, even_graph, q_fac)
fano_consistent = [p for p in paths_from_0
                   if all(on_fano_line(p[i],p[i+1]) for i in range(1,len(p)-1))]
positive_paths  = [p for p in fano_consistent
                   if all(fano_mult_pos(p[i],p[i+1]) for i in range(1,len(p)-1))]

def test_fano_consistent_count(): assert len(fano_consistent) == 240
def test_positive_count():         assert len(positive_paths) == 16
def test_240_substrate():          assert 240 == lam * math.factorial(mu+1)
def test_16_substrate():           assert 16  == lam**mu
def test_even_graph_6_regular():   assert all(len(even_graph[v])==6 for v in even_class)

if __name__ == '__main__':
    test_fano_consistent_count()
    test_positive_count()
    test_240_substrate()
    test_16_substrate()
    test_even_graph_6_regular()
    print('BT178: 5/5 tests passed')
