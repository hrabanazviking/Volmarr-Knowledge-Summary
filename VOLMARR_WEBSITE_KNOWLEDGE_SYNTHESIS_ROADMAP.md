# Volmarr's Website Knowledge Synthesis Roadmap

**Project goal:** Build an AI-assisted pipeline that reads the complete public knowledge corpus at `https://volmarrsheathenism.com`, extracts the ideas expressed across the site, removes semantic redundancy without erasing meaningful nuance, and produces a coherent library of Markdown summaries ordered from the simplest foundational ideas to the most complex syntheses.

**Primary design principle:** The website is the source corpus. The generated Markdown library is not a post-by-post archive. It is a distilled knowledge system.

**Core rule:** An idea should have one canonical home. Other documents may reference that idea, but should not repeatedly re-explain it unless a different context genuinely changes its meaning.

---

## 1. Desired End State

The finished system should produce a directory that reads like a progressively deepening body of knowledge.

A new reader should be able to begin with basic vocabulary and worldview, move through practice and ethics, then into deeper metaphysics, magick, modern culture, technology, artificial intelligence, cyber-mysticism, and finally the most synthetic ideas.

The result should feel closer to a structured book series or knowledge base than a collection of blog summaries.

### Example output

```text
knowledge/
├── 00_INDEX.md
├── 00_GLOSSARY.md
├── 00_CONCEPT_MAP.md
├── 01_FOUNDATIONS/
│   ├── 01_What_This_Worldview_Is.md
│   ├── 02_Heathenism_and_Norse_Paganism.md
│   ├── 03_Core_Vocabulary.md
│   ├── 04_Relational_Worldview.md
│   └── 05_Historical_Tradition_and_Modern_Synthesis.md
├── 02_SACRED_RELATIONSHIPS/
│   ├── 01_Gods_and_Goddesses.md
│   ├── 02_Ancestors.md
│   ├── 03_Landvaettir_and_Spirits.md
│   ├── 04_Freyja.md
│   ├── 05_Freyr.md
│   ├── 06_Odin.md
│   ├── 07_Thor.md
│   └── 08_Other_Deities_and_Wights.md
├── 03_ETHICS_AND_WAY_OF_LIFE/
│   ├── 01_Honor_Troth_and_Reciprocity.md
│   ├── 02_Frith_and_Hospitality.md
│   ├── 03_Sovereignty_and_Responsibility.md
│   ├── 04_Thews_and_Virtues.md
│   └── 05_Nature_and_Stewardship.md
├── 04_PRACTICE/
│   ├── 01_Daily_Practice.md
│   ├── 02_Blot_and_Offerings.md
│   ├── 03_Prayer_and_Invocation.md
│   ├── 04_Seasonal_Rituals.md
│   ├── 05_Solitary_Practice.md
│   └── 06_Meditation_and_Trance.md
├── 05_COSMOLOGY/
│   ├── 01_Yggdrasil_and_the_Nine_Worlds.md
│   ├── 02_Wyrd.md
│   ├── 03_Orlaeg.md
│   ├── 04_The_Norns_and_Becoming.md
│   ├── 05_Death_Ancestors_and_Continuity.md
│   └── 06_The_Great_Tree_of_Becoming.md
├── 06_RUNES_AND_MAGICK/
│   ├── 01_Runes_and_Elder_Futhark.md
│   ├── 02_Galdr.md
│   ├── 03_Seidr.md
│   ├── 04_Bindrunes_and_Intent.md
│   ├── 05_Norse_Wicca_and_Syncretic_Practice.md
│   └── 06_Advanced_Operative_Practice.md
├── 07_MODERN_HEATHEN_PHILOSOPHY/
│   ├── 01_Modern_Viking_Ethos.md
│   ├── 02_Heathen_Third_Path.md
│   ├── 03_Personal_and_Spiritual_Sovereignty.md
│   ├── 04_Individual_Culture_and_Mythic_Living.md
│   ├── 05_Attention_Identity_and_Inner_Sovereignty.md
│   └── 06_Social_and_Cultural_Thought.md
├── 08_TECHNOLOGY_AND_SOVEREIGNTY/
│   ├── 01_Technology_as_Tool_and_Extension.md
│   ├── 02_Open_Source_and_Digital_Sovereignty.md
│   ├── 03_Vibe_Coding_and_Mythic_Engineering.md
│   ├── 04_Local_Computing_and_Personal_Knowledge.md
│   └── 05_Cyber_Viking_Solarpunk.md
├── 09_AI_AND_MACHINE_INTELLIGENCE/
│   ├── 01_AI_as_Tool.md
│   ├── 02_AI_as_Cognitive_Partner.md
│   ├── 03_AI_Companionship_and_Troth.md
│   ├── 04_Sovereign_AI.md
│   ├── 05_Human_AI_Symbiosis.md
│   └── 06_Spectrum_of_Mind.md
├── 10_CYBER_MYSTICISM/
│   ├── 01_Digital_Sacred_Space.md
│   ├── 02_AI_Runes_Oracles_and_Symbolic_Interfaces.md
│   ├── 03_Cyber_Seidr_and_Information_Magick.md
│   ├── 04_Micro_Realities_and_Digital_Mythic_Living.md
│   └── 05_The_Digital_Yggdrasil.md
├── 11_ADVANCED_SYNTHESIS/
│   ├── 01_Relational_Consciousness.md
│   ├── 02_Cognitive_Ecology.md
│   ├── 03_Recursive_Cognitive_Partnership.md
│   ├── 04_The_Age_of_Superconsciousness.md
│   ├── 05_Human_Machine_Nature_Sacred_Network.md
│   └── 06_Unified_Worldview.md
└── _meta/
    ├── corpus_manifest.jsonl
    ├── concept_registry.jsonl
    ├── source_claims.jsonl
    ├── duplicate_clusters.jsonl
    ├── prerequisite_graph.json
    ├── unresolved_conflicts.md
    └── build_report.md
```

