import json
from pathlib import Path
from src.graph.temporal_evolution import TemporalEvolutionTracker

def test_temporal_evolution_output():
    tracker = TemporalEvolutionTracker()
    data = tracker.build_timeline()
    
    assert "concept_wyrd_and_orlaeg" in data
    assert "concept_heathen_third_path" in data
    assert "concept_ai_cognitive_partner" in data
    assert "concept_cyber_viking_solarpunk" in data
    
    assert len(data["concept_wyrd_and_orlaeg"]["phases"]) == 3
    assert len(data["concept_heathen_third_path"]["phases"]) == 3
    
    json_path = Path("data/database/temporal_evolution.json")
    report_path = Path("reports/temporal_evolution.md")
    
    assert json_path.exists()
    assert report_path.exists()
    assert report_path.stat().st_size > 500
