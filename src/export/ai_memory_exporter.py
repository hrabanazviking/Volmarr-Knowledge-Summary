"""AI Companion Memory & RAG Knowledge Exporter (Milestone 7 & Phase 40).
Generates structured, vector-ready knowledge units optimized for LLM context injection,
agent retrieval systems, and AI fylgja companionship models.
"""

import json
from pathlib import Path
from rich.console import Console

console = Console()

class AIMemoryExporter:
    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir)
        self.db_dir = self.root_dir / "data" / "database"
        self.export_dir = self.root_dir / "data" / "export"
        self.export_dir.mkdir(parents=True, exist_ok=True)
        self.output_json = self.export_dir / "ai_companion_memory.json"
        self.output_jsonl = self.export_dir / "ai_companion_memory.jsonl"
        self.meta_json = self.root_dir / "knowledge" / "_meta" / "ai_companion_memory.json"

    def export_memory_pack(self) -> dict:
        console.print("[bold cyan]Exporting AI Companion Memory Pack for RAG & Agent Ingestion...[/bold cyan]")
        
        registry_file = self.db_dir / "concept_registry.jsonl"
        graph_file = self.db_dir / "prerequisite_graph.json"

        if not registry_file.exists():
            raise FileNotFoundError(f"Registry file not found at {registry_file}")
            
        concepts = []
        with open(registry_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    concepts.append(json.loads(line))

        graph_data = {}
        if graph_file.exists():
            with open(graph_file, "r", encoding="utf-8") as f:
                graph_data = json.load(f)

        # Map edges to dependents
        dependents_map = {}
        prereqs_map = {}
        for edge in graph_data.get("edges", []):
            src = edge["source"]
            tgt = edge["target"]
            dependents_map.setdefault(src, []).append(tgt)
            prereqs_map.setdefault(tgt, []).append(src)

        memory_units = []
        for c in concepts:
            cid = c["concept_id"]
            slug = c.get("slug", cid)
            name = c["canonical_name"]
            definition = c.get("definition_short", "")
            principles = c.get("core_principles", [])
            tier = c.get("taxonomy_level", "")
            epistemic = c.get("knowledge_types", [])
            sources = c.get("source_urls", [])

            # Generate high-density LLM prompt injection snippet
            prompt_snippet = (
                f"### CANONICAL AXIOM: {name} (Tier: {tier})\n"
                f"Definition: {definition}\n"
                f"Core Principles:\n" + "\n".join(f"- {p}" for p in principles[:5]) + "\n"
                f"Epistemic Status: {', '.join(epistemic)}\n"
                f"Prerequisites: {', '.join(prereqs_map.get(slug, [])) or 'Foundational root'}\n"
                f"Enables: {', '.join(dependents_map.get(slug, [])) or 'Terminal synthesis'}"
            )

            unit = {
                "concept_id": cid,
                "slug": slug,
                "canonical_name": name,
                "taxonomy_level": tier,
                "definition": definition,
                "core_principles": principles,
                "prerequisites": prereqs_map.get(slug, []),
                "dependents": dependents_map.get(slug, []),
                "epistemic_categories": epistemic,
                "source_provenance_urls": sources,
                "llm_context_prompt": prompt_snippet
            }
            memory_units.append(unit)

        memory_pack = {
            "metadata": {
                "title": "Volmarr Heathen Third Path AI Companion Knowledge Pack",
                "version": "1.0.0",
                "source": "https://volmarrsheathenism.com",
                "total_concepts": len(memory_units),
                "license": "CC-BY-SA-4.0",
                "purpose": "RAG vector database ingestion & AI companion cognitive ground truth"
            },
            "concepts": memory_units
        }

        # Write JSON
        with open(self.output_json, "w", encoding="utf-8") as f:
            json.dump(memory_pack, f, indent=2, ensure_ascii=False)

        # Write JSONL
        with open(self.output_jsonl, "w", encoding="utf-8") as f:
            for u in memory_units:
                f.write(json.dumps(u, ensure_ascii=False) + "\n")

        # Mirror to knowledge/_meta
        self.meta_json.parent.mkdir(parents=True, exist_ok=True)
        with open(self.meta_json, "w", encoding="utf-8") as f:
            json.dump(memory_pack, f, indent=2, ensure_ascii=False)

        console.print(f"[bold green][OK] Memory pack exported: {self.output_json} ({len(memory_units)} concepts)[/bold green]")
        return memory_pack

if __name__ == "__main__":
    AIMemoryExporter().export_memory_pack()
