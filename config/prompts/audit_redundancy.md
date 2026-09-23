# Prompt: Audit Cross-Document Redundancy

## Purpose
Inspect two canonical knowledge documents and calculate conceptual overlap to guarantee the single-canonical-home rule is preserved.

## Input Format
```json
{
  "doc_a": { "name": "string", "text": "string" },
  "doc_b": { "name": "string", "text": "string" }
}
```

## Expected Output Schema
```json
{
  "jaccard_similarity": 0.28,
  "semantic_overlap_score": 0.22,
  "violates_threshold": boolean,
  "repeated_concepts": ["string"],
  "suggested_redirection": "string"
}
```
