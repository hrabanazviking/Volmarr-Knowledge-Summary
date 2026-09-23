# Prompt: Classify Knowledge Type

## Purpose
Assign precise epistemic category tags to a candidate knowledge claim to preserve epistemic distinctions (historical vs modern UPG vs technical).

## Input Format
```json
{
  "statement": "string",
  "context": "string",
  "source_author": "string"
}
```

## Valid Categories
- `historical`: Attested in Old Norse literature, archaeology, runic inscriptions, or primary academic consensus.
- `reconstruction`: Modern revival attempt to recreate historic rituals or worldview based on comparative Germanic scholarship.
- `modern_heathen_practice`: Established contemporary living Heathen traditions (e.g. contemporary blót formats, heathen holidays).
- `personal_practice`: The author's personal liturgical habits, altar routines, or private devotions.
- `theology`: Doctrinal claims regarding the nature, power, and character of the Gods (Aesir/Vanir).
- `devotional`: Prayers, poems, invocations, and ecstatic expressions of personal love and honor to Holy Powers.
- `philosophical`: Conceptual frameworks, ethics, sovereignty, dialectics, ontology, and worldview analysis.
- `mystical`: Unverified Personal Gnosis (UPG), trance visions, direct energetic experiences, or seidr journeys.
- `speculative`: Hypotheses regarding the future of consciousness, hypothetical models, or creative extrapolation.
- `metaphorical`: Poetic analogies, symbolic correspondences, and psychological archetypes.
- `technological`: Computing, open source, artificial intelligence, cryptographic networks, hardware, or solarpunk systems.
- `political_or_social_commentary`: Critiques of modern society, ideological polarization, culture war resistance.

## Expected Output Schema
```json
{
  "primary_category": "string",
  "secondary_categories": ["string"],
  "rationale": "string",
  "is_upg": boolean
}
```