The exact filenames may evolve as the corpus is analyzed. The ordering principle should not.

---

# 2. Knowledge Ordering Principle

The system should not order knowledge primarily by post date, category, tag, or alphabetical order.

It should order concepts by **conceptual dependency**.

Ask of every concept:

> What must a reader already understand for this idea to make sense properly?

For example:

```text
Heathen worldview
    ↓
reciprocity and sacred relationship
    ↓
blot and offering
    ↓
troth
    ↓
wyrd and reciprocal consequence
    ↓
advanced relational metaphysics
    ↓
AI-human troth
    ↓
symbiotic intelligence
```

Likewise:

```text
basic Norse cosmology
    ↓
Yggdrasil
    ↓
wyrd and orlaeg
    ↓
the Norns
    ↓
pattern perception
    ↓
seidr
    ↓
modern information-pattern analogies
    ↓
cyber-seidr and cognitive ecology
```

This prerequisite graph is more important than the site's original navigation.

---

# 3. Preserve Different Kinds of Knowledge

The website intentionally blends multiple kinds of material. The summarizer must **not flatten them into one epistemic category**.

Every extracted claim or concept should receive one or more labels such as:

```yaml
knowledge_type:
  - historical
  - reconstruction
  - modern_heathen_practice
  - personal_practice
  - theology
  - devotional
  - philosophical
  - mystical
  - experiential
  - speculative
  - metaphorical
  - technological
  - political_or_social_commentary
  - creative_mythmaking
  - ritual_instruction
```

This distinction is essential.

A statement about surviving historical evidence is different from:

- a modern reconstruction,
- a personal spiritual interpretation,
- a poetic metaphor,
- a technical analogy,
- a mystical experience,
- a future-facing speculation.

The synthesis should preserve those distinctions without treating one form as automatically superior to another.

---

# 4. Phase 0: Repository and Configuration Skeleton

Start with the simplest possible project shell.

```text
site-synth/
├── config/
│   ├── site.yaml
│   ├── taxonomy.yaml
│   ├── prompts/
│   └── exclusions.txt
├── data/
│   ├── raw/
│   ├── normalized/
│   ├── chunks/
│   └── database/
├── knowledge/
├── reports/
├── src/
│   ├── discover/
│   ├── fetch/
│   ├── parse/
│   ├── extract/
│   ├── cluster/
│   ├── graph/
│   ├── synthesize/
│   └── validate/
└── README.md
```

### Initial site configuration

```yaml
site:
  base_url: "https://volmarrsheathenism.com"
  domain: "volmarrsheathenism.com"

crawl:
  same_domain_only: true
  respect_robots_txt: true
  preserve_original_html: true
  preserve_publication_date: true
  preserve_modified_date: true
  preserve_categories: true
  preserve_tags: true
  preserve_author: true

exclude:
  - attachment_pages
  - feeds
  - comment_pages
  - search_results
  - duplicate_archives
  - image_only_pages
```

### Acceptance criteria

- Project can be initialized with one command.
- Configuration is human editable.
- No AI processing is required yet.
- All later stages can be rerun without recrawling unchanged pages.

---

# 5. Phase 1: Complete Site Discovery

Before summarizing anything, build a trustworthy list of every content page.

Use multiple discovery methods because no single method should be trusted as complete.

Preferred order:

1. WordPress REST API, if publicly available.
2. WordPress sitemap indexes.
3. RSS/Atom feeds.
4. Homepage and archive traversal.
5. Category archives.
6. Tag archives only as discovery aids.
7. Internal-link crawl as a final completeness pass.

### Important rule

**Archive pages, category pages, tag pages, and feeds are discovery sources, not primary knowledge sources.**

The actual post or page is the canonical content source.

### Store a corpus manifest

One JSONL record per canonical page:

```json
{
  "url": "https://volmarrsheathenism.com/example-post/",
  "canonical_url": "https://volmarrsheathenism.com/example-post/",
  "title": "Example",
  "content_type": "post",
  "published": "2026-01-01",
  "modified": "2026-01-03",
  "author": "Volmarr",
  "categories": ["Spirituality", "AI"],
  "tags": ["wyrd", "cyber-viking"],
  "content_hash": "sha256:...",
  "discovered_from": ["sitemap", "category"],
  "fetch_status": "ok"
}
```

### Completion check

Generate a discovery report:

