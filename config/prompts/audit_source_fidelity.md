# Prompt: Audit Source Fidelity

## Purpose
Verify that all synthesized principles in a canonical document accurately represent the underlying corpus without hallucination or unsupported doctrinal drift.

## Input Format
```json
{
  "synthesized_text": "string",
  "source_claims": ["string"],
  "raw_excerpts": ["string"]
}
```

## Expected Output Schema
```json
{
  "fidelity_score": 0.98,
  "hallucination_detected": boolean,
  "unsupported_statements": ["string"],
  "recommendations": ["string"]
}
```
