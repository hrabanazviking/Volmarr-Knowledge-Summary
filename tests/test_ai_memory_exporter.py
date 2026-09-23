from pathlib import Path
from src.export.ai_memory_exporter import AIMemoryExporter

def test_ai_memory_export():
    exporter = AIMemoryExporter()
    memory_pack = exporter.export_memory_pack()
    
    assert "metadata" in memory_pack
    assert "concepts" in memory_pack
    assert len(memory_pack["concepts"]) == 64
    
    first = memory_pack["concepts"][0]
    assert "concept_id" in first
    assert "canonical_name" in first
    assert "definition" in first
    assert "core_principles" in first
    assert "llm_context_prompt" in first
    assert "CANONICAL AXIOM:" in first["llm_context_prompt"]
    
    json_path = Path("data/export/ai_companion_memory.json")
    jsonl_path = Path("data/export/ai_companion_memory.jsonl")
    
    assert json_path.exists()
    assert jsonl_path.exists()
    assert json_path.stat().st_size > 2000
    assert jsonl_path.stat().st_size > 2000