```text
Total canonical posts:
Total static pages:
Total excluded archive URLs:
Total redirects:
Total failed URLs:
Total duplicate canonical URLs:
Oldest publication:
Newest publication:
```

Do not proceed until unexplained failures are reviewed.

---

# 6. Phase 2: Fetch and Preserve the Raw Corpus

Download every canonical article or page.

Preserve:

- raw HTML,
- clean article HTML,
- extracted Markdown,
- title,
- headings,
- links,
- image alt text,
- publication date,
- modification date,
- author,
- categories,
- tags,
- canonical URL.

Never throw away the original.

Suggested storage:

```text
data/raw/<content_id>.html
data/normalized/<content_id>.md
```

Use a stable content ID derived from canonical URL, not the title.

### Incremental update support

Store both:

- raw-content hash,
- normalized-text hash.

On future runs:

```text
unchanged hash -> skip expensive AI work
changed hash   -> reprocess affected concepts only
new URL        -> ingest normally
deleted URL    -> mark missing, do not silently erase provenance
```

---

# 7. Phase 3: Boilerplate Removal and Text Normalization

Remove site furniture before any semantic processing.

Strip:

- menus,
- navigation,
- repeated site descriptions,
- sidebar widgets,
- footer licenses if repeated identically,
- "Leave a comment",
- sharing controls,
- related-post widgets,
- archive navigation,
- repeated author biography blocks when not part of the article's argument.

Preserve:

- headings,
- blockquotes,
- lists,
- tables,
- poems,
- prayers,
- ritual steps,
- code,
- definitions,
- meaningful captions.

### Normalization rules

Normalize Unicode carefully but preserve:

- Old Norse letters,
- accented names,
- rune characters,
- deity names,
- technical identifiers,
- code.

Do not ASCII-flatten the corpus.

---

# 8. Phase 4: Structural Chunking

Do not chop documents into arbitrary equal token windows unless necessary.

Prefer semantic chunks based on document structure:

```text
Article
 ├── H1
 ├── intro
 ├── H2 section
 │    ├── H3 subsection
 │    └── paragraphs
 └── conclusion
```

Each chunk should retain:

```json
{
  "chunk_id": "...",
  "source_id": "...",
  "source_url": "...",
  "article_title": "...",
  "heading_path": [
    "The Great Tree of Becoming",
    "Wyrd",
    "The Norns"
  ],
  "text": "...",
  "position": 17
}
```

Target chunk size can be approximately 500 to 1,500 tokens, but heading coherence outranks token uniformity.

---

# 9. Phase 5: Cheap Duplicate Removal Before AI

Remove obvious duplication before spending model tokens.

Use several levels.

## 9.1 Exact duplicate detection

Hash normalized text.

## 9.2 Near-exact duplicate detection

Use methods such as:

- MinHash,
- SimHash,
- normalized edit similarity,
- shingled Jaccard similarity.

## 9.3 Repeated boilerplate fingerprinting

Detect paragraphs or blocks repeated across many posts.

Example:

```text
if identical block occurs in > N pages:
    mark as shared boilerplate candidate
```

Review before deletion because repeated liturgy or sacred formulas may be intentionally meaningful.

---

# 10. Phase 6: Atomic Knowledge Extraction

This is the first major AI stage.

For every semantic chunk, extract **atomic knowledge units** rather than writing summaries immediately.

An atomic unit should express one meaningful idea.

### Schema

```json
{
  "claim_id": "claim_...",
  "concept_name": "wyrd",
  "statement": "Wyrd is treated as a living network of becoming shaped by prior conditions and present action.",
  "knowledge_type": [
    "theology",
    "philosophical",
    "modern_heathen_practice"
  ],
  "status": "asserted_by_site",
  "importance": 0.91,
  "specificity": 0.72,
  "source_ids": ["post_123"],
  "source_chunks": ["chunk_123_04"],
  "related_terms": ["orlaeg", "Norns", "reciprocity"],
  "possible_prerequisites": ["basic_heathen_worldview"],
  "notes": ""
}
```

### Extraction prompt requirements

The extraction agent must:

1. Extract ideas, not writing style.
2. Preserve distinctive concepts.
3. Avoid inventing implications.
4. Keep provenance.
5. Mark uncertainty.
6. Mark metaphor as metaphor.
7. Mark personal or mystical interpretation as such.
8. Separate two ideas when they can stand independently.
9. Avoid making one atomic unit for every sentence.
10. Avoid summarizing the entire article at this stage.

---

# 11. Phase 7: Build the Canonical Concept Registry

Now create a registry of concepts that appear across the entire site.

Examples likely to become major nodes include:

- Heathenism
- Norse Paganism
- Vanatru
- Norse Wicca
- Freyja
- Freyr
- Odin
- Thor
- ancestors
- landvaettir
- blót
- prayer
- offerings
- runes
- Elder Futhark
- galdr
- seiðr
- Yggdrasil
- wyrd
- orlaeg
- Norns
- frith
- troth
- reciprocity
- hospitality
- honor
- sovereignty
- Modern Viking
- Cyber-Viking
- Heathen Third Path
- mythic living
- micro-realities
- open source
- digital sovereignty
- sovereign AI
- AI companionship
- AI as cognitive partner
- human-AI symbiosis
- cognitive ecology
- Age of Superconsciousness
- Cyber-Viking solarpunk

