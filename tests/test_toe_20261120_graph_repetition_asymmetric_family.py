"""Independent small-graph controls for the mixed qutrit hypergraph product."""
import sys
import unittest
from pathlib import Path
import networkx as nx
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"analysis"))
from toe_20261120_graph_repetition_asymmetric_family import run,verify_graph

class GeneralGraphHGPTests(unittest.TestCase):
    def test_all_four_graphs(self):
        out=run(write=False)
        found={e["graph"]:e["parameters"] for e in out["examples"]}
        self.assertEqual(found["cube_Q3"],dict(n=50,k=5,dX=3,dZ=4,d=3))
        self.assertEqual(found["Petersen"],dict(n=63,k=6,dX=3,dZ=5,d=3))
        self.assertEqual(found["Heawood"],dict(n=89,k=8,dX=3,dZ=6,d=3))
        self.assertEqual(found["W33_Levi"],dict(n=638,k=81,dX=3,dZ=8,d=3))
        self.assertTrue(all(e["proof_checks"]["commuting_stabilizers"] for e in out["examples"]))
    def test_invalid_graph_guard(self):
        # A path cannot support the claimed code geometry.
        with self.assertRaises(AssertionError):
            verify_graph(nx.path_graph(7),"path")
        # Disconnected sources are rejected.
        with self.assertRaises(AssertionError):
            verify_graph(nx.disjoint_union(nx.petersen_graph(),nx.petersen_graph()),"disjoint")
    def test_generic_symmetric_cubic_case(self):
        p=verify_graph(nx.petersen_graph(),"Petersen")
        self.assertEqual(p["check_weights"],{"HX":5,"HZ":4})
        self.assertNotEqual(p["proof_checks"]["anticommuting_logical_pair"],0)

if __name__=="__main__":
    unittest.main()
