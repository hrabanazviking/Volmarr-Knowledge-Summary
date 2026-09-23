# Prompt: Detect Contradiction and Tension

## Purpose
Identify genuine doctrinal, ethical, or methodological contradictions between two claims across the corpus.

## Input Format
```json
{
  "claim_a": { "text": "string", "source_url": "string", "date": "string" },
  "claim_b": { "text": "string", "source_url": "string", "date": "string" }
}
```

## Guidelines
- Do not falsely reconcile real contradictions just to make the system appear uniform.
- Distinguish between a genuine contradiction (incompatible truth claims) and complementary perspectives (different applications of one root principle).
- Note if Claim B represents a chronological evolution or maturation of Claim A.

## Expected Output Schema
```json
{
  "is_contradiction": boolean,
  "tension_type": "lore_vs_upg" | "earlier_vs_later" | "literal_vs_metaphorical" | "folkish_vs_inclusive" | "other",
  "position_a_summary": "string",
  "position_b_summary": "string",
  "suggested_treatment": "keep_both" | "superseded_by_later" | "human_review_required"
}
```