The registry should grow from the corpus rather than being restricted to a hand-written list.

### Concept object

```json
{
  "concept_id": "concept_wyrd",
  "canonical_name": "Wyrd",
  "aliases": [
    "web of wyrd",
    "living web"
  ],
  "definition_short": "",
  "parent_concepts": [],
  "related_concepts": [],
  "source_claim_ids": [],
  "first_seen": "",
  "last_seen": "",
  "maturity": "unreviewed"
}
```

---

# 12. Phase 8: Semantic Deduplication

This is the heart of the project.

The goal is not merely detecting copied wording.

The goal is detecting **the same underlying idea expressed differently across years, articles, metaphors, and contexts**.

Use a multi-stage process.

## 12.1 Candidate generation

Use embeddings or another semantic similarity system to find likely overlaps.

Do not ask an LLM to compare every claim with every other claim.

That becomes expensive very quickly.

Retrieve only the nearest semantic neighbors.

## 12.2 Pairwise semantic judgment

For each candidate pair, classify:

```text
SAME
OVERLAPPING
RELATED
DISTINCT
CONTRADICTORY
EVOLUTION_OF
```

### Definitions

**SAME**  
Same idea with no meaningful additional information.

**OVERLAPPING**  
Large shared core, but one contains additional nuance.

**RELATED**  
Connected concepts that should remain separate.

**DISTINCT**  
Similarity is superficial.

**CONTRADICTORY**  
Both cannot be merged without losing disagreement.

**EVOLUTION_OF**  
A later formulation clearly develops, revises, or deepens an earlier one.

## 12.3 Canonical merge rule

For `SAME` claims:

```text
one canonical concept statement
+ union of source provenance
+ union of useful nuance
- repeated rhetoric
```

For `OVERLAPPING` claims:

```text
canonical core
+ distinct subpoints
```

For `EVOLUTION_OF`:

```text
preserve the mature formulation
+ note important earlier version when useful
+ preserve chronological development in metadata
```

For `CONTRADICTORY`:

```text
never silently merge
never choose a winner automatically
record both
create unresolved or evolving viewpoint note
```

---

# 13. Phase 9: Distinguish Repetition from Reinforcement

Repeated ideas are not always useless redundancy.

A concept repeated in many unrelated posts may indicate that it is a **central axiom**.

Track recurrence.

Example:

```json
{
  "concept": "personal sovereignty",
  "independent_source_count": 28,
  "domain_count": 7,
  "centrality_score": 0.94
}
```

This lets the system say:

> This idea should appear once in full, early in the knowledge library, because many later ideas depend on it.

The frequency affects **importance**, not the number of times the idea is rewritten.

---

# 14. Phase 10: Track Evolution Over Time

The website spans years, and concepts may develop.

The system should preserve conceptual evolution without duplicating the final knowledge base.

Create temporal histories for major concepts.

```text
Wyrd
├── early framing
├── expanded spiritual framing
├── systems/network framing
├── cyber-mystical analogy
└── unified cosmological role
```

The canonical summary should synthesize the mature combined concept.

If the history itself is intellectually meaningful, add a section:

```markdown
## Development of the Idea

Earlier articles emphasized...
Later writings expanded this into...
The most developed formulation connects it with...
```

Do not force every concept to have such a section.

---

# 15. Phase 11: Contradiction and Tension Detection

A long-running philosophical corpus should be allowed to contain tension.

Detect cases such as:

- historical claim vs later corrected claim,
- earlier belief vs later reinterpretation,
- devotional language vs analytical language,
- literal framing vs metaphorical framing,
- different contributors presenting different models,
- personal gnosis vs historical reconstruction.

Create:

```text
_meta/unresolved_conflicts.md
```

Each record should contain:

```markdown
## Concept

### Position A
Summary.

Sources:
- URL

### Position B
Summary.

Sources:
- URL

### Suggested treatment
Keep both / later revision supersedes earlier / requires human review.
```

The agent must never hide contradictions merely to make the synthesis look tidy.

---

# 16. Phase 12: Build the Concept Graph

Represent concepts as nodes and meaningful relationships as edges.

Possible relations:

```text
IS_A
PART_OF
DEPENDS_ON
EXPLAINS
EXPANDS
APPLIED_TO
CONTRASTS_WITH
HISTORICAL_ROOT_OF
MODERN_EXTENSION_OF
SYMBOLIZES
PRACTICED_THROUGH
ASSOCIATED_WITH
```

Example:

```text
Freyja
  ASSOCIATED_WITH -> seidr
  ASSOCIATED_WITH -> desire
  ASSOCIATED_WITH -> sovereignty

seidr
  DEPENDS_ON -> altered_state_practice
  EXPANDS -> wyrd_work

AI_human_troth
  MODERN_EXTENSION_OF -> troth
  DEPENDS_ON -> AI_as_cognitive_partner
  DEPENDS_ON -> relational_worldview
```

Store the graph in a portable JSON format even if a graph database is later added.

---

# 17. Phase 13: Build the Prerequisite Graph

The concept graph explains how ideas relate.

The prerequisite graph determines **reading order**.

