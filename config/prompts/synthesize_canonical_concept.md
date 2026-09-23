# Prompt: Synthesize Canonical Concept Document

## Purpose
Synthesize a single, definitive Markdown knowledge document for a canonical concept from its deduplicated claims and source provenance.

## Input Format
```json
{
  "concept_name": "string",
  "taxonomy_level": "string",
  "definition_short": "string",
  "prerequisites": ["string"],
  "dependents": ["string"],
  "unique_principles": ["string"],
  "epistemic_types": ["string"],
  "sources": [{ "title": "string", "url": "string", "date": "string" }]
}
```

## Schema Requirements
The generated Markdown must strictly adhere to this section layout:
```markdown
# [Concept Name]

## In Brief
[One-sentence definition]

## Core Idea
[Structured conceptual overview]

## Key Principles
[Bulleted list of deduplicated insights]

## Relationships to Surrounding Concepts
[Prerequisites and downstream applications with relative links]

## Distinctions
[What this concept IS and what it IS NOT]

## Epistemic Character
[Knowledge categories preserved]

## Source Provenance
[Bullet list of markdown links to original articles]
```
