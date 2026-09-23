"""Safe Merge Algorithm (Phase 31).
Implements conservative semantic deduplication:
- Candidate retrieval via lexical/semantic similarity
- Relational decision modeling (SAME, OVERLAPPING, EVOLUTION_OF, CONTRADICTORY, NEW_CONCEPT)
- Conservative provenance union and human review queue dispatching
"""

import re
import json
from dataclasses import dataclass
from pathlib import Path
from rich.console import Console

console = Console()

@dataclass
class MergeDecision:
    label: str          # SAME, OVERLAPPING, EVOLUTION_OF, CONTRADICTORY, NEW_CONCEPT
    confidence: float
    target_concept_id: str | None
    reason: str

class SafeMergeEngine:
    SAME_THRESHOLD = 0.80
    OVERLAP_THRESHOLD = 0.40
    TENSION_THRESHOLD = 0.30

    def __init__(self, db_dir: str = "data/database"):
        self.db_dir = Path(db_dir)
        self.registry_file = self.db_dir / "concept_registry.jsonl"
        self.claims_file = self.db_dir / "source_claims.jsonl"
        self.clusters_file = self.db_dir / "duplicate_clusters.jsonl"

    @staticmethod
    def word_set(text: str) -> set[str]:
        return set(re.findall(r"\w+", text.lower()))

    def compute_similarity(self, text1: str, text2: str) -> float:
        w1 = self.word_set(text1)
        w2 = self.word_set(text2)
        if not w1 or not w2:
            return 0.0
        return len(w1 & w2) / len(w1 | w2)

    def retrieve_candidates(self, claim_text: str, concepts: list[dict], top_k: int = 5) -> list[tuple[float, dict]]:
        """Finds candidate concepts using word-set Jaccard overlap."""
        candidates = []
        for c in concepts:
            concept_corpus = f"{c['canonical_name']} {c['definition_short']} " + " ".join(c.get("core_principles", []))
            sim = self.compute_similarity(claim_text, concept_corpus)
            if sim > 0.05:
                candidates.append((sim, c))
                
        candidates.sort(key=lambda x: x[0], reverse=True)
        return candidates[:top_k]

    def evaluate_relation(self, claim: dict, candidate: dict, similarity: float) -> MergeDecision:
        """Determines semantic relationship between claim and concept."""
        stmt = claim["statement"].lower()
        targets = [p.lower() for p in candidate.get("core_principles", [])]
        if candidate.get("definition_short"):
            targets.append(candidate["definition_short"].lower())
            
        principle_sims = [self.compute_similarity(stmt, t) for t in targets] if targets else [0.0]
        max_p_sim = max(principle_sims) if principle_sims else 0.0

        # 1. Exact or near-identical to an existing core principle
        if max_p_sim >= self.SAME_THRESHOLD:
            best_idx = principle_sims.index(max_p_sim)
            return MergeDecision(
                label="SAME",
                confidence=max_p_sim,
                target_concept_id=candidate["concept_id"],
                reason=f"High similarity ({max_p_sim:.2f}) with principle: '{targets[best_idx][:60]}...'"
            )

        # 2. Check for contradiction indicators
        negation_markers = ["not ", "never ", "rejects ", "opposes ", "false ", "distortion ", "illusion "]
        has_negation = any(m in stmt for m in negation_markers)
        if has_negation and (max_p_sim >= self.TENSION_THRESHOLD or similarity >= self.TENSION_THRESHOLD):
            return MergeDecision(
                label="CONTRADICTORY",
                confidence=max(max_p_sim, similarity),
                target_concept_id=candidate["concept_id"],
                reason=f"Claim expresses potential tension or negation relative to {candidate['canonical_name']}"
            )

        # 3. Check for temporal/evolution indicators
        evolution_markers = ["mature", "later", "evolution", "earlier", "previously", "develops beyond", "superconsciousness"]
        has_evolution = any(m in stmt for m in evolution_markers)
        if has_evolution and (max_p_sim >= self.OVERLAP_THRESHOLD or similarity >= 0.25):
            return MergeDecision(
                label="EVOLUTION_OF",
                confidence=max(max_p_sim, similarity),
                target_concept_id=candidate["concept_id"],
                reason=f"Chronological development or theoretical expansion of {candidate['canonical_name']}"
            )

        # 4. Overlapping nuance
        if max_p_sim >= self.OVERLAP_THRESHOLD or similarity >= 0.25:
            return MergeDecision(
                label="OVERLAPPING",
                confidence=max(max_p_sim, similarity),
                target_concept_id=candidate["concept_id"],
                reason=f"Shares core vocabulary and domain with {candidate['canonical_name']}"
            )

        # 5. Otherwise new/distinct
        return MergeDecision(
            label="NEW_CONCEPT",
            confidence=1.0 - max(max_p_sim, similarity),
            target_concept_id=None,
            reason="Insufficient overlap with existing canonical concepts"
        )

    def process_incoming_claim(self, claim: dict, concepts: list[dict]) -> tuple[MergeDecision, str]:
        candidates = self.retrieve_candidates(claim["statement"], concepts, top_k=5)
        if not candidates:
            return MergeDecision("NEW_CONCEPT", 1.0, None, "No candidate match found"), "create_new"
            
        sim, best_candidate = candidates[0]
        decision = self.evaluate_relation(claim, best_candidate, sim)
        
        if decision.label == "SAME":
            return decision, "merge_provenance"
        elif decision.label == "OVERLAPPING":
            return decision, "append_nuance"
        elif decision.label == "EVOLUTION_OF":
            return decision, "record_evolution"
        elif decision.label == "CONTRADICTORY":
            return decision, "queue_for_review"
        else:
            return decision, "create_new"

if __name__ == "__main__":
    engine = SafeMergeEngine()
    test_claim = {
        "statement": "Nothing becomes alone in the sacred web of the Heathen universe.",
        "concept_name": "relational_worldview"
    }
    sample_concepts = [
        {
            "concept_id": "concept_relational_worldview",
            "canonical_name": "Relational Worldview",
            "definition_short": "Nothing becomes alone: all beings exist in a reciprocal web.",
            "core_principles": ["Nothing becomes alone.", "Reciprocal kinship unites gods and humans."]
        }
    ]
    dec, action = engine.process_incoming_claim(test_claim, sample_concepts)
    print(f"Decision: {dec.label} (confidence: {dec.confidence:.2f}) -> Action: {action}")