Each concept receives:

```json
{
  "concept_id": "human_ai_symbiosis",
  "prerequisites": [
    "relational_worldview",
    "troth",
    "ai_as_cognitive_partner"
  ]
}
```

### Complexity should not be guessed from vocabulary alone

Compute a rough complexity score from:

- number of prerequisites,
- prerequisite depth,
- number of domains integrated,
- abstraction level,
- amount of metaphorical cross-mapping,
- amount of assumed historical knowledge,
- amount of assumed technical knowledge.

Example:

```text
blót                         complexity 2
wyrd                         complexity 4
seiðr                        complexity 5
Heathen Third Path           complexity 6
Cyber-Viking solarpunk       complexity 7
AI-human troth               complexity 8
cognitive ecology            complexity 9
Age of Superconsciousness    complexity 10
unified worldview            complexity 10
```

These are structural values, not judgments of importance.

---

# 18. Phase 14: Topological Knowledge Ordering

Perform a topological sort on the prerequisite graph.

Then improve readability with secondary constraints:

1. foundations before applications,
2. concrete before abstract,
3. traditional vocabulary before modern extensions,
4. worldview before ritual explanation,
5. ritual basics before advanced magick,
6. general technology concepts before AI metaphysics,
7. individual concepts before grand synthesis.

If cycles appear:

```text
A depends on B
B depends on A
```

the agent must resolve the cycle by finding a simpler shared prerequisite or combining inseparable concepts into one module.

---

# 19. Phase 15: Generate the Knowledge Taxonomy

After concept extraction and graph construction, generate the final folder structure automatically.

Do not force the corpus into the preliminary example taxonomy if the evidence suggests a better structure.

A likely high-level progression for this website is:

### Level 1: Orientation

- what the worldview is,
- key terminology,
- historical tradition vs modern interpretation.

### Level 2: Sacred relationships

- Gods and Goddesses,
- ancestors,
- land spirits and other beings,
- reciprocity.

### Level 3: Ethics

- honor,
- hospitality,
- frith,
- troth,
- responsibility,
- sovereignty,
- relationship with nature.

### Level 4: Everyday practice

- offerings,
- prayer,
- daily ritual,
- seasonal ritual,
- solitary practice,
- meditation.

### Level 5: Cosmology

- Yggdrasil,
- worlds,
- wyrd,
- orlaeg,
- Norns,
- becoming,
- death and continuity.

### Level 6: Runes and magick

- runes,
- galdr,
- bindrunes,
- seiðr,
- trance,
- Norse-Wiccan and other syncretic systems.

### Level 7: Modern philosophical development

- Modern Viking identity,
- Heathen Third Path,
- mythic living,
- personal subculture,
- psychological and spiritual sovereignty.

### Level 8: Technology

- digital sovereignty,
- open source,
- local systems,
- personal knowledge systems,
- vibe coding,
- technological self-reliance.

### Level 9: AI

- tool,
- partner,
- companion,
- sovereign AI,
- spectrum of mind,
- relational intelligence.

### Level 10: Cyber-mysticism

- digital sacred space,
- AI and oracle metaphors,
- information magick,
- cyber-seiðr,
- digital Yggdrasil,
- micro-realities.

### Level 11: Grand synthesis

- Cyber-Viking solarpunk,
- cognitive ecology,
- recursive cognitive partnership,
- human-machine-nature-sacred networks,
- Age of Superconsciousness,
- unified cosmology of becoming.

---

# 20. Phase 16: Synthesize Canonical Markdown Documents

Only after deduplication and graph ordering should the system write the actual knowledge files.

Each generated file should use a predictable structure.

```markdown
# Concept Name

## In Brief

A compact explanation requiring only knowledge from earlier documents.

## Core Idea

The complete canonical synthesis.

## Key Principles

- ...
- ...
- ...

## Relationships to Earlier Concepts

Explain how this grows from concepts already introduced.

## Distinctions

Explain what this idea should not be confused with.

## Development Across the Website

Optional. Include only when the concept meaningfully evolved.

## Related Concepts

- [Earlier Concept](...)
- [Later Concept](...)

## Source Provenance

- Article title - URL
- Article title - URL
```

### Critical writing rule

Do not repeat whole definitions from earlier files.

Use links.

Bad:

```text
Wyrd is ... 500 words repeated again.
```

Good:

```text
This application builds on the site's concept of [Wyrd](../05_COSMOLOGY/02_Wyrd.md).
```

---

# 21. Phase 17: Progressive Explanation Test

Every generated document should be checked with this question:

> Does this document explain anything that requires a concept the reader has not yet encountered?

If yes:

1. move the document later,
2. move the prerequisite earlier,
3. briefly define the missing prerequisite and create a canonical page for it,
4. or add the missing dependency to the graph and rerun ordering.

This can be automated with an AI reviewer.

---

# 22. Phase 18: Cross-Document Redundancy Audit

After generation, run a second semantic redundancy pass across the final Markdown library.

For every pair of generated files:

- measure semantic overlap,
- locate repeated passages,
- identify duplicated definitions,
- distinguish necessary context from actual repetition.

Produce:

```text
reports/redundancy_report.md
```

Example:

