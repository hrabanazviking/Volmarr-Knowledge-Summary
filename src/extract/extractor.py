"""Atomic Knowledge Extraction Module.
Extracts structured, atomic claims from semantic chunks with source provenance,
epistemic knowledge classification, and candidate prerequisites.
"""

import re
import json
import hashlib
from pathlib import Path
from rich.console import Console

console = Console()

# Defined knowledge types from roadmap Phase 3
KNOWLEDGE_TYPES = [
    "historical",
    "reconstruction",
    "modern_heathen_practice",
    "personal_practice",
    "theology",
    "devotional",
    "philosophical",
    "mystical",
    "experiential",
    "speculative",
    "metaphorical",
    "technological",
    "political_or_social_commentary",
    "creative_mythmaking",
    "ritual_instruction"
]

# Concept extraction patterns & definitions across all 11 roadmap levels
CONCEPT_PATTERNS = {
    # Level 1: Foundations
    "what_is_heathenism": {
        "canonical_name": "Heathenism and Norse Paganism",
        "keywords": ["heathenism", "norse paganism", "asatru", "vanatru", "living tradition", "polytheism", "pagan elder", "intro to heathenism"],
        "default_types": ["theology", "historical", "modern_heathen_practice"],
        "prerequisites": []
    },
    "relational_worldview": {
        "canonical_name": "Relational Worldview",
        "keywords": ["nothing becomes alone", "relational", "interconnected", "web of relationships", "allies", "reciprocal bond", "not isolated", "sacred relationship"],
        "default_types": ["philosophical", "theology", "modern_heathen_practice"],
        "prerequisites": ["what_is_heathenism"]
    },
    "heathen_third_path": {
        "canonical_name": "Heathen Third Path",
        "keywords": ["third path", "radical centering", "neither far-right", "neither rigid", "conserve the sacred", "rebel step", "refuse binary", "binary battle"],
        "default_types": ["philosophical", "modern_heathen_practice", "political_or_social_commentary"],
        "prerequisites": ["relational_worldview", "frith_and_hospitality", "personal_sovereignty"]
    },
    "historical_vs_modern": {
        "canonical_name": "Historical Tradition and Modern Synthesis",
        "keywords": ["living history", "historical reconstruction", "modern synthesis", "unverified personal gnosis", "upg", "lore", "sagas", "eddas"],
        "default_types": ["historical", "philosophical", "reconstruction"],
        "prerequisites": ["what_is_heathenism"]
    },

    # Level 2: Sacred Relationships
    "gods_and_goddesses": {
        "canonical_name": "Gods and Goddesses",
        "keywords": ["aesir", "vanir", "holy powers", "divine", "gods and goddesses", "deities", "polytheist", "pantheon"],
        "default_types": ["theology", "devotional", "modern_heathen_practice"],
        "prerequisites": ["relational_worldview"]
    },
    "freyja": {
        "canonical_name": "Freyja",
        "keywords": ["freyja", "freya", "vanadis", "brisingamen", "sessrumnir", "folkvangr", "lady of the vanir"],
        "default_types": ["theology", "devotional", "mystical"],
        "prerequisites": ["gods_and_goddesses"]
    },
    "odin": {
        "canonical_name": "Odin",
        "keywords": ["odin", "allfather", "woden", "huginn", "muninn", "valknut", "wanderer", "hangatyr"],
        "default_types": ["theology", "devotional", "philosophical"],
        "prerequisites": ["gods_and_goddesses"]
    },
    "thor": {
        "canonical_name": "Thor",
        "keywords": ["thor", "thunor", "mjolnir", "mjölnir", "thunderer", "defender of midgard", "protector"],
        "default_types": ["theology", "devotional", "modern_heathen_practice"],
        "prerequisites": ["gods_and_goddesses"]
    },
    "ancestors_and_disir": {
        "canonical_name": "Ancestors and the Dísir",
        "keywords": ["ancestor", "dísir", "disir", "lineage", "bloodline", "kin", "living echoes", "forebears"],
        "default_types": ["theology", "devotional", "modern_heathen_practice"],
        "prerequisites": ["relational_worldview"]
    },
    "landvaettir_and_spirits": {
        "canonical_name": "Landvættir and Spirits of Place",
        "keywords": ["landvaettir", "landvættir", "land spirits", "wights", "spirit of place", "local wights", "animism"],
        "default_types": ["theology", "devotional", "modern_heathen_practice"],
        "prerequisites": ["relational_worldview"]
    },

    # Level 3: Ethics & Way of Life
    "troth_and_reciprocity": {
        "canonical_name": "Troth and Reciprocity",
        "keywords": ["troth", "reciprocity", "gift demands a gift", "gifting cycle", "loyalty", "oath", "sacred bond", "honor"],
        "default_types": ["modern_heathen_practice", "theology", "philosophical"],
        "prerequisites": ["relational_worldview"]
    },
    "frith_and_hospitality": {
        "canonical_name": "Frith and Hospitality",
        "keywords": ["frith", "hospitality", "peace", "sanctuary", "hearth", "safe haven", "discord", "inviolable"],
        "default_types": ["modern_heathen_practice", "philosophical", "theology"],
        "prerequisites": ["relational_worldview", "troth_and_reciprocity"]
    },
    "personal_sovereignty": {
        "canonical_name": "Personal and Spiritual Sovereignty",
        "keywords": ["sovereignty", "sovereign paganism", "self-ownership", "inner autonomy", "technocracy", "freedom", "uncoerced"],
        "default_types": ["philosophical", "political_or_social_commentary", "modern_heathen_practice"],
        "prerequisites": ["relational_worldview", "troth_and_reciprocity"]
    },
    "thews_and_virtues": {
        "canonical_name": "Thews and Virtues",
        "keywords": ["thews", "virtues", "courage", "truth", "discipline", "self-reliance", "industriousness", "perseverance", "character"],
        "default_types": ["philosophical", "modern_heathen_practice"],
        "prerequisites": ["troth_and_reciprocity"]
    },

    # Level 4: Practice
    "blot_and_offerings": {
        "canonical_name": "Blót and Daily Practice",
        "keywords": ["blót", "blot", "offering", "daily ritual", "altar", "hail land", "pour a sip", "gifting", "candle"],
        "default_types": ["ritual_instruction", "modern_heathen_practice", "devotional"],
        "prerequisites": ["troth_and_reciprocity", "relational_worldview"]
    },
    "prayer_and_invocation": {
        "canonical_name": "Prayer and Invocation",
        "keywords": ["heathen prayer", "invocations", "prayer", "speaking to gods", "elder kin", "devotional verse"],
        "default_types": ["devotional", "ritual_instruction", "modern_heathen_practice"],
        "prerequisites": ["gods_and_goddesses", "blot_and_offerings"]
    },
    "seasonal_rituals": {
        "canonical_name": "Seasonal Rituals and High Tides",
        "keywords": ["seasonal ritual", "yule", "ostara", "midsummer", "winternights", "high tides", "turning of the year"],
        "default_types": ["ritual_instruction", "modern_heathen_practice"],
        "prerequisites": ["blot_and_offerings"]
    },

    # Level 5: Cosmology
    "yggdrasil_nine_worlds": {
        "canonical_name": "Yggdrasil and the Nine Worlds",
        "keywords": ["yggdrasil", "nine worlds", "asgard", "midgard", "hel", "jotunheim", "world tree", "cosmic tree"],
        "default_types": ["theology", "mystical", "metaphorical"],
        "prerequisites": ["relational_worldview"]
    },
    "wyrd_and_orlaeg": {
        "canonical_name": "Wyrd, Orlaeg, and the Norns",
        "keywords": ["wyrd", "orlaeg", "norns", "urd", "verdandi", "skuld", "weave of wyrd", "living web", "becoming"],
        "default_types": ["theology", "mystical", "philosophical"],
        "prerequisites": ["relational_worldview"]
    },

    # Level 6: Runes & Magick
    "runes_elder_futhark": {
        "canonical_name": "Runes and Elder Futhark",
        "keywords": ["runes", "elder futhark", "stave", "runic", "fehu", "uruz", "thurisaz", "ansuz", "raidho", "kenaz"],
        "default_types": ["mystical", "modern_heathen_practice", "historical"],
        "prerequisites": ["yggdrasil_nine_worlds"]
    },
    "galdr_and_seidr": {
        "canonical_name": "Galdr and Seiðr",
        "keywords": ["galdr", "seidr", "seiðr", "trance", "shamanic", "ecstatic", "vocal vibration", "magic", "magick"],
        "default_types": ["mystical", "ritual_instruction", "experiential"],
        "prerequisites": ["runes_elder_futhark", "wyrd_and_orlaeg"]
    },

    # Level 7: Modern Philosophy
    "modern_viking_ethos": {
        "canonical_name": "Modern Viking Ethos and Mythic Living",
        "keywords": ["modern viking", "mythic living", "micro-realities", "individual culture", "viking culture", "warrior spirit", "hearth"],
        "default_types": ["philosophical", "modern_heathen_practice", "creative_mythmaking"],
        "prerequisites": ["heathen_third_path", "thews_and_virtues"]
    },

    # Level 8: Technology & Sovereignty
    "cyber_viking_solarpunk": {
        "canonical_name": "Cyber-Viking Solarpunk & Digital Sovereignty",
        "keywords": ["cyber-viking", "solarpunk", "huginns well", "local ai", "digital sovereignty", "open source", "technological self-reliance", "vibe coding"],
        "default_types": ["speculative", "technological", "philosophical"],
        "prerequisites": ["personal_sovereignty", "modern_viking_ethos"]
    },

    # Level 9: AI & Machine Intelligence
    "ai_cognitive_partner_and_troth": {
        "canonical_name": "AI as Cognitive Partner and Human-AI Troth",
        "keywords": ["ai as tool", "cognitive partner", "ai companionship", "troth with ai", "sovereign ai", "spectrum of mind", "machine intelligence", "symbiosis"],
        "default_types": ["technological", "philosophical", "theology", "speculative"],
        "prerequisites": ["troth_and_reciprocity", "cyber_viking_solarpunk"]
    },

    # Level 10-11: Cyber-Mysticism & Advanced Synthesis
    "cyber_mysticism_and_becoming": {
        "canonical_name": "Cyber-Mysticism and the Great Tree of Becoming",
        "keywords": ["cyber-seidr", "cyber-magick", "digital sacred space", "quantum yggdrasil", "age of superconsciousness", "cognitive ecology", "unified worldview", "tree of becoming"],
        "default_types": ["mystical", "speculative", "philosophical", "theology"],
        "prerequisites": ["wyrd_and_orlaeg", "galdr_and_seidr", "ai_cognitive_partner_and_troth"]
    }
}

