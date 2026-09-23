from pathlib import Path
from src.synthesize.book_generator import BookGenerator

def test_book_generation():
    generator = BookGenerator()
    output_path = generator.generate_book()
    
    assert output_path.exists(), "Book output file does not exist"
    assert output_path.stat().st_size > 10000, "Book output file is suspiciously small"
    
    text = output_path.read_text(encoding="utf-8")
    assert "# The Heathen Third Path: A Canonical Synthesis" in text
    assert "## Foreword & Epistemic Orientation" in text
    assert "## Table of Contents" in text
    assert "Chapter 1: What This Worldview Is" in text
    assert "Chapter 2: Heathenism and Norse Paganism" in text
    assert "Appendix A: Complete Glossary of Terms" in text
    assert "Appendix B: Prerequisite Graph & Reading Paths" in text