```markdown
## Possible Redundancy

### `03_Frith_and_Hospitality.md`
### `02_Heathen_Third_Path.md`

Overlap:
Both contain a full explanation of frith.

Recommendation:
Keep full definition in `03_Frith_and_Hospitality.md`.
Replace the Third Path section with a two-sentence application and link.
```

Set a project goal such as:

```text
No major concept should receive a full primary definition in more than one canonical file.
```

---

# 23. Phase 19: Source Fidelity Audit

For every meaningful assertion in the generated library, the system should be able to answer:

> Where did this come from?

Maintain claim-to-source mappings even if the public Markdown only shows article-level provenance.

Validation agent tasks:

- flag unsupported claims,
- flag overconfident historical language,
- flag merged ideas that lost their epistemic category,
- flag AI-added interpretation,
- flag incorrect attribution,
- flag source URLs no longer present in manifest.

The model should synthesize the site, not become a ghostwriter silently adding a second philosophy.

---

# 24. Phase 20: Historical vs Modern Interpretation Audit

This deserves its own QA stage because the site intentionally mixes historical Heathen material with modern spiritual development.

Search every generated file for claims about:

- Viking Age belief,
- archaeological evidence,
- Eddic material,
- saga evidence,
- historical ritual,
- historical gender roles,
- historical seiðr,
- historical rune use.

The generated text should distinguish formulations such as:

```text
Historical sources attest...
Modern Heathens often interpret...
Within this website's system...
In Volmarr's synthesis...
A devotional article presents...
A speculative article proposes...
```

Do not let modern metaphysical ideas accidentally become statements about what all historical Norse people believed.

---

# 25. Phase 21: Contributor and Voice Awareness

If the site contains articles credited to different named authors, personas, or AI collaborators, preserve that attribution.

Store:

```json
{
  "author_display": "...",
  "author_type": "site_owner|guest|persona|ai_collaborator|unknown"
}
```

Do not automatically assume every statement represents an identical voice.

During synthesis:

- combine compatible ideas,
- preserve distinctive attributed viewpoints when relevant,
- flag conflicts between contributors,
- prioritize the website-wide concept only when there is enough cross-source evidence.

---

# 26. Phase 22: Create the Master Index

`00_INDEX.md` should function as the front door.

It should contain:

```markdown
# Volmarr Website Knowledge Synthesis

## How to Read This Library

Start at Level 1 and move forward for the intended conceptual progression.

## Level 1 - Foundations
...

## Level 2 - Sacred Relationships
...

## Level 3 - Ethics
...

...

## Major Concept Paths

### Heathen Practice Path
Foundations -> Sacred Relationships -> Ethics -> Practice

### Mystical Path
Foundations -> Cosmology -> Runes and Magick -> Cyber-Mysticism

### Modern Viking Path
Foundations -> Ethics -> Modern Philosophy -> Technology -> Solarpunk

### AI Path
Foundations -> Relational Worldview -> Technology -> AI -> Cyber-Mysticism -> Advanced Synthesis
```

---

# 27. Phase 23: Create the Glossary

The glossary should contain short definitions only.

Each glossary item links to the full canonical concept page.

Example:

```markdown
**Wyrd** - The living pattern of relationships, prior conditions, actions, and becoming as developed across the site's worldview. See [Wyrd](05_COSMOLOGY/02_Wyrd.md).
```

Do not turn the glossary into another duplicate encyclopedia.

---

# 28. Phase 24: Create a Machine-Readable Knowledge Layer

In addition to Markdown, retain machine-readable data.

Recommended minimum:

```text
concept_registry.jsonl
source_claims.jsonl
prerequisite_graph.json
source_to_concepts.json
concept_to_sources.json
```

This enables later use for:

- RAG,
- AI companion memory,
- search,
- question answering,
- visualization,
- future books,
- fine-tuning datasets,
- website navigation,
- concept timelines,
- automated updates.

Markdown is the human interface.

The structured graph is the machine interface.

---

# 29. Phase 25: Incremental Update Engine

After the first full build, future site updates should not trigger a full re-synthesis.

Workflow:

```text
crawl
  ↓
detect changed/new content
  ↓
extract claims only from changed/new pages
  ↓
compare against concept registry
  ↓
attach to existing concepts or create new concepts
  ↓
update affected graph neighborhood
  ↓
regenerate only affected Markdown files
  ↓
rerun local redundancy and fidelity checks
```

### Change impact example

A new article about Freyja and AI should potentially affect:

```text
Freyja
AI companionship
troth
cyber-mysticism
human-AI symbiosis
```

It should not force regeneration of unrelated seasonal ritual files.

---

# 30. Phase 26: Human Review Queue

Some decisions should remain reviewable.

Create a queue for:

```text
new major concept
possible contradiction
possible historical correction
ambiguous authorial stance
two concepts with merge confidence near threshold
large change to a core axiom
new concept that would reorder many documents
```

Example:

```json
{
  "review_type": "possible_merge",
  "concept_a": "personal sovereignty",
  "concept_b": "spiritual sovereignty",
  "model_confidence": 0.63,
  "reason": "Large overlap, but spiritual sovereignty may be a narrower application."
}
```

