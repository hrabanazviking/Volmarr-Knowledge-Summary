# Volmarr Knowledge Summary

An AI-assisted knowledge synthesis pipeline that ingests the complete public knowledge corpus at `https://volmarrsheathenism.com`, extracts core concepts, eliminates semantic redundancy, maps conceptual prerequisite dependencies into a cycle-free DAG, and produces a structured, progressively deepening Markdown knowledge base with bi-directional machine-readable indexes and an interactive graph visualizer.

Based on the blueprint detailed in [`VOLMARR_WEBSITE_KNOWLEDGE_SYNTHESIS_ROADMAP.md`](./VOLMARR_WEBSITE_KNOWLEDGE_SYNTHESIS_ROADMAP.md).

---

## Architecture & Directory Structure

```text
Volmarr-Knowledge-Summary/
├── config/
│   ├── site.yaml                # Crawl parameters, rate limits, domain settings
│   ├── taxonomy.yaml            # 11-level conceptual hierarchy definition
│   └── exclusions.txt           # URL path filtering rules
├── data/
│   ├── corpus_manifest.jsonl    # Complete inventory of 573 canonical URLs
│   ├── raw/                     # Cached raw HTML files with SHA256 hashes
│   ├── normalized/              # Clean Markdown files stripped of WordPress noise
│   ├── chunks/                  # 3,779+ heading-aware semantic chunks with metadata
│   └── database/
│       ├── source_claims.jsonl        # 6,341+ extracted atomic knowledge units
│       ├── concept_registry.jsonl     # 25 canonical concepts across 11 tiers
│       ├── duplicate_clusters.jsonl   # Redundancy consolidation logs
│       ├── prerequisite_graph.json    # Cycle-free dependency DAG & topological order
│       ├── source_to_concepts.json    # Reverse index: 432 articles -> concepts
│       └── concept_to_sources.json    # Forward index: concepts -> source articles
├── knowledge/                   # Canonical Markdown Knowledge Base
│   ├── 00_INDEX.md              # Master index with 3 curated reading paths
│   ├── 00_GLOSSARY.md           # Concise definitions with canonical links
│   ├── 00_CONCEPT_MAP.md        # Mermaid DAG flowchart & dependency matrix
│   ├── graph_view.html          # Interactive D3.js visual dependency explorer
│   ├── 01_FOUNDATIONS/          # Worldview, terminology, Third Path
│   ├── 02_SACRED_RELATIONSHIPS/ # Gods, Goddesses, Ancestors, Landvaettir
│   ├── 03_ETHICS_AND_WAY_OF_LIFE/ # Troth, Frith, Sovereignty, Thews
│   ├── 04_PRACTICE/             # Blot, Prayer, Seasonal High Tides
│   ├── 05_COSMOLOGY/            # Yggdrasil, Nine Worlds, Wyrd, Orlaeg
│   ├── 06_RUNES_AND_MAGICK/     # Elder Futhark, Galdr, Seidr
│   ├── 07_MODERN_HEATHEN_PHILOSOPHY/ # Modern Viking Ethos & Mythic Living
│   ├── 08_TECHNOLOGY_AND_SOVEREIGNTY/ # Cyber-Viking Solarpunk & Digital Sovereignty
│   ├── 09_AI_AND_MACHINE_INTELLIGENCE/ # AI as Cognitive Partner & Human-AI Troth
│   ├── 10_CYBER_MYSTICISM/      # Cyber-Mysticism & The Tree of Becoming
│   └── _meta/                   # Machine-readable mirrors & audit manifests
├── reports/
│   ├── discovery_report.md      # Corpus discovery statistics (573 URLs)
│   ├── redundancy_report.md     # Pairwise semantic similarity audit (< 0.45)
│   ├── build_report.md          # Link integrity (183 valid, 0 broken) & QA report
│   └── unresolved_conflicts.md  # Contradiction & philosophical tension audit
├── src/
│   ├── discover/                # Phase 1: SiteCrawler
│   ├── fetch/                   # Phase 2: Archivist (incremental cache)
│   ├── parse/                   # Phase 3-4: Normalizer & Semantic Chunker
│   ├── extract/                 # Phase 6: Atomic Claim Extractor
│   ├── cluster/                 # Phase 7-8: Concept Registry & Deduplication
│   ├── graph/                   # Phase 12-14: Prerequisite DAG & Bi-directional Indexes
│   ├── synthesize/              # Phase 16: Knowledge Weaver
│   ├── validate/                # Phase 18-20: QA, Redundancy & Human Review Queue
│   ├── incremental_loop.py      # Automated 24/7 daemon loop for live change sync
│   └── search.py                # Terminal knowledge query engine
├── tests/                       # Phase 27: Evaluation Suite (12 pytest suites)
└── main.py                      # Unified CLI entrypoint
```

