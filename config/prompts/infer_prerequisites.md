# Prompt: Infer Conceptual Prerequisites

## Purpose
Determine the strict conceptual dependencies of a concept: what ideas must a reader understand first for this concept to be comprehensible?

## Input Format
```json
{
  "target_concept": {
    "name": "string",
    "definition": "string",
    "core_principles": ["string"]
  },
  "candidate_prerequisites": [
    { "concept_id": "string", "name": "string", "tier": "string" }
  ]
}
```

## Rules
- Complexity alone does not make an idea a dependent; there must be direct semantic reliance.
- Avoid cyclical dependencies ($A 	o B 	o A$).
- Keep prerequisites minimal and direct (transitive reduction).

## Expected Output Schema
```json
{
  "prerequisites": [
    {
      "concept_id": "string",
      "dependency_strength": "CRITICAL" | "HELPFUL",
      "justification": "string"
    }
  ]
}
```
