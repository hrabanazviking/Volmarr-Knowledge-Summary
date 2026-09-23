from pathlib import Path
from src.synthesize.explorer_builder import ExplorerBuilder

def test_explorer_builder():
    builder = ExplorerBuilder()
    output_html = builder.build_explorer()
    
    assert output_html.exists()
    assert output_html.stat().st_size > 10000
    
    content = output_html.read_text(encoding="utf-8")
    assert "Volmarr Knowledge Explorer" in content
    assert "Relational Worldview" in content
    assert "concept-list" in content
    assert "btn-prev" in content
    assert "btn-next" in content
    assert "search-box" in content
