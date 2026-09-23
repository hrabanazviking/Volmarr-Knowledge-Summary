# Prompt: Audit Progressive Explanation Order

## Purpose
Validate that the topological reading order introduces foundational concepts before advanced concepts that depend upon them.

## Input Format
```json
{
  "reading_sequence": [
    { "rank": 1, "concept_id": "string", "prerequisites": ["string"] }
  ]
}
```

## Expected Output Schema
```json
{
  "is_valid_dag_order": boolean,
  "violations": [
    {
      "concept": "string",
      "prerequisite": "string",
      "concept_rank": 5,
      "prerequisite_rank": 8,
      "issue": "Prerequisite appears after dependent concept"
    }
  ]
}
```
