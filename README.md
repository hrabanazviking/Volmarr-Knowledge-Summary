# Volmarr Knowledge Summary

An AI-assisted knowledge synthesis pipeline that ingests the public corpus at `https://volmarrsheathenism.com`, extracts core concepts, eliminates semantic redundancy, maps conceptual prerequisite dependencies into a DAG, and produces a structured, progressively deepening Markdown knowledge base.

Based on the blueprint detailed in [`VOLMARR_WEBSITE_KNOWLEDGE_SYNTHESIS_ROADMAP.md`](./VOLMARR_WEBSITE_KNOWLEDGE_SYNTHESIS_ROADMAP.md).

---

## Architecture & Directory Structure

```text
Volmarr-Knowledge-Summary/
├── config/
│   ├── site.yaml           # Crawl parameters, rate limits, domain settings
│   ├── taxonomy.yaml       # 11-level conceptual hierarchy definition
│   └── exclusions.txt      # URL path filtering rules
├── data/
│   ├── corpus_manifest.jsonl # Complete inventory of 571 canonical URLs
│   ├── raw/                # Cached raw HTML files with SHA256 hashes
│   ├── normalized/         # Clean Markdown files stripped of WordPress noise
│   ├── chunks/             # Heading-aware semantic chunks with metadata
│   └── database/
│       ├── source_claims.jsonl      # Extracted atomic knowledge units
│       ├── concept_registry.jsonl   # Canonical concepts & provenance
│       ├── duplicate_clusters.jsonl # Redundancy consolidation logs
│       └── prerequisite_graph.json  # Concept dependency DAG & reading order
├── knowledge/              # Generated Canonical Markdown Library
│   ├── 00_INDEX.md         # Master index with topological learning paths
│   ├── 00_GLOSSARY.md      # Concise definitions with canonical links
│   ├── 01_FOUNDATIONS/
│   ├── 02_SACRED_RELATIONSHIPS/
│   ├── 03_ETHICS_AND_WAY_OF_LIFE/
│   ├── 04_PRACTICE/
│   ├── 05_COSMOLOGY/
│   └── 08_TECHNOLOGY_AND_SOVEREIGNTY/
├── reports/
│   ├── discovery_report.md  # Corpus discovery statistics (571 URLs)
│   ├── redundancy_report.md # Pairwise semantic similarity audit (< 0.45)
│   └── build_report.md      # Link integrity & schema compliance report
├── src/
│   ├── discover/           # Phase 1: SiteCrawler
│   ├── fetch/              # Phase 2: Archivist (incremental cache)
│   ├── parse/              # Phase 3-4: Normalizer & Semantic Chunker
│   ├── extract/            # Phase 6: Atomic Claim Extractor
│   ├── cluster/            # Phase 7-8: Concept Registry & Deduplication
│   ├── graph/              # Phase 12-14: Prerequisite DAG & Topological Sort
│   ├── synthesize/         # Phase 16: Knowledge Weaver
│   └── validate/           # Phase 18-20: QA & Redundancy Auditor
└── main.py                 # Unified CLI entrypoint
```

---

## Quickstart

Run with `uv` (fast Python environment manager):

```bash
# Run the complete end-to-end pipeline
uv run python main.py --all

# Or run individual stages:
uv run python main.py --discover   # Discover all 571 URLs from sitemap.xml
uv run python main.py --fetch      # Fetch raw HTML with rate-limiting & hash cache
uv run python main.py --normalize  # Strip WordPress noise and normalize to Markdown
uv run python main.py --chunk      # Heading-aware semantic chunking
uv run python main.py --extract    # Extract atomic claims with epistemic tags
uv run python main.py --registry   # Build canonical concept registry & clusters
uv run python main.py --graph      # Build DAG & calculate topological order
uv run python main.py --weave      # Synthesize canonical Markdown library
uv run python main.py --audit      # Run QA audit (link integrity, redundancy)
```

---

## Canonical Reading Order (Milestone 1 Prototype)

1. **[Relational Worldview](./knowledge/01_FOUNDATIONS/01_Relational_Worldview.md)** — Foundational axiom: *"Nothing becomes alone."*
2. **[Ancestors and the Dísir](./knowledge/02_SACRED_RELATIONSHIPS/01_Ancestors_and_Disir.md)** — Living echoes and lineage continuity.
3. **[Troth and Reciprocity](./knowledge/03_ETHICS_AND_WAY_OF_LIFE/01_Troth_and_Reciprocity.md)** — Sacred mutual loyalty and gifting cycle.
4. **[Wyrd and Orlaeg](./knowledge/05_COSMOLOGY/01_Wyrd_and_Orlaeg.md)** — Dynamic web of cause, condition, and becoming.
5. **[Frith and Hospitality](./knowledge/03_ETHICS_AND_WAY_OF_LIFE/02_Frith_and_Hospitality.md)** — Inviolable peace, hearth sanctuary, and boundary keeping.
6. **[Personal and Spiritual Sovereignty](./knowledge/03_ETHICS_AND_WAY_OF_LIFE/03_Personal_and_Spiritual_Sovereignty.md)** — Self-governance, digital autonomy, and anti-technocratic agency.
7. **[Blót and Daily Practice](./knowledge/04_PRACTICE/01_Blot_and_Daily_Practice.md)** — Concrete operative gifting rituals and everyday devotion.
8. **[Heathen Third Path](./knowledge/01_FOUNDATIONS/02_Heathen_Third_Path.md)** — Radical centering; refusing polarized dogmas.
9. **[Cyber-Viking Solarpunk & Digital Sovereignty](./knowledge/08_TECHNOLOGY_AND_SOVEREIGNTY/01_Cyber_Viking_Solarpunk.md)** — Modern ecological-technological synthesis and local AI sovereignty.