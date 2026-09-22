"""Prerequisite Graph and Topological Ordering Module.
Constructs conceptual dependency DAG, verifies cycle-free learning progression,
and determines canonical reading order.
"""

import json
from pathlib import Path
import networkx as nx
from rich.console import Console

console = Console()

class PrerequisiteGraph:
    def __init__(self, registry_path: str = "data/database/concept_registry.jsonl", db_dir: str = "data/database"):
        self.registry_path = Path(registry_path)
        self.db_dir = Path(db_dir)
        self.graph_path = self.db_dir / "prerequisite_graph.json"

    def build_graph(self) -> tuple[nx.DiGraph, list[dict]]:
        if not self.registry_path.exists():
            raise FileNotFoundError(f"Registry not found: {self.registry_path}")

        concepts = []
        with open(self.registry_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    concepts.append(json.loads(line))

        G = nx.DiGraph()

        # Add nodes
        for c in concepts:
            cid = c["slug"]
            G.add_node(
                cid,
                canonical_name=c["canonical_name"],
                taxonomy_level=c["taxonomy_level"],
                definition_short=c["definition_short"],
                prerequisites=c["prerequisites"],
                total_claims=c["total_claims"],
                source_count=c["source_articles_count"]
            )

        # Add edges: prerequisite -> concept (must learn prerequisite first)
        for c in concepts:
            cid = c["slug"]
            for prereq in c["prerequisites"]:
                if prereq in G:
                    G.add_edge(prereq, cid, relation="PREREQUISITE_FOR")
                else:
                    console.print(f"[yellow]Warning: prerequisite '{prereq}' not in graph[/yellow]")

        # Check for cycles
        if not nx.is_directed_acyclic_graph(G):
            cycles = list(nx.simple_cycles(G))
            raise ValueError(f"Cycle detected in prerequisite graph: {cycles}")

        # Compute topological ordering
        ordered_slugs = list(nx.topological_sort(G))
        
        # Calculate complexity scores (depth in graph + level weighting)
        ordered_concepts = []
        for rank, slug in enumerate(ordered_slugs, start=1):
            node_data = G.nodes[slug]
            ancestors = nx.ancestors(G, slug)
            depth = len(ancestors)
            complexity = depth * 2 + (1 if node_data["source_count"] > 5 else 0)
            
            entry = {
                "rank": rank,
                "slug": slug,
                "canonical_name": node_data["canonical_name"],
                "taxonomy_level": node_data["taxonomy_level"],
                "prerequisites": node_data["prerequisites"],
                "prerequisite_depth": depth,
                "complexity_score": complexity,
                "definition_short": node_data["definition_short"]
            }
            ordered_concepts.append(entry)

        # Export graph to JSON
        graph_data = {
            "nodes": [
                {
                    "id": n,
                    **G.nodes[n],
                    "ancestors": list(nx.ancestors(G, n)),
                    "descendants": list(nx.descendants(G, n))
                }
                for n in G.nodes()
            ],
            "edges": [
                {"source": u, "target": v, "relation": d.get("relation", "DEPENDS_ON")}
                for u, v, d in G.edges(data=True)
            ],
            "topological_reading_order": ordered_concepts
        }

        with open(self.graph_path, "w", encoding="utf-8") as f:
            json.dump(graph_data, f, indent=2, ensure_ascii=False)

        console.print(f"[bold green]Prerequisite graph generated successfully.[/bold green] Nodes: {len(G.nodes)}, Edges: {len(G.edges)}")
        console.print("[bold cyan]Topological Reading Order:[/bold cyan]")
        for c in ordered_concepts:
            console.print(f"  {c['rank']:02d}. [bold]{c['canonical_name']}[/bold] ({c['taxonomy_level']}) - Prereqs: {c['prerequisites']}")

        return G, ordered_concepts

if __name__ == "__main__":
    pg = PrerequisiteGraph()
    pg.build_graph()
