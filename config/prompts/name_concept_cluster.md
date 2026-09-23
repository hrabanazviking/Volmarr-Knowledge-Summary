# Prompt: Name Concept Cluster

## Purpose
Analyze a cluster of atomic claims and generate a canonical title, slug, and short summary that represents the unified conceptual home.

## Input Format
```json
{
  "claims": ["string"],
  "taxonomy_tier": "string",
  "source_titles": ["string"]
}
```

## Guidelines
1. The name must be concise, dignified, and reflective of Norse Heathen terminology where applicable.
2. Avoid sensationalist blog titles or clickbait phrasing.
3. Provide a one-sentence summary capturing the invariant essence of the concept.

## Expected Output Schema
```json
{
  "canonical_name": "string",
  "slug": "concept_name_slug",
  "definition_short": "string",
  "prerequisite_concepts": ["string"],
  "primary_tier": "string"
}
```
