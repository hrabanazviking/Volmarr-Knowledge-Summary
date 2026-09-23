# Prompt: Detect Semantic Relation

## Purpose
Determine the semantic relationship between a new claim and an existing canonical concept node.

## Input Format
```json
{
  "new_claim": "string",
  "canonical_concept": {
    "concept_id": "string",
    "name": "string",
    "definition": "string",
    "core_principles": ["string"]
  }
}
```

## Possible Decision Labels
- `SAME`: Proposition expresses identical semantic meaning (candidate for provenance union and duplicate elimination).
- `OVERLAPPING`: Shares the foundational core but contributes distinct nuance or application.
- `EVOLUTION_OF`: Represents an authorial revision, later maturity, or temporal development of an earlier view.
- `CONTRADICTORY`: Direct logical, doctrinal, or practical conflict with the canonical principle.
- `DISTINCT`: Unrelated concept belonging elsewhere in the taxonomy.

## Expected Output Schema
```json
{
  "relation": "SAME" | "OVERLAPPING" | "EVOLUTION_OF" | "CONTRADICTORY" | "DISTINCT",
  "confidence": 0.88,
  "shared_elements": ["string"],
  "novel_elements": ["string"],
  "recommendation": "merge_provenance" | "append_principle" | "record_tension" | "create_new"
}
```
