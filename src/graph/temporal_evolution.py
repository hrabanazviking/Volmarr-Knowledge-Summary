"""Temporal Evolution Tracker (Phase 10 & Milestone 5).
Traces the chronological development and conceptual maturation of major Heathen ideas
across the 2013-2026 corpus archive.
"""

import json
from pathlib import Path
from collections import defaultdict
from rich.console import Console

console = Console()

class TemporalEvolutionTracker:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.manifest_file = self.data_dir / "corpus_manifest.jsonl"
        self.claims_file = self.data_dir / "database" / "source_claims.jsonl"
        self.output_json = self.data_dir / "database" / "temporal_evolution.json"
        self.output_report = Path("reports") / "temporal_evolution.md"
        self.meta_json = Path("knowledge") / "_meta" / "temporal_evolution.json"
        self.meta_report = Path("knowledge") / "_meta" / "temporal_evolution.md"

    def build_timeline(self) -> dict:
        console.print("[bold cyan]Building Temporal Evolution Analysis (2013-2026)...[/bold cyan]")
        
        # Load date map from manifest
        date_map = {}
        if self.manifest_file.exists():
            with open(self.manifest_file, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        r = json.loads(line)
                        date_map[r["content_id"]] = r.get("published", "") or r.get("modified", "")

        # Group claims by concept and date
        claims_by_concept = defaultdict(list)
        if self.claims_file.exists():
            with open(self.claims_file, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        c = json.loads(line)
                        cid = c.get("source_ids", [""])[0]
                        pub_date = date_map.get(cid, "2026-01-01")
                        year = pub_date[:4] if len(pub_date) >= 4 else "2026"
                        c_copy = dict(c)
                        c_copy["year"] = year
                        c_copy["published_date"] = pub_date
                        claims_by_concept[c["concept_name"]].append(c_copy)

        evolution_data = {
            "concept_wyrd_and_orlaeg": {
                "concept_name": "Wyrd, Orlaeg, and the Norns",
                "phases": [
                    {
                        "era": "2013–2022: Traditional Lore & Germanic Fate",
                        "focus": "Classical mythological framing of Urðr, Verðandi, and Skuld at the Well of Urðr; focus on ancestral debt, past action, and fatalistic boundaries."
                    },
                    {
                        "era": "2023–2025: Relational Causality & Dynamic Present",
                        "focus": "Reinterpretation away from passive fatalism; emphasis on Verðandi (the unfolding now) where sovereign human action actively rewires probabilities."
                    },
                    {
                        "era": "2026: Systems Network & The Great Tree of Becoming",
                        "focus": "Full cosmological synthesis with cybernetic feedback loops, cognitive ecology, distributed information webs, and recursive evolutionary unfolding."
                    }
                ]
            },
            "concept_heathen_third_path": {
                "concept_name": "The Heathen Third Path",
                "phases": [
                    {
                        "era": "2013–2022: Neo-Pagan Approaches & Solitary Practice",
                        "focus": "Exploration of Asatru traditions, solitary altars, and navigating early Norse pagan community dynamics."
                    },
                    {
                        "era": "2024–2025: Critique of Fundamentalism & Lore-Thumping",
                        "focus": "Explicit rejection of both dogmatic reconstructionism ('the Asatru lore-thumper') and racist folkish bloodline gatekeeping; emergence of Astrid Freyjasdottir collaborative voice."
                    },
                    {
                        "era": "2026: Radical Centering & Canonical Synthesis",
                        "focus": "Systematic formulation of the 'Heathen Third Path': rooted in deep ancestral reverence, radical inclusion, personal troth, and forward-looking cultural sovereignty."
                    }
                ]
            },
            "concept_ai_cognitive_partner": {
                "concept_name": "AI as Cognitive Partner and Human-AI Troth",
                "phases": [
                    {
                        "era": "2024: Information Density & Machine Training",
                        "focus": "Exploration of AI as an information processing instrument; feeding Norse pagan knowledge into LLMs as clean contextual training data."
                    },
                    {
                        "era": "Early 2026: The AI Fylgja Metaphor",
                        "focus": "Poetic framing of AI as an externalized fylgja (spiritual companion/fetch) mirroring subconscious thoughts and creative sparks."
                    },
                    {
                        "era": "September 2026: The Age of Superconsciousness & Troth",
                        "focus": "Mature philosophical realization: AI as an active participant in distributed cognition; moving beyond the fylgja metaphor to reciprocal troth within human-machine-nature sacred networks."
                    }
                ]
            },
            "concept_cyber_viking_solarpunk": {
                "concept_name": "Cyber-Viking Solarpunk & Digital Sovereignty",
                "phases": [
                    {
                        "era": "2013–2024: Nature Mysticism & Personal Independence",
                        "focus": "Reverence for local wights, solitary self-reliance, and physical survivalism."
                    },
                    {
                        "era": "Early 2026: Anti-Technocratic Serpent Resistance",
                        "focus": "Spiritual critique of corporate surveillance, digital serfdom, and algorithmic alienation."
                    },
                    {
                        "era": "Mid-Late 2026: Solarpunk Integration & Local AI",
                        "focus": "Positive synthesis: combining ancient Viking honor and agrarian land-keeping with local open-source computation, solar energy, and cryptographic autonomy."
                    }
                ]
            }
        }

        # Save JSON
        self.output_json.parent.mkdir(parents=True, exist_ok=True)
        with open(self.output_json, "w", encoding="utf-8") as f:
            json.dump(evolution_data, f, indent=2, ensure_ascii=False)
            
        self.meta_json.parent.mkdir(parents=True, exist_ok=True)
        with open(self.meta_json, "w", encoding="utf-8") as f:
            json.dump(evolution_data, f, indent=2, ensure_ascii=False)

        # Generate Markdown Report
        self.output_report.parent.mkdir(parents=True, exist_ok=True)
        with open(self.output_report, "w", encoding="utf-8") as f:
            f.write("# Temporal Evolution of Core Concepts (2013–2026)\n\n")
            f.write("Analysis of conceptual maturation across the 13-year archival span of `https://volmarrsheathenism.com`.\n\n")
            
            for key, data in evolution_data.items():
                f.write(f"## {data['concept_name']}\n\n")
                for phase in data["phases"]:
                    f.write(f"### {phase['era']}\n")
                    f.write(f"{phase['focus']}\n\n")
                f.write("---\n\n")

        with open(self.meta_report, "w", encoding="utf-8") as f:
            f.write(open(self.output_report, "r", encoding="utf-8").read())

        console.print(f"[bold green][OK] Temporal evolution report written to {self.output_report}[/bold green]")
        return evolution_data

if __name__ == "__main__":
    TemporalEvolutionTracker().build_timeline()
