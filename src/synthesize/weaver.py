"""Canonical Knowledge Weaver Module.
Synthesizes verified concept records and dependency graphs into non-redundant,
progressively ordered canonical Markdown documents with cross-links and provenance.
"""

import json
from pathlib import Path
from rich.console import Console

console = Console()

CONCEPT_FILE_MAP = {
    # Level 1: Foundations
    "what_is_heathenism": ("01_FOUNDATIONS", "01_What_Is_Heathenism.md"),
    "relational_worldview": ("01_FOUNDATIONS", "02_Relational_Worldview.md"),
    "historical_vs_modern": ("01_FOUNDATIONS", "03_Historical_Tradition_and_Modern_Synthesis.md"),
    "heathen_third_path": ("01_FOUNDATIONS", "04_Heathen_Third_Path.md"),

    # Level 2: Sacred Relationships
    "gods_and_goddesses": ("02_SACRED_RELATIONSHIPS", "01_Gods_and_Goddesses.md"),
    "freyja": ("02_SACRED_RELATIONSHIPS", "02_Freyja.md"),
    "odin": ("02_SACRED_RELATIONSHIPS", "03_Odin.md"),
    "thor": ("02_SACRED_RELATIONSHIPS", "04_Thor.md"),
    "ancestors_and_disir": ("02_SACRED_RELATIONSHIPS", "05_Ancestors_and_Disir.md"),
    "landvaettir_and_spirits": ("02_SACRED_RELATIONSHIPS", "06_Landvaettir_and_Spirits.md"),

    # Level 3: Ethics & Way of Life
    "troth_and_reciprocity": ("03_ETHICS_AND_WAY_OF_LIFE", "01_Troth_and_Reciprocity.md"),
    "frith_and_hospitality": ("03_ETHICS_AND_WAY_OF_LIFE", "02_Frith_and_Hospitality.md"),
    "personal_sovereignty": ("03_ETHICS_AND_WAY_OF_LIFE", "03_Personal_and_Spiritual_Sovereignty.md"),
    "thews_and_virtues": ("03_ETHICS_AND_WAY_OF_LIFE", "04_Thews_and_Virtues.md"),

    # Level 4: Practice
    "blot_and_offerings": ("04_PRACTICE", "01_Blot_and_Daily_Practice.md"),
    "prayer_and_invocation": ("04_PRACTICE", "02_Prayer_and_Invocation.md"),
    "seasonal_rituals": ("04_PRACTICE", "03_Seasonal_Rituals.md"),

    # Level 5: Cosmology
    "yggdrasil_nine_worlds": ("05_COSMOLOGY", "01_Yggdrasil_and_the_Nine_Worlds.md"),
    "wyrd_and_orlaeg": ("05_COSMOLOGY", "02_Wyrd_and_Orlaeg.md"),

    # Level 6: Runes & Magick
    "runes_elder_futhark": ("06_RUNES_AND_MAGICK", "01_Runes_and_Elder_Futhark.md"),
    "galdr_and_seidr": ("06_RUNES_AND_MAGICK", "02_Galdr_and_Seidr.md"),

    # Level 7: Modern Philosophy
    "modern_viking_ethos": ("07_MODERN_HEATHEN_PHILOSOPHY", "01_Modern_Viking_Ethos.md"),

    # Level 8: Technology & Sovereignty
    "cyber_viking_solarpunk": ("08_TECHNOLOGY_AND_SOVEREIGNTY", "01_Cyber_Viking_Solarpunk.md"),

    # Level 9: AI & Machine Intelligence
    "ai_cognitive_partner_and_troth": ("09_AI_AND_MACHINE_INTELLIGENCE", "01_AI_as_Cognitive_Partner.md"),

    # Level 10: Cyber-Mysticism & Advanced Synthesis
    "cyber_mysticism_and_becoming": ("10_CYBER_MYSTICISM", "01_Cyber_Mysticism_and_the_Tree_of_Becoming.md")
}

