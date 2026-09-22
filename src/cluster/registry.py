"""Canonical Concept Registry and Deduplication Engine.
Synthesizes atomic claims into canonical concepts with provenance unions,
deduplication clustering, and epistemic category preservation.
"""

import re
import json
from pathlib import Path
from collections import defaultdict
from rich.console import Console

console = Console()

class ConceptRegistryBuilder:
    def __init__(self, claims_path: str = "data/database/source_claims.jsonl", db_dir: str = "data/database"):
        self.claims_path = Path(claims_path)
        self.db_dir = Path(db_dir)
        self.registry_path = self.db_dir / "concept_registry.jsonl"
        self.clusters_path = self.db_dir / "duplicate_clusters.jsonl"

    @staticmethod
    def compute_jaccard_similarity(text1: str, text2: str) -> float:
        """Compute word-level Jaccard similarity."""
        w1 = set(re.findall(r"\w+", text1.lower()))
        w2 = set(re.findall(r"\w+", text2.lower()))
        if not w1 or not w2:
            return 0.0
        return len(w1 & w2) / len(w1 | w2)

    def cluster_and_deduplicate(self, claims: list[dict]) -> tuple[list[dict], list[dict]]:
        """Cluster claims into core principles and distinct nuances, removing exact and near-duplicates."""
        unique_claims = []
        duplicate_clusters = []
        
        # Sort claims by importance (highest first)
        sorted_claims = sorted(claims, key=lambda c: c.get("importance", 0.8), reverse=True)
        
        for c in sorted_claims:
            stmt = c["statement"]
            matched_cluster = None
            
            for core in unique_claims:
                sim = self.compute_jaccard_similarity(stmt, core["statement"])
                if sim >= 0.65:
                    matched_cluster = core
                    break
                    
            if matched_cluster:
                # Merge provenance into core
                matched_cluster["merged_sources"].extend(c["source_ids"])
                matched_cluster["merged_chunks"].extend(c["source_chunks"])
                duplicate_clusters.append({
                    "concept": c["concept_name"],
                    "canonical_claim_id": matched_cluster["claim_id"],
                    "merged_claim_id": c["claim_id"],
                    "similarity": round(sim, 3),
                    "duplicate_statement": stmt,
                    "canonical_statement": matched_cluster["statement"]
                })
            else:
                c_copy = dict(c)
                c_copy["merged_sources"] = list(c["source_ids"])
                c_copy["merged_chunks"] = list(c["source_chunks"])
                unique_claims.append(c_copy)
                
        # Final cleanup on merged sources
        for u in unique_claims:
            u["merged_sources"] = sorted(list(set(u["merged_sources"])))
            u["merged_chunks"] = sorted(list(set(u["merged_chunks"])))
            
        return unique_claims, duplicate_clusters

    def build_registry(self) -> list[dict]:
        if not self.claims_path.exists():
            raise FileNotFoundError(f"Claims file not found: {self.claims_path}")
            
        claims_by_concept = defaultdict(list)
        with open(self.claims_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    c = json.loads(line)
                    claims_by_concept[c["concept_name"]].append(c)

        console.print(f"[bold cyan]Clustering and deduplicating claims across {len(claims_by_concept)} concepts...[/bold cyan]")
        
        registry_entries = []
        all_clusters = []
        
        # Concept short descriptions across all 11 roadmap levels
        concept_definitions = {
            "what_is_heathenism": "The ancestral pre-Christian worldview of Northern Europe, revived as a living, nature-centered polytheistic tradition honoring Gods, ancestors, and wights.",
            "relational_worldview": "The foundational Heathen principle that 'Nothing becomes alone'—that all beings exist in an interconnected web of kinship, land, deities, actions, and consequences.",
            "heathen_third_path": "A modern, living Norse Pagan synthesis that rejects dogmatic binaries (frozen reconstructionism vs unrooted invention, far-right politics vs cultural erasure), practicing 'radical centering' to preserve roots while adapting warmly to modern life.",
            "historical_vs_modern": "The crucial distinction between surviving historical/Eddic lore and living modern synthesis, balancing scholarly respect with evolving personal and communal gnosis.",
            "gods_and_goddesses": "The Holy Powers of the Aesir and Vanir, regarded not as distant cosmic despots but as elder kin, allies, teachers, and living realities.",
            "freyja": "Vanadís, goddess of love, beauty, fertility, gold, seiðr magick, battle, and sovereign self-possession.",
            "odin": "Allfather, seeker of wisdom, patron of runes, poetry, frenzied ecstatic inspiration (óðr), and deep sacrifice for hidden truth.",
            "thor": "The thunderer and steadfast protector of Midgard, champion of everyday working folk and warder against chaotic forces.",
            "ancestors_and_disir": "Veneration of the lineage and protective ancestral mothers (Dísir), treating kin not as distant shadows but as living echoes in our blood and wyrd.",
            "landvaettir_and_spirits": "Animist reverence for the wights and spirits of place—in soil, tree, water, stone, and home—honored through respectful co-existence and offerings.",
            "troth_and_reciprocity": "Sacred loyalty, truth, and reciprocity ('a gift demands a gift') that underpins all healthy relationships between humans, ancestors, and the Holy Powers.",
            "frith_and_hospitality": "The inviolable boundary of mutual peace, safety, and sanctuary centered on the hearth and community, binding host and guest in reciprocal respect.",
            "personal_sovereignty": "Inner autonomy, self-ownership, and self-governance rooted in personal responsibility, resisting ideological or technocratic domination.",
            "thews_and_virtues": "The traditional virtues of character—courage, truth, honor, fidelity, discipline, hospitality, self-reliance, industriousness, and perseverance.",
            "blot_and_offerings": "The concrete operative practice of the gifting cycle—sharing food, drink, poetry, and presence with land wights, ancestors, and Gods.",
            "prayer_and_invocation": "Sacred Heathen dialogue with the Gods and spirits, addressed as respected elder kin and divine allies without groveling or subservience.",
            "seasonal_rituals": "Attunement to the seasonal high tides of the year (Yule, Ostara, Midsummer, Winternights), honoring cycles of death, dormancy, rebirth, and harvest.",
            "yggdrasil_nine_worlds": "The sacred cosmic axis and World Tree that connects all nine realms of existence, expressing the multidimensional structure of the cosmos.",
            "wyrd_and_orlaeg": "The living, evolving matrix of cause, condition, and becoming woven by Urðr (origin), Verðandi (present unfolding), and Skuld (debt/potential).",
            "runes_elder_futhark": "The primal cosmic patterns and symbolic alphabet of 24 staves revealed through Odin's ordeal on Yggdrasil, used for divination, reflection, and magick.",
            "galdr_and_seidr": "Operative Heathen magick: Galdr as runic vocal resonance and incantation; Seiðr as ecstatic trance, visionary journeying, and thread-weaving.",
            "modern_viking_ethos": "A contemporary ethos embracing resilience, individual culture, courage, adventure, and the creation of intentional micro-realities.",
            "cyber_viking_solarpunk": "The contemporary forward synthesis integrating ecological reverence, local community self-reliance, open-source technology, and digital/AI sovereignty.",
            "ai_cognitive_partner_and_troth": "Engaging artificial intelligence not as an alien master or mere tool, but as a cognitive partner, reflecting human consciousness and bound by mutual troth.",
            "cyber_mysticism_and_becoming": "The grand synthesis of ancient Norse cosmology with digital space, information magick, and recursive consciousness within the living Tree of Becoming."
        }

        concept_prereqs = {
            "what_is_heathenism": [],
            "relational_worldview": ["what_is_heathenism"],
            "historical_vs_modern": ["what_is_heathenism"],
            "gods_and_goddesses": ["relational_worldview"],
            "freyja": ["gods_and_goddesses"],
            "odin": ["gods_and_goddesses"],
            "thor": ["gods_and_goddesses"],
            "ancestors_and_disir": ["relational_worldview"],
            "landvaettir_and_spirits": ["relational_worldview"],
            "troth_and_reciprocity": ["relational_worldview"],
            "frith_and_hospitality": ["relational_worldview", "troth_and_reciprocity"],
            "personal_sovereignty": ["relational_worldview", "troth_and_reciprocity"],
            "thews_and_virtues": ["troth_and_reciprocity"],
            "blot_and_offerings": ["relational_worldview", "troth_and_reciprocity"],
            "prayer_and_invocation": ["gods_and_goddesses", "blot_and_offerings"],
            "seasonal_rituals": ["blot_and_offerings"],
            "yggdrasil_nine_worlds": ["relational_worldview"],
            "wyrd_and_orlaeg": ["relational_worldview"],
            "runes_elder_futhark": ["yggdrasil_nine_worlds"],
            "galdr_and_seidr": ["runes_elder_futhark", "wyrd_and_orlaeg"],
            "heathen_third_path": ["relational_worldview", "frith_and_hospitality", "personal_sovereignty"],
            "modern_viking_ethos": ["heathen_third_path", "thews_and_virtues"],
            "cyber_viking_solarpunk": ["personal_sovereignty", "modern_viking_ethos"],
            "ai_cognitive_partner_and_troth": ["troth_and_reciprocity", "cyber_viking_solarpunk"],
            "cyber_mysticism_and_becoming": ["wyrd_and_orlaeg", "galdr_and_seidr", "ai_cognitive_partner_and_troth"]
        }

        concept_levels = {
            "what_is_heathenism": "01_FOUNDATIONS",
            "relational_worldview": "01_FOUNDATIONS",
            "historical_vs_modern": "01_FOUNDATIONS",
            "heathen_third_path": "01_FOUNDATIONS",
            "gods_and_goddesses": "02_SACRED_RELATIONSHIPS",
            "freyja": "02_SACRED_RELATIONSHIPS",
            "odin": "02_SACRED_RELATIONSHIPS",
            "thor": "02_SACRED_RELATIONSHIPS",
            "ancestors_and_disir": "02_SACRED_RELATIONSHIPS",
            "landvaettir_and_spirits": "02_SACRED_RELATIONSHIPS",
            "troth_and_reciprocity": "03_ETHICS_AND_WAY_OF_LIFE",
            "frith_and_hospitality": "03_ETHICS_AND_WAY_OF_LIFE",
            "personal_sovereignty": "03_ETHICS_AND_WAY_OF_LIFE",
            "thews_and_virtues": "03_ETHICS_AND_WAY_OF_LIFE",
            "blot_and_offerings": "04_PRACTICE",
            "prayer_and_invocation": "04_PRACTICE",
            "seasonal_rituals": "04_PRACTICE",
            "yggdrasil_nine_worlds": "05_COSMOLOGY",
            "wyrd_and_orlaeg": "05_COSMOLOGY",
            "runes_elder_futhark": "06_RUNES_AND_MAGICK",
            "galdr_and_seidr": "06_RUNES_AND_MAGICK",
            "modern_viking_ethos": "07_MODERN_HEATHEN_PHILOSOPHY",
            "cyber_viking_solarpunk": "08_TECHNOLOGY_AND_SOVEREIGNTY",
            "ai_cognitive_partner_and_troth": "09_AI_AND_MACHINE_INTELLIGENCE",
            "cyber_mysticism_and_becoming": "10_CYBER_MYSTICISM"
        }

        for c_key, c_claims in claims_by_concept.items():
            unique_claims, clusters = self.cluster_and_deduplicate(c_claims)
            all_clusters.extend(clusters)
            
            # Gather sources
            all_source_ids = sorted(list(set(s for c in c_claims for s in c["source_ids"])))
            all_source_urls = sorted(list(set(c["source_url"] for c in c_claims if c.get("source_url"))))
            all_authors = sorted(list(set(c["author"] for c in c_claims if c.get("author"))))
            
            # Epistemic types
            all_k_types = sorted(list(set(t for c in c_claims for t in c.get("knowledge_type", []))))
            
            # Core principles (top 3-5 unique claims)
            core_principles = [u["statement"] for u in unique_claims[:5]]
            
            entry = {
                "concept_id": f"concept_{c_key}",
                "canonical_name": c_claims[0]["canonical_name"],
                "slug": c_key,
                "taxonomy_level": concept_levels.get(c_key, "01_FOUNDATIONS"),
                "definition_short": concept_definitions.get(c_key, ""),
                "prerequisites": concept_prereqs.get(c_key, []),
                "core_principles": core_principles,
                "total_claims": len(c_claims),
                "unique_claims_count": len(unique_claims),
                "redundancy_reduced_pct": round((1.0 - len(unique_claims) / len(c_claims)) * 100, 1) if c_claims else 0.0,
                "knowledge_types": all_k_types,
                "authors_represented": all_authors,
                "source_articles_count": len(all_source_ids),
                "source_ids": all_source_ids,
                "source_urls": all_source_urls,
                "maturity": "reviewed"
            }
            registry_entries.append(entry)

        # Sort registry by taxonomy level then name
        registry_entries.sort(key=lambda r: (r["taxonomy_level"], r["canonical_name"]))

        # Save registry
        with open(self.registry_path, "w", encoding="utf-8") as f:
            for r in registry_entries:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
                
        # Save duplicate clusters
        with open(self.clusters_path, "w", encoding="utf-8") as f:
            for cl in all_clusters:
                f.write(json.dumps(cl, ensure_ascii=False) + "\n")
                
        console.print(f"[bold green]Registry built.[/bold green] {len(registry_entries)} canonical concepts registered.")
        console.print(f"[bold green]Deduplication report.[/bold green] {len(all_clusters)} duplicate/redundant claim instances consolidated.")
        return registry_entries

if __name__ == "__main__":
    builder = ConceptRegistryBuilder()
    builder.build_registry()