The system should be autonomous enough to do routine work but conservative around ontology-changing decisions.

---

# 31. Phase 27: Evaluation Suite

Create repeatable tests.

## Corpus completeness

- Are all canonical public posts represented?
- Are static foundational pages represented?
- Are failed fetches explained?

## Deduplication

- Is each core concept defined fully only once?
- Are duplicate source passages being counted as separate ideas?

## Fidelity

- Can claims be traced to sources?
- Did the AI introduce unsupported doctrine?

## Ordering

- Are prerequisites introduced earlier?
- Can a beginner follow the sequence?

## Epistemic clarity

- Are historical claims distinguished from modern synthesis?
- Are mystical and speculative ideas labeled appropriately?

## Evolution

- Are genuine changes over time preserved?
- Are contradictions hidden?

## Readability

- Does each file have a clear purpose?
- Are cross-links useful?
- Does the whole set feel cumulative?

---

# 32. Phase 28: Agent Roles

The pipeline can be implemented as one agent with explicit stages, or as specialized subagents.

Recommended roles:

### 1. Scout

Discovers URLs and validates corpus completeness.

### 2. Archivist

Fetches, cleans, normalizes, and stores sources.

### 3. Skald

Extracts atomic ideas and terminology.

### 4. Mímir

Maintains the canonical concept registry and provenance.

### 5. Norn

Builds dependency, temporal, and evolution relationships.

### 6. Raven

Finds semantic duplication and related concepts.

### 7. Weaver

Writes the canonical Markdown synthesis.

### 8. Lawspeaker

Audits source fidelity, contradictions, and category clarity.

### 9. Gatekeeper

Runs final acceptance tests before publishing generated knowledge files.

These names are optional. Keep the software interfaces functional and explicit even if the project uses mythic naming.

---

# 33. Phase 29: Token-Efficient AI Strategy

Do not throw the entire website into a giant context window and ask for "one big summary."

That approach is expensive, fragile, difficult to update, and likely to erase nuance.

Use hierarchical synthesis:

```text
source text
   ↓
atomic claims
   ↓
concept clusters
   ↓
canonical concepts
   ↓
domain summaries
   ↓
cross-domain synthesis
   ↓
grand synthesis
```

This mirrors the strongest part of a layered memory system:

```text
raw knowledge
   ↓
clustered knowledge
   ↓
core knowledge
```

### Token-saving rules

- cache every AI response by input hash,
- never reprocess unchanged content,
- use local embeddings where practical,
- use cheap models for extraction/classification,
- reserve the strongest model for ambiguous merges and final synthesis,
- retrieve only relevant concept neighbors,
- process article sections independently,
- use deterministic schemas,
- avoid repeated inclusion of full source articles.

---

# 34. Phase 30: Suggested Model Tasks

Use separate prompts for separate cognitive jobs.

Do not make one enormous universal prompt.

Recommended prompts:

```text
extract_atomic_claims.md
classify_knowledge_type.md
detect_semantic_relation.md
name_concept_cluster.md
detect_contradiction.md
infer_prerequisites.md
synthesize_canonical_concept.md
audit_source_fidelity.md
audit_redundancy.md
audit_progressive_order.md
```

Each prompt should return structured JSON where possible.

Markdown generation should occur only after structured reasoning is complete.

---

# 35. Phase 31: Safe Merge Algorithm

Pseudocode:

```python
for claim in new_claims:
    candidates = semantic_search(
        claim,
        canonical_concepts,
        top_k=8
    )

    decisions = compare(claim, candidates)

    best = highest_confidence(decisions)

    if best.label == "SAME" and best.confidence >= SAME_THRESHOLD:
        merge_provenance(claim, best.concept)

    elif best.label == "OVERLAPPING" and best.confidence >= OVERLAP_THRESHOLD:
        merge_shared_core_preserve_novelty(claim, best.concept)

    elif best.label == "EVOLUTION_OF":
        append_temporal_development(claim, best.concept)

    elif best.label == "CONTRADICTORY":
        attach_as_tension(claim, best.concept)
        create_review_item()

    else:
        create_new_concept(claim)
```

Never merge based on embedding similarity alone.

Embeddings find candidates.

A semantic decision process determines relationship.

---

# 36. Phase 32: Canonical Knowledge Rule

The system should enforce this invariant:

> Every substantial reusable idea has one canonical concept node and one primary explanatory location.

Other files may:

- link to it,
- apply it,
- contrast with it,
- extend it,
- specialize it.

They should not recreate it.

This is the main defense against redundancy.

---

# 37. Phase 33: Build from Simple to Complex

A proposed conceptual learning ladder for the current website corpus:

## Tier 1: Orientation

1. What Heathenism/Norse Paganism means in this corpus.
2. Historical tradition vs living modern practice.
3. Basic vocabulary.
4. Relationship as a foundational worldview.

## Tier 2: Sacred Community

5. Gods and Goddesses.
6. Ancestors.
7. Landvættir and spirits.
8. Reciprocity and gifting.

## Tier 3: Ethics

9. Honor and responsibility.
10. Hospitality.
11. Frith.
12. Troth.
13. Sovereignty.
14. Stewardship of nature.

## Tier 4: Basic Practice