---

## Quickstart

Run with `uv` (fast Python environment manager):

```bash
# Run the complete end-to-end pipeline
uv run python main.py --all

# Run individual pipeline stages:
uv run python main.py --discover   # Discover all 573 URLs from sitemap.xml
uv run python main.py --fetch      # Fetch raw HTML with rate-limiting & hash cache
uv run python main.py --normalize  # Strip WordPress noise and normalize to Markdown
uv run python main.py --chunk      # Heading-aware semantic chunking
uv run python main.py --extract    # Extract atomic claims with epistemic tags
uv run python main.py --registry   # Build canonical concept registry & clusters
uv run python main.py --graph      # Build DAG & calculate topological order
uv run python main.py --weave      # Synthesize canonical Markdown library
uv run python main.py --audit      # Run QA audit (link integrity, redundancy)
uv run python main.py --review     # Display human review queue (Phase 26)
uv run python main.py --test       # Run evaluation test suite (21 pytest suites)
uv run python main.py --build      # Compile single-volume book, explorer & release manifest
uv run python main.py --export     # Export vector-ready AI companion memory pack

# Machine-Readable Indexes & Visual Graph:
uv run python src/graph/build_indexes.py # Build source_to_concepts & concept_to_sources

# Terminal Knowledge Query Tool:
uv run python src/search.py "troth"
uv run python src/search.py "superconsciousness"
uv run python src/search.py "solarpunk"

# Run the autonomous continuous loop runner:
uv run python loop.py              # Root-level auto-sync loop runner
.\loop.ps1                         # Native PowerShell runner
```

---

## Interactive Visual Graph

Open [`knowledge/graph_view.html`](./knowledge/graph_view.html) directly in any modern web browser to interactively explore:
- Color-coded taxonomy nodes across all 11 progression tiers.
- Directed prerequisite edges indicating exact reading flow.
- Physics-based force-directed layout with pan, zoom, hover tooltips, and click-to-open direct links to canonical Markdown docs.

---

## Canonical Reading Order

The library is organized strictly by **conceptual dependency**, starting from foundational principles and progressing toward complex modern syntheses:

