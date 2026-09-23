"""Book Generation Engine (Milestone 6 & Phase 33/40).
Compiles the entire canonical knowledge base into a single, publication-ready,
topologically-ordered book volume: `dist/The_Heathen_Third_Path_Canonical_System.md`.
"""

import json
import re
from pathlib import Path
from rich.console import Console

console = Console()

class BookGenerator:
    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir)
        self.knowledge_dir = self.root_dir / "knowledge"
        self.db_dir = self.root_dir / "data" / "database"
        self.dist_dir = self.root_dir / "dist"
        self.dist_dir.mkdir(parents=True, exist_ok=True)
        self.output_md = self.dist_dir / "The_Heathen_Third_Path_Canonical_System.md"
        self.graph_file = self.db_dir / "prerequisite_graph.json"
        self.glossary_file = self.knowledge_dir / "00_GLOSSARY.md"

    @staticmethod
    def slugify(title: str) -> str:
        return re.sub(r"[^\w\- ]", "", title).strip().lower().replace(" ", "-")

    def generate_book(self) -> Path:
        console.print("[bold cyan]Compiling Canonical Opus into single volume...[/bold cyan]")
        
        if not self.graph_file.exists():
            raise FileNotFoundError(f"Prerequisite graph not found at {self.graph_file}")

        with open(self.graph_file, "r", encoding="utf-8") as f:
            graph_data = json.load(f)

        reading_order = graph_data["topological_reading_order"]

        # Map slug to markdown file
        slug_to_file = {}
        for md_path in self.knowledge_dir.rglob("*.md"):
            if "_meta" in md_path.parts or md_path.name.startswith("00_"):
                continue
            # Extract concept slug from file text or name
            text = md_path.read_text(encoding="utf-8")
            title_match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
            title = title_match.group(1).strip() if title_match else md_path.stem
            slug_to_file[md_path.stem] = (title, md_path, text)
            # Also map by sanitized slug
            clean_stem = re.sub(r"^\d+_", "", md_path.stem).lower()
            slug_to_file[clean_stem] = (title, md_path, text)

        lines = []
        
        # Front Matter
        lines.append("# The Heathen Third Path: A Canonical Synthesis")
        lines.append("\n**Author:** Synthesized from the writings of Volmarr and named collaborative voices")
        lines.append("**Source Corpus:** `https://volmarrsheathenism.com` (2013–2026)")
        lines.append("**Architecture:** Ordered strictly by conceptual dependency (Cycle-Free Topological DAG)")
        lines.append("**Format:** Single-Volume Canonical Edition\n")
        lines.append("---\n")

        # Foreword
        lines.append("## Foreword & Epistemic Orientation\n")
        lines.append(
            "This book is not a blog archive or chronological scrapbook. It is a distilled conceptual memory. "
            "Every concept within this volume has one canonical home, arranged so that foundational ideas "
            "provide the necessary prerequisites for deeper metaphysics, ethics, magick, and modern cybernetic synthesis.\n"
        )
        lines.append(
            "The reader is invited to walk this path from the primal relational axiom—*Nothing becomes alone*—through "
            "the sacred bonds of troth, frith, and the Holy Powers, onward into the Elder Futhark and Seiðr, "
            "and finally to the contemporary frontier of Cyber-Viking solarpunk, AI companionship, and the living Tree of Becoming.\n"
        )
        lines.append("---\n")

        # Table of Contents
        lines.append("## Table of Contents\n")
        lines.append("1. [Foreword & Epistemic Orientation](#foreword--epistemic-orientation)")
        
        current_tier = None
        chapter_num = 1
        for item in reading_order:
            tier = item["taxonomy_level"]
            tier_display = tier.replace("_", " ").title()
            if tier != current_tier:
                lines.append(f"\n### {tier_display}\n")
                current_tier = tier
            
            c_name = item["canonical_name"]
            c_slug = self.slugify(f"chapter-{chapter_num}-{c_name}")
            lines.append(f"- [Chapter {chapter_num}: {c_name}](#{c_slug})")
            chapter_num += 1

        lines.append("\n### Appendices\n")
        lines.append("- [Appendix A: Complete Glossary of Terms](#appendix-a-complete-glossary-of-terms)")
        lines.append("- [Appendix B: Prerequisite Graph & Reading Paths](#appendix-b-prerequisite-graph--reading-paths)")
        lines.append("\n---\n")

        # Chapters
        chapter_num = 1
        current_tier = None
        for item in reading_order:
            tier = item["taxonomy_level"]
            tier_display = tier.replace("_", " ").title()
            c_slug = item["slug"]
            c_name = item["canonical_name"]
            
            if tier != current_tier:
                lines.append(f"\n# Part {tier[:2]}: {tier_display}\n")
                lines.append(f"*Foundational concepts governing {tier_display.lower()}.*\n\n---\n")
                current_tier = tier

            # Find matching file content
            found = False
            for key, (t_title, t_path, t_content) in slug_to_file.items():
                if c_slug in key or key in c_slug or self.slugify(c_name) in self.slugify(t_title):
                    lines.append(f"\n## Chapter {chapter_num}: {c_name}\n")
                    # Strip the original H1 title to avoid duplicate headers
                    body = re.sub(r"^#\s+[^\n]+\n", "", t_content).strip()
                    # Rewrite relative markdown links to local chapter anchors
                    body_linked = re.sub(r"\[([^\]]+)\]\(\.\./[^\)]+\.md\)", r"*\1*", body)
                    lines.append(body_linked)
                    lines.append("\n\n---\n")
                    found = True
                    break
                    
            if not found:
                lines.append(f"\n## Chapter {chapter_num}: {c_name}\n")
                lines.append(f"*{item.get('definition_short', '')}*\n\n---\n")
                
            chapter_num += 1

        # Appendix A: Glossary
        lines.append("\n# Appendix A: Complete Glossary of Terms\n")
        if self.glossary_file.exists():
            glossary_text = self.glossary_file.read_text(encoding="utf-8")
            glossary_body = re.sub(r"^#\s+[^\n]+\n", "", glossary_text).strip()
            # Rewrite relative links
            glossary_clean = re.sub(r"\[([^\]]+)\]\(\./[^\)]+\.md\)", r"**\1**", glossary_body)
            lines.append(glossary_clean)
        else:
            lines.append("*Glossary data compiled from canonical definitions.*")
        lines.append("\n\n---\n")

        # Appendix B: Graph Summary
        lines.append("\n# Appendix B: Prerequisite Graph & Reading Paths\n")
        lines.append("The 25 concepts in this volume form a strictly cycle-free Directed Acyclic Graph (DAG):\n")
        lines.append("- **Total Concept Nodes:** 25")
        lines.append(f"- **Total Directed Dependency Edges:** {len(graph_data.get('edges', []))}")
        lines.append("- **Topological Ordering:** Computed using Kahn's algorithm, guaranteeing zero prerequisite violations.\n")
        lines.append("### Foundational Reading Paths")
        lines.append("1. **Foundational Heathen Path:** Relational Worldview → Troth and Reciprocity → Frith and Hospitality → Blót and Daily Practice")
        lines.append("2. **Modern Viking & Sovereignty Path:** Relational Worldview → Troth → Personal Sovereignty → Heathen Third Path → Cyber-Viking Solarpunk")
        lines.append("3. **Cosmological & Mystical Path:** Relational Worldview → Ancestors → Wyrd and Orlaeg → Galdr & Seiðr → Cyber-Mysticism")
        lines.append("4. **Digital Solarpunk & AI Troth:** Personal Sovereignty → Solarpunk → AI as Cognitive Partner → The Age of Superconsciousness\n")

        # Write output file
        content = "\n".join(lines)
        self.output_md.write_text(content, encoding="utf-8")
        console.print(f"[bold green][OK] Master canonical book generated: {self.output_md} ({len(content.splitlines())} lines)[/bold green]")
        return self.output_md

if __name__ == "__main__":
    BookGenerator().generate_book()