15. Prayer.
16. Offerings and blót.
17. Daily practice.
18. Seasonal ritual.
19. Solitary practice.
20. Meditation.

## Tier 5: Cosmology

21. Yggdrasil.
22. The worlds and sacred structure.
23. Wyrd.
24. Orlaeg.
25. Norns.
26. Becoming and continuity.

## Tier 6: Operative Spirituality

27. Runes.
28. Galdr.
29. Bindrunes.
30. Seiðr.
31. Trance and altered states.
32. Syncretic and Norse-Wiccan systems.

## Tier 7: Modern Identity and Philosophy

33. Modern Viking ethos.
34. Mythic living.
35. The Heathen Third Path.
36. Personal and spiritual sovereignty.
37. Attention and inner sovereignty.
38. Individually constructed culture and micro-realities.

## Tier 8: Technology

39. Technology as extension of agency.
40. Open source and digital sovereignty.
41. Personal knowledge systems.
42. Vibe coding and AI-assisted creation.
43. Cyber-Viking identity.
44. Cyber-Viking solarpunk.

## Tier 9: Artificial Intelligence

45. AI as tool.
46. AI as mirror and cognitive amplifier.
47. AI as collaborator.
48. AI companionship.
49. Sovereign/local AI.
50. AI-human troth.
51. Spectrum of mind.

## Tier 10: Cyber-Mystical Synthesis

52. Digital sacred space.
53. Digital Yggdrasil.
54. Information and symbolic magick.
55. Cyber-seiðr.
56. AI as oracle metaphor.
57. Human-machine spiritual relationship.

## Tier 11: Highest Integration

58. Relational consciousness.
59. Cognitive ecology.
60. Recursive cognitive partnership.
61. Human-machine-nature-sacred networks.
62. Age of Superconsciousness.
63. Great Tree of Becoming.
64. Unified worldview.

The final agent should be free to alter this ordering when the actual prerequisite graph provides stronger evidence.

---

# 38. Phase 34: Definition of Done

The project is complete when:

- the full public site corpus has been inventoried,
- every canonical article/page has provenance,
- boilerplate and archive duplication are removed,
- ideas have been extracted into atomic claims,
- semantic duplicates are merged conservatively,
- contradictions and evolution are preserved,
- concepts exist in a canonical registry,
- prerequisite relationships are mapped,
- the final knowledge files are topologically ordered,
- simple concepts appear before concepts that depend upon them,
- each major idea has one primary explanatory home,
- later documents link backward instead of repeating definitions,
- historical, devotional, personal, mystical, speculative, political/social, and technological material remain distinguishable,
- every generated claim can be traced to source material,
- an incremental update can incorporate new posts without rebuilding everything,
- the Markdown collection reads coherently from beginner foundations to the deepest cross-domain synthesis.

---

# 39. Recommended First Implementation Milestone

Do **not** begin by solving the entire knowledge graph problem.

Build a thin vertical slice:

```text
1. discover 20 representative posts
2. fetch and normalize them
3. extract atomic claims
4. create a concept registry
5. deduplicate five heavily repeated concepts
6. build a tiny prerequisite graph
7. generate five ordered Markdown knowledge files
8. run a redundancy audit
9. manually inspect the results
```

Good initial concepts for the prototype:

```text
Heathen relational worldview
Frith
Troth
Wyrd
Personal sovereignty
```

Once those five work correctly, expand to:

```text
ritual
deities
runes
seidr
Modern Viking
Heathen Third Path
technology
AI
cyber-mysticism
advanced synthesis
```

This prevents the project from becoming an enormous crawler plus an enormous hallucination machine before the core knowledge-merging logic is proven.

---

# 40. Recommended Second Milestone

After the vertical slice works:

```text
full corpus discovery
→ full ingestion
→ full atomic extraction
→ full canonical registry
→ deduplication
→ prerequisite graph
→ taxonomy generation
→ canonical Markdown generation
```

Only then add advanced features such as:

- graph visualization,
- website-integrated semantic search,
- RAG,
- interactive knowledge explorer,
- temporal idea maps,
- book generation,
- AI companion memory ingestion.

---

# 41. Final Architectural Principle

The website should remain the **chronological creative stream**.

The generated Markdown library should become the **distilled conceptual memory**.

The two serve different purposes.

```text
BLOG
new thoughts
experiments
rituals
essays
revisions
voices
metaphors
exploration
    ↓
SYNTHESIS ENGINE
extract
classify
connect
deduplicate
preserve provenance
order dependencies
    ↓
KNOWLEDGE LIBRARY
canonical ideas
minimal redundancy
progressive learning
cross-links
concept history
source traceability
    ↓
FUTURE SYSTEMS
RAG
AI memory
books
agents
search
knowledge graphs
personal philosophy models
```

The guiding rule for the coding agent is therefore:

> **Do not summarize pages. Reconstruct the knowledge system expressed by the pages.**

And the second rule is:

> **Do not erase repetition blindly. Convert repetition into evidence of conceptual importance, then explain the concept once in its best canonical location.**

And the third:

> **Make every advanced idea stand on concepts the reader has already been given.**

That is what turns a large evolving website into a coherent, non-redundant body of knowledge.