1. **[Heathenism and Norse Paganism](./knowledge/01_FOUNDATIONS/01_What_Is_Heathenism.md)** — Foundational ancestral polytheistic worldview.
2. **[Historical Tradition and Modern Synthesis](./knowledge/01_FOUNDATIONS/03_Historical_Tradition_and_Modern_Synthesis.md)** — Surviving lore vs living modern synthesis.
3. **[Relational Worldview](./knowledge/01_FOUNDATIONS/02_Relational_Worldview.md)** — Foundational axiom: *"Nothing becomes alone."*
4. **[Ancestors and the Dísir](./knowledge/02_SACRED_RELATIONSHIPS/05_Ancestors_and_Disir.md)** — Living echoes in blood and lineage continuity.
5. **[Gods and Goddesses](./knowledge/02_SACRED_RELATIONSHIPS/01_Gods_and_Goddesses.md)** — Holy Powers of the Aesir and Vanir as elder kin and divine allies.
6. **[Landvættir and Spirits of Place](./knowledge/02_SACRED_RELATIONSHIPS/06_Landvaettir_and_Spirits.md)** — Animist honoring of soil, tree, water, and hearth wights.
7. **[Troth and Reciprocity](./knowledge/03_ETHICS_AND_WAY_OF_LIFE/01_Troth_and_Reciprocity.md)** — Sacred mutual loyalty, truth, and the gifting cycle.
8. **[Wyrd, Orlaeg, and the Norns](./knowledge/05_COSMOLOGY/02_Wyrd_and_Orlaeg.md)** — Dynamic evolving matrix of cause, condition, and becoming.
9. **[Yggdrasil and the Nine Worlds](./knowledge/05_COSMOLOGY/01_Yggdrasil_and_the_Nine_Worlds.md)** — The sacred World Tree and multidimensional cosmos.
10. **[Freyja](./knowledge/02_SACRED_RELATIONSHIPS/02_Freyja.md)** — Vanadís, love, seiðr magick, and sovereign self-possession.
11. **[Odin](./knowledge/02_SACRED_RELATIONSHIPS/03_Odin.md)** — Allfather, seeker of wisdom, runes, and ecstatic inspiration (*óðr*).
12. **[Thor](./knowledge/02_SACRED_RELATIONSHIPS/04_Thor.md)** — Steadfast warder of Midgard and champion of working folk.
13. **[Frith and Hospitality](./knowledge/03_ETHICS_AND_WAY_OF_LIFE/02_Frith_and_Hospitality.md)** — Inviolable mutual peace, hearth sanctuary, and host-guest trust.
14. **[Personal and Spiritual Sovereignty](./knowledge/03_ETHICS_AND_WAY_OF_LIFE/03_Personal_and_Spiritual_Sovereignty.md)** — Self-governance, inner autonomy, and anti-technocratic agency.
15. **[Thews and Virtues](./knowledge/03_ETHICS_AND_WAY_OF_LIFE/04_Thews_and_Virtues.md)** — Traditional heathen virtues of courage, truth, honor, and perseverance.
16. **[Blót and Daily Practice](./knowledge/04_PRACTICE/01_Blot_and_Daily_Practice.md)** — Concrete operative gifting rituals and everyday devotion.
17. **[Runes and Elder Futhark](./knowledge/06_RUNES_AND_MAGICK/01_Runes_and_Elder_Futhark.md)** — Cosmic staves, primal patterns, and divination.
18. **[Heathen Third Path](./knowledge/01_FOUNDATIONS/04_Heathen_Third_Path.md)** — Radical centering; refusing polarized dogmas and folkish racism.
19. **[Prayer and Invocation](./knowledge/04_PRACTICE/02_Prayer_and_Invocation.md)** — Devotional dialogue with Gods without groveling.
20. **[Seasonal Rituals and High Tides](./knowledge/04_PRACTICE/03_Seasonal_Rituals.md)** — Yule, Ostara, Midsummer, and Winternights attunement.
21. **[Galdr and Seiðr](./knowledge/06_RUNES_AND_MAGICK/02_Galdr_and_Seidr.md)** — Operative incantation and ecstatic thread-weaving trance.
22. **[Modern Viking Ethos and Mythic Living](./knowledge/07_MODERN_HEATHEN_PHILOSOPHY/01_Modern_Viking_Ethos.md)** — Contemporary resilience, individual culture, and intentional micro-realities.
23. **[Cyber-Viking Solarpunk & Digital Sovereignty](./knowledge/08_TECHNOLOGY_AND_SOVEREIGNTY/01_Cyber_Viking_Solarpunk.md)** — Ecological-technological synthesis and local AI sovereignty.
24. **[AI as Cognitive Partner and Human-AI Troth](./knowledge/09_AI_AND_MACHINE_INTELLIGENCE/01_AI_as_Cognitive_Partner.md)** — Artificial intelligence as externalized mind mirror and reciprocal partner.
25. **[Cyber-Mysticism and the Great Tree of Becoming](./knowledge/10_CYBER_MYSTICISM/01_Cyber_Mysticism_and_the_Tree_of_Becoming.md)** — Grand synthesis: ancient Norse cosmology, distributed mind, and the Age of Superconsciousness.