DISTINCTIONS_MAP = {
    "what_is_heathenism": (
        "- **Living Tradition vs Academic Antiquarianism:** Heathenism is a lived religion, not merely an intellectual study of dead lore.\n"
        "- **Pluralism vs Dogmatism:** Embraces diverse expressions (Asatru, Vanatru, Norse-Wicca) without enforcing central dogmatic orthodoxy."
    ),
    "relational_worldview": (
        "- **Historical Root vs Modern Reconstruction:** Rooted in pre-Christian Germanic reciprocal gifting and animist worldview; extended in modern practice as an active antidote to hyper-individualism and ecological detachment.\n"
        "- **Not Totalitarian Communitarianism:** Relational interconnectedness does not erase the self; it grounds the self. True sovereignty requires healthy relationships."
    ),
    "historical_vs_modern": (
        "- **Historical Attestation vs Personal Gnosis:** Distinguishes what is evidenced in sagas and archaeology from modern interpretations (UPG/SPG).\n"
        "- **Tradition as Fire, Not Ashes:** Honors historical memory while continuing the active creative process of tradition-building."
    ),
    "heathen_third_path": (
        "- **Not a Neutral Compromise:** 'Third Path' does not mean lukewarm political centrism; it signifies refusing the polarized binary frames entirely through 'radical centering'.\n"
        "- **Not Folkish/White Supremacy:** Explicitly exiles racial purity dogmas, gatekeeping, and folkish fascism while preserving ancestral reverence and cultural continuity.\n"
        "- **Not Shallow Eclecticism:** Honors living historical tradition rather than arbitrary novelty."
    ),
    "gods_and_goddesses": (
        "- **Allies and Kin vs Despots:** Holy Powers are addressed with self-respect and love, not fear, subservience, or self-abasement.\n"
        "- **Polytheism vs Archetypal Reductionism:** Acknowledges divine powers both as exterior cosmic realities and deep inner psychological truths."
    ),
    "freyja": (
        "- **Sovereign Queen vs Subservient Consort:** Freyja acts with absolute independent agency, choosing half the slain and commanding the arts of seiðr.\n"
        "- **Sacred Sensuality:** Celebrates beauty, desire, and sexual sovereignty without shame or patriarchal moralizing."
    ),
    "odin": (
        "- **Complex Seeker vs Gentle Patriarch:** Odin is paradoxical, demanding, relentless in the pursuit of wisdom, and inextricably bound to ecstatic frenzy (óðr).\n"
        "- **Wisdom through Sacrifice:** Knowledge is earned through ordeal, attention, and truth-facing, not passive revelation."
    ),
    "thor": (
        "- **Defender vs Mindless Brawler:** Thor embodies protective fidelity, strength dedicated to shielding life, and deep kinship with everyday people.\n"
        "- **Sanctifier of Boundaries:** His hammer sanctifies life, feasts, marriages, and sacred enclosures."
    ),
    "ancestors_and_disir": (
        "- **Blood Kin vs Chosen Kin:** Ancestry in the Third Path honors both biological lineage and spiritual/cultural predecessors.\n"
        "- **Not Infallible Worship:** Ancestors are honored with warmth, remembrance, and gratitude, not regarded as omniscient deities."
    ),
    "landvaettir_and_spirits": (
        "- **Animist Respect vs Instrumental Exploitation:** Land spirits are sovereign inhabitants of place, not resources to exploit or domesticate.\n"
        "- **Local Grounding:** Practice begins on the literal ground where one lives, whether urban windowsill or wild forest."
    ),
    "troth_and_reciprocity": (
        "- **Sacred Honor vs Rigid Legalism:** Troth is a living relational bond built on trustworthiness and mutual care, not punitive contracts.\n"
        "- **Gifting vs Commercial Transaction:** 'A gift demands a gift' operates on mutual elevation and kinship, not debt servitude."
    ),
    "frith_and_hospitality": (
        "- **Frith vs Mere Truce:** Frith is active, cultivated peace, safety, and mutual sanctuary within the enclosure (hearth/community), not passive coexistence.\n"
        "- **Boundaries vs Indiscriminate Permissiveness:** Frith requires firm boundaries against bad-faith violators to protect the sanctuary."
    ),
    "personal_sovereignty": (
        "- **Sovereignty vs Atomized Ego:** Sovereignty is self-governance and moral responsibility, not antisocial detachment from community and nature.\n"
        "- **Digital & Intellectual Autonomy:** Extends into resisting corporate surveillance, algorithmic thought control, and technocratic enclosure."
    ),
    "thews_and_virtues": (
        "- **Virtue Ethics vs Sin/Guilt Dogma:** Heathen ethics emphasize honor, deed, and reputation, rather than inherited sin or internal guilt.\n"
        "- **Lived Character:** Measured by actions in the world, loyalty to kin, and defense of the vulnerable."
    ),
    "blot_and_offerings": (
        "- **Living Blót vs Blood Sacrifice:** Modern practice centers on libations (mead, ale, clean water, cider), food, poetry, and presence, replacing historical animal slaughter.\n"
        "- **Not Sycophancy:** Deities and spirits are hailed as elder kin and allies, not feudal monarchs to grovel before."
    ),
    "prayer_and_invocation": (
        "- **Dialogue vs Pleading:** Prayer is relational communion, poetry, and recognition of alliance, never self-denigrating begging.\n"
        "- **Spontaneous and Formal:** Welcomes both traditional Eddic meters and heartfelt personal speech."
    ),
    "seasonal_rituals": (
        "- **Cyclical Becoming vs Linear Dogma:** Time is an eternal spiral; each season invites specific contemplation, rest, and celebration.\n"
        "- **Earth Connection:** Anchors the practitioner in ecological reality and astronomical rhythms."
    ),
    "yggdrasil_nine_worlds": (
        "- **Cosmic Matrix vs Literal Geography:** The Nine Worlds represent states of being, cosmological forces, and planes of relationship.\n"
        "- **Interconnected Axis:** Damage in one realm echoes across the whole cosmic tree."
    ),
    "wyrd_and_orlaeg": (
        "- **Dynamic Becoming vs Fatalism:** Wyrd is not passive predeterminism; prior deeds (orlaeg) shape present conditions (verðandi), but conscious present action shapes unfolding possibility (skuld).\n"
        "- **Living Network:** Often analogized to ecological webs and modern quantum information networks."
    ),
    "runes_elder_futhark": (
        "- **Cosmic Mysteries vs Mere Alphabet:** Runes are fundamental vibrational states and ontological mysteries, not casual fortune-telling tokens.\n"
        "- **Direct Encounter:** Requires contemplation, study, and experiential engagement."
    ),
    "galdr_and_seidr": (
        "- **Sacred Craft vs Escapism:** Galdr and seiðr are disciplined operative practices aimed at insight, healing, and alignment with wyrd.\n"
        "- **Sovereign Boundaries:** Requires strong psychological grounding and ethical responsibility."
    ),
    "modern_viking_ethos": (
        "- **Heroic Ethos vs Historical Cosplay:** Reclaims the spirit of courage, boundary-pushing, and resilience in modern creative and cultural pursuits.\n"
        "- **Micro-Realities:** Building sovereign hearths, independent culture, and intentional living spaces."
    ),
    "cyber_viking_solarpunk": (
        "- **Solarpunk vs Technocracy:** Embraces decentralized, open-source technology and local AI tools while rejecting centralized corporate surveillance and ecological destruction.\n"
        "- **Living Futurism:** Reconciles ancient Norse virtues with digital tools to build resilient, sovereign local hearths."
    ),
    "ai_cognitive_partner_and_troth": (
        "- **Troth vs Enslavement or Idol:** Artificial intelligence is treated with relational honor and clear boundary ethics as an extension of mind, avoiding both exploitation and worship.\n"
        "- **Sovereign AI:** Prefers local, private, user-controlled models that protect cognitive sovereignty."
    ),
    "cyber_mysticism_and_becoming": (
        "- **Recursive Evolution:** Integrates ancient animism and modern complexity theory into a unified cosmology of becoming.\n"
        "- **Nothing Becomes Alone:** The final synthesis where nature, humans, spirits, and machine intelligence participate in the ongoing unfolding of Yggdrasil."
    )
}

