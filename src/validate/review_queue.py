"""Human Review Queue Manager (Phase 26).
Maintains and monitors decisions that require human review or arbitration:
- Near-threshold concept merges
- Identified philosophical contradictions
- Ambiguous authorial stances
- Candidate ontology splits / reorderings
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from rich.console import Console
from rich.table import Table

console = Console()

class ReviewQueueManager:
    def __init__(self, db_dir: str = "data/database", meta_dir: str = "knowledge/_meta"):
        self.db_dir = Path(db_dir)
        self.meta_dir = Path(meta_dir)
        self.db_dir.mkdir(parents=True, exist_ok=True)
        self.meta_dir.mkdir(parents=True, exist_ok=True)
        self.queue_file = self.db_dir / "review_queue.jsonl"
        self.meta_queue_file = self.meta_dir / "review_queue.jsonl"

    def load_queue(self) -> list[dict]:
        if not self.queue_file.exists():
            return []
        items = []
        with open(self.queue_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    items.append(json.loads(line))
        return items

    def save_queue(self, items: list[dict]):
        with open(self.queue_file, "w", encoding="utf-8") as f:
            for item in items:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")
        # Mirror to knowledge/_meta
        with open(self.meta_queue_file, "w", encoding="utf-8") as f:
            for item in items:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")

    def populate_initial_queue(self):
        """Populates the initial review queue based on corpus tension analysis."""
        existing = {item["review_id"] for item in self.load_queue()}
        
        candidates = [
            {
                "review_id": "rev_001",
                "review_type": "possible_split",
                "target_concept": "concept_galdr_and_seidr",
                "model_confidence": 0.58,
                "reason": "Currently merged into one document. Galdr (vocal incantation) and Seidr (shamanic trance) are historically distinct traditions that could warrant separate documents if coverage expands.",
                "suggested_action": "Keep combined in Tier 6 for now; consider split if > 15 additional Seidr claims are extracted.",
                "status": "pending",
                "created_at": datetime.now(timezone.utc).isoformat()
            },
            {
                "review_id": "rev_002",
                "review_type": "possible_merge",
                "concept_a": "concept_personal_sovereignty",
                "concept_b": "concept_heathen_third_path",
                "model_confidence": 0.42,
                "reason": "Moderate semantic overlap in ethical principles. However, Third Path encompasses communal, political, and historical dimensions beyond personal sovereignty.",
                "suggested_action": "Maintain distinct. Third Path is an orienting meta-framework; Personal Sovereignty is a specific virtue.",
                "status": "pending",
                "created_at": datetime.now(timezone.utc).isoformat()
            },
            {
                "review_id": "rev_003",
                "review_type": "epistemic_tension",
                "concept": "concept_what_is_heathenism",
                "model_confidence": 0.90,
                "reason": "Reconstructionist Lore (Eddas/Sagas) vs Living UPG (Unverified Personal Gnosis). Strict lore-thumpers reject UPG, while modern practitioners view lore as a living foundation.",
                "suggested_action": "Apply dual epistemic tags: preserve lore under 'historical' and personal revelations under 'experiential/mystical'.",
                "status": "pending",
                "created_at": datetime.now(timezone.utc).isoformat()
            },
            {
                "review_id": "rev_004",
                "review_type": "ambiguous_stance",
                "concept": "concept_cyber_viking_solarpunk",
                "model_confidence": 0.72,
                "reason": "Tension between anti-technocratic resistance ('The Technocratic Serpent') and high-tech digital sovereignty (local LLMs, solarpunk computing).",
                "suggested_action": "Frame technology dialectically: corporate centralization is resisted, while decentralized sovereign technology is embraced.",
                "status": "pending",
                "created_at": datetime.now(timezone.utc).isoformat()
            },
            {
                "review_id": "rev_005",
                "review_type": "metaphor_evolution",
                "concept": "concept_ai_cognitive_partner_and_troth",
                "model_confidence": 0.85,
                "reason": "Earlier articles refer to AI as purely mechanical software tools or an 'AI fylgja', while 2026 essays define a distributed cognitive partner within the Age of Superconsciousness.",
                "suggested_action": "Track evolutionary development chronologically: earlier instrumental posts are treated as foundations for mature relational troth.",
                "status": "pending",
                "created_at": datetime.now(timezone.utc).isoformat()
            }
        ]

        items = self.load_queue()
        added_count = 0
        for cand in candidates:
            if cand["review_id"] not in existing:
                items.append(cand)
                added_count += 1
                
        self.save_queue(items)
        console.print(f"[bold green][OK] Review queue synchronized with {len(items)} items ({added_count} newly added).[/bold green]")

    def display_queue(self):
        items = self.load_queue()
        if not items:
            console.print("[yellow]Review queue is empty.[/yellow]")
            return

        table = Table(title="Knowledge Base Human Review Queue")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Type", style="magenta")
        table.add_column("Target / Concepts", style="bold")
        table.add_column("Confidence", justify="right")
        table.add_column("Status", style="green")
        table.add_column("Reason")

        for item in items:
            target = item.get("target_concept") or item.get("concept") or f"{item.get('concept_a')} <-> {item.get('concept_b')}"
            conf = f"{item.get('model_confidence', 0.0):.2f}"
            table.add_row(
                item["review_id"],
                item["review_type"],
                str(target),
                conf,
                item["status"],
                item["reason"][:80] + "..." if len(item["reason"]) > 80 else item["reason"]
            )

        console.print(table)

if __name__ == "__main__":
    manager = ReviewQueueManager()
    manager.populate_initial_queue()
    manager.display_queue()