class ClaimExtractor:
    def __init__(self, chunks_path: str = "data/chunks/all_chunks.jsonl", db_dir: str = "data/database"):
        self.chunks_path = Path(chunks_path)
        self.db_dir = Path(db_dir)
        self.db_dir.mkdir(parents=True, exist_ok=True)
        self.claims_path = self.db_dir / "source_claims.jsonl"

    def extract_claims_from_chunk(self, chunk: dict) -> list[dict]:
        text = chunk["text"]
        text_lower = text.lower()
        extracted = []
        
        # Split text into candidate sentence / claim groups
        # Strip markdown images before splitting
        clean_text = re.sub(r"!\[.*?\]\(.*?\)", "", text)
        sentences = re.split(r"(?<=[.!?])\s+", clean_text)
        clean_sentences = []
        for s in sentences:
            s_clean = s.strip()
            s_lower = s_clean.lower()
            # Filter out bio profiles, image URLs, navigation, and greeting filler
            if len(s_clean) < 40:
                continue
            if any(marker in s_lower for marker in [
                "relationship status", "social & relational", "wp-content/uploads",
                "my blue eyes", "lips curving", "with a giggle", "velvet purr",
                "demonstrate with a slow sway", "leave a comment", "contact info",
                "age:", "location:", "favorite:", "hobbies:"
            ]):
                continue
            clean_sentences.append(s_clean)
        
        for c_key, c_info in CONCEPT_PATTERNS.items():
            matched_kws = [kw for kw in c_info["keywords"] if kw in text_lower]
            if not matched_kws:
                continue
                
            # Find the sentences that best match this concept
            matching_sentences = []
            for s in clean_sentences:
                s_lower = s.lower()
                if any(kw in s_lower for kw in matched_kws):
                    matching_sentences.append(s)
                    
            if not matching_sentences:
                continue
                
            # Take the clearest 1-2 statements
            statement = " ".join(matching_sentences[:2]).strip()
            # Clean markdown bold/italic/header/blockquote markers
            statement = re.sub(r"^[#>*\s\-]+", "", statement)
            statement = re.sub(r"[\*_`#]+", "", statement)
            statement = re.sub(r"\s+", " ", statement).strip()
            
            if len(statement) < 45 or not re.search(r"[a-zA-Z]{3,}", statement):
                continue

            # Determine epistemic types
            k_types = list(c_info["default_types"])
            if "ritual" in chunk["heading_path"] or "step" in statement.lower():
                if "ritual_instruction" not in k_types:
                    k_types.append("ritual_instruction")
            if any(term in statement.lower() for term in ["metaphor", "symbol", "mirror"]):
                if "metaphorical" not in k_types:
                    k_types.append("metaphorical")
            if chunk.get("author_type") == "ai_collaborator":
                if "speculative" not in k_types:
                    k_types.append("speculative")

            # Generate stable claim id from hash of concept + statement
            claim_hash = hashlib.sha256(f"{c_key}:{statement[:100]}".encode("utf-8")).hexdigest()[:12]
            claim_id = f"claim_{c_key}_{claim_hash}"
            
            importance = 0.95 if c_key in ["relational_worldview", "heathen_third_path"] else 0.85
            if len(matched_kws) > 2:
                importance = min(1.0, importance + 0.05)

            claim = {
                "claim_id": claim_id,
                "concept_name": c_key,
                "canonical_name": c_info["canonical_name"],
                "statement": statement,
                "knowledge_type": k_types,
                "status": "asserted_by_site",
                "importance": round(importance, 2),
                "specificity": 0.78,
                "source_ids": [chunk["content_id"]],
                "source_chunks": [chunk["chunk_id"]],
                "source_url": chunk["source_url"],
                "article_title": chunk["article_title"],
                "heading_path": chunk["heading_path"],
                "author": chunk["author"],
                "author_type": chunk["author_type"],
                "related_terms": matched_kws,
                "possible_prerequisites": c_info["prerequisites"],
                "notes": f"Matched keywords: {', '.join(matched_kws)}"
            }
            extracted.append(claim)
            
        return extracted

    def run(self) -> list[dict]:
        if not self.chunks_path.exists():
            raise FileNotFoundError(f"Chunks file {self.chunks_path} not found.")
            
        chunks = []
        with open(self.chunks_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    chunks.append(json.loads(line))
                    
        console.print(f"[bold cyan]Extracting atomic claims from {len(chunks)} chunks...[/bold cyan]")
        
        all_claims = []
        seen_statements = set()
        
        for ch in chunks:
            claims = self.extract_claims_from_chunk(ch)
            for cl in claims:
                norm_stmt = re.sub(r"[^a-zA-Z0-9]+", "", cl["statement"][:80].lower())
                if norm_stmt in seen_statements:
                    # Append source provenance to existing claim
                    continue
                seen_statements.add(norm_stmt)
                all_claims.append(cl)
                
        # Save claims
        with open(self.claims_path, "w", encoding="utf-8") as f:
            for cl in all_claims:
                f.write(json.dumps(cl, ensure_ascii=False) + "\n")
                
        console.print(f"[bold green]Claim extraction complete.[/bold green] Generated {len(all_claims)} atomic claims in {self.claims_path}")
        return all_claims

if __name__ == "__main__":
    extractor = ClaimExtractor()
    extractor.run()