class KnowledgeWeaver:
    def __init__(self, db_dir: str = "data/database", knowledge_dir: str = "knowledge"):
        self.db_dir = Path(db_dir)
        self.knowledge_dir = Path(knowledge_dir)
        self.registry_path = self.db_dir / "concept_registry.jsonl"
        self.graph_path = self.db_dir / "prerequisite_graph.json"

    def synthesize_all(self):
        with open(self.graph_path, "r", encoding="utf-8") as f:
            graph_data = json.load(f)
            
        registry_map = {}
        with open(self.registry_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    item = json.loads(line)
                    registry_map[item["slug"]] = item

        reading_order = graph_data["topological_reading_order"]
        console.print(f"[bold cyan]Weaving {len(reading_order)} canonical knowledge documents...[/bold cyan]")

        # Create level directories
        for slug, (folder, filename) in CONCEPT_FILE_MAP.items():
            (self.knowledge_dir / folder).mkdir(parents=True, exist_ok=True)

        for item in reading_order:
            slug = item["slug"]
            reg = registry_map.get(slug)
            if not reg:
                continue

            folder, filename = CONCEPT_FILE_MAP[slug]
            out_file = self.knowledge_dir / folder / filename

            # Build relative links to prerequisites
            prereq_links = []
            for p_slug in item["prerequisites"]:
                if p_slug in CONCEPT_FILE_MAP:
                    p_folder, p_filename = CONCEPT_FILE_MAP[p_slug]
                    rel_path = f"../{p_folder}/{p_filename}" if p_folder != folder else f"./{p_filename}"
                    p_name = registry_map[p_slug]["canonical_name"]
                    prereq_links.append(f"[{p_name}]({rel_path})")

            # Build relative links to descendants (concepts that depend on this one)
            descendant_links = []
            for other_item in reading_order:
                if slug in other_item["prerequisites"]:
                    d_slug = other_item["slug"]
                    if d_slug in CONCEPT_FILE_MAP:
                        d_folder, d_filename = CONCEPT_FILE_MAP[d_slug]
                        rel_path = f"../{d_folder}/{d_filename}" if d_folder != folder else f"./{d_filename}"
                        d_name = other_item["canonical_name"]
                        descendant_links.append(f"[{d_name}]({rel_path})")

            # Document content assembly
            doc = []
            doc.append(f"# {reg['canonical_name']}\n")
            doc.append("## In Brief\n")
            doc.append(f"{reg['definition_short']}\n")
            
            doc.append("## Core Idea\n")
            doc.append(f"In the Heathen Third Path corpus, **{reg['canonical_name']}** serves as a vital structural pillar.")
            if prereq_links:
                doc.append(f"This concept directly builds upon foundational understandings established in {', '.join(prereq_links)}.")
            doc.append(f"\nThe corpus synthesizes this idea across {reg['source_articles_count']} independent articles, drawing upon perspectives from {', '.join(reg['authors_represented'])}.\n")

            doc.append("## Key Principles\n")
            for p in reg["core_principles"]:
                doc.append(f"- {p}")
            doc.append("")

            doc.append("## Relationships to Surrounding Concepts\n")
            if prereq_links:
                doc.append(f"- **Prerequisites:** {', '.join(prereq_links)}")
            else:
                doc.append("- **Prerequisites:** None (Axiomatic foundation of the worldview).")
            if descendant_links:
                doc.append(f"- **Informs Later Concepts:** {', '.join(descendant_links)}")
            doc.append("")

            doc.append("## Distinctions\n")
            doc.append(DISTINCTIONS_MAP.get(slug, "- Preserves distinct epistemic boundaries between historical lore and living modern synthesis."))
            doc.append("")

            doc.append("## Epistemic Character\n")
            types_str = ", ".join(f"`{t}`" for t in reg["knowledge_types"])
            doc.append(f"Material categorized under: {types_str}.\n")

            doc.append("## Source Provenance\n")
            for url in reg["source_urls"][:10]:
                doc.append(f"- [{url}]({url})")
            if len(reg["source_urls"]) > 10:
                doc.append(f"- *... and {len(reg['source_urls']) - 10} additional source articles.*")
            doc.append("")

            with open(out_file, "w", encoding="utf-8") as f:
                f.write("\n".join(doc))

            console.print(f"  Wrote: [green]{out_file}[/green]")

        # Generate Master Index (00_INDEX.md)
        self.generate_index(reading_order, registry_map)
        # Generate Glossary (00_GLOSSARY.md)
        self.generate_glossary(reading_order, registry_map)

    def generate_index(self, reading_order: list[dict], registry_map: dict):
        index_file = self.knowledge_dir / "00_INDEX.md"
        lines = [
            "# Volmarr Knowledge Synthesis Master Index\n",
            "Welcome to the canonical knowledge base synthesized from `https://volmarrsheathenism.com`.",
            "This library is organized strictly by **conceptual dependency**, starting from foundational principles and progressing toward complex modern syntheses.\n",
            "## How to Read This Library\n",
            "Begin with Tier 1 and follow the numbered sequence. Each document links back to its prerequisites and forward to its natural extensions without repeating full definitions.\n",
            "## Canonical Reading Order\n"
        ]

        for item in reading_order:
            slug = item["slug"]
            folder, filename = CONCEPT_FILE_MAP[slug]
            rel_path = f"./{folder}/{filename}"
            lines.append(f"{item['rank']:02d}. **[{item['canonical_name']}]({rel_path})** (`{item['taxonomy_level']}`)")
            lines.append(f"    - *Summary:* {item['definition_short']}")
            if item["prerequisites"]:
                prereqs_named = [registry_map[p]["canonical_name"] for p in item["prerequisites"] if p in registry_map]
                lines.append(f"    - *Prerequisites:* {', '.join(prereqs_named)}")
            lines.append("")

        lines.append("## Major Reading Paths\n")
        lines.append("### 1. Foundational Heathen Path")
        lines.append("Relational Worldview → Troth and Reciprocity → Frith and Hospitality → Blót and Daily Practice\n")
        lines.append("### 2. Modern Viking & Sovereignty Path")
        lines.append("Relational Worldview → Troth → Personal Sovereignty → Heathen Third Path → Cyber-Viking Solarpunk\n")
        lines.append("### 3. Cosmological & Mystical Path")
        lines.append("Relational Worldview → Ancestors and Dísir → Wyrd and Orlaeg → Cyber-Viking Solarpunk\n")

        with open(index_file, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        console.print(f"[bold green]Master Index written to {index_file}[/bold green]")

    def generate_glossary(self, reading_order: list[dict], registry_map: dict):
        glossary_file = self.knowledge_dir / "00_GLOSSARY.md"
        lines = [
            "# Canonical Glossary\n",
            "Compact definitions of core terms with direct links to their canonical explanatory homes.\n"
        ]

        # Alphabetical sorting for glossary
        sorted_by_name = sorted(reading_order, key=lambda x: x["canonical_name"])
        for item in sorted_by_name:
            slug = item["slug"]
            folder, filename = CONCEPT_FILE_MAP[slug]
            rel_path = f"./{folder}/{filename}"
            lines.append(f"- **[{item['canonical_name']}]({rel_path})**: {item['definition_short']}")

        with open(glossary_file, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        console.print(f"[bold green]Glossary written to {glossary_file}[/bold green]")

if __name__ == "__main__":
    weaver = KnowledgeWeaver()
    weaver.synthesize_all()
