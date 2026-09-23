import pytest
from src.cluster.merge_algorithm import SafeMergeEngine

@pytest.fixture
def merge_engine():
    return SafeMergeEngine()

@pytest.fixture
def sample_concept():
    return {
        "concept_id": "concept_relational_worldview",
        "canonical_name": "Relational Worldview",
        "definition_short": "Nothing becomes alone: all beings exist in a reciprocal web of kinship.",
        "core_principles": [
            "Nothing becomes alone.",
            "Reciprocal kinship unites gods, spirits, and humans."
        ]
    }

def test_safe_merge_identical_claim(merge_engine, sample_concept):
    claim = {
        "statement": "Nothing becomes alone.",
        "concept_name": "relational_worldview"
    }
    dec, action = merge_engine.process_incoming_claim(claim, [sample_concept])
    assert dec.label == "SAME"
    assert action == "merge_provenance"
    assert dec.confidence >= 0.85

def test_safe_merge_overlapping_claim(merge_engine, sample_concept):
    claim = {
        "statement": "Nothing becomes alone in the reciprocal web of kinship and land.",
        "concept_name": "relational_worldview"
    }
    dec, action = merge_engine.process_incoming_claim(claim, [sample_concept])
    assert dec.label in ["SAME", "OVERLAPPING"]
    assert dec.target_concept_id == "concept_relational_worldview"

def test_safe_merge_contradictory_claim(merge_engine, sample_concept):
    claim = {
        "statement": "Rejects the illusion that reciprocal kinship unites gods and humans; nature is indifferent.",
        "concept_name": "relational_worldview"
    }
    dec, action = merge_engine.process_incoming_claim(claim, [sample_concept])
    assert dec.label == "CONTRADICTORY"
    assert action == "queue_for_review"

def test_safe_merge_new_concept(merge_engine, sample_concept):
    claim = {
        "statement": "Quantum entanglement in semiconductor superlattices enables cryogenic qubits.",
        "concept_name": "quantum_physics"
    }
    dec, action = merge_engine.process_incoming_claim(claim, [sample_concept])
    assert dec.label == "NEW_CONCEPT"
    assert action == "create_new"
