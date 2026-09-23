# Prompt: Extract Atomic Claims

## Purpose
Extract discrete, self-contained, atomic knowledge propositions from normalized Markdown source articles without introducing extraneous assumptions.

## Input Format
```json
{
  "article_title": "string",
  "source_url": "string",
  "author": "string",
  "chunk_id": "string",
  "heading_path": ["string"],
  "text": "string"
}
```

## Instructions
1. Read the chunk text carefully.
2. Identify distinct philosophical, theological, ethical, cosmological, historical, or technological claims.
3. Exclude non-substantive personal biographies, marketing copy, social media links, or navigational boilerplate.
4. Each extracted claim must be self-contained so that it can be evaluated without requiring the surrounding paragraph.
5. Assign a specificity score (0.0 to 1.0) and an importance score (0.0 to 1.0).

## Expected Output Schema
```json
{
  "claims": [
    {
      "statement": "string",
      "related_concept_slug": "string",
      "importance": 0.85,
      "specificity": 0.80,
      "knowledge_types": ["historical" | "theology" | "modern_heathen_practice" | "philosophical" | "mystical" | "technological"],
      "confidence": 0.95
    }
  ]
}
```
