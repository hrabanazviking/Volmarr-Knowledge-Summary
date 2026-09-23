import json
from pathlib import Path
import networkx as nx

GRAPH_FILE = Path("data/database/prerequisite_graph.json")

def test_prerequisite_graph_is_dag():
    assert GRAPH_FILE.exists()
    data = json.loads(GRAPH_FILE.read_text(encoding="utf-8"))
    
    nodes = data["nodes"]
    edges = data["edges"]
    topological_order = data["topological_reading_order"]
    
    assert len(nodes) == 64, f"Expected 64 nodes, got {len(nodes)}"
    assert len(edges) >= 30, f"Expected at least 30 edges, got {len(edges)}"
    assert len(topological_order) == 64, f"Topological order missing nodes"
    
    G = nx.DiGraph()
    for n in nodes:
        G.add_node(n["id"])
    for e in edges:
        G.add_edge(e["source"], e["target"])
        
    assert nx.is_directed_acyclic_graph(G), "Prerequisite graph contains cycles!"

def test_prerequisites_precede_dependents_in_reading_order():
    data = json.loads(GRAPH_FILE.read_text(encoding="utf-8"))
    topological_order = data["topological_reading_order"]
    order_map = {item["slug"]: idx for idx, item in enumerate(topological_order)}
    
    for edge in data["edges"]:
        src = edge["source"]
        tgt = edge["target"]
        assert order_map[src] < order_map[tgt], (
            f"Ordering violation: Prerequisite {src} (index {order_map[src]}) "
            f"does not precede dependent {tgt} (index {order_map[tgt]})"
        )
