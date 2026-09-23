"""Interactive Knowledge Explorer Web App Builder (Milestone 8).
Compiles all 25 canonical concepts, prerequisite edges, glossary terms, and reading paths
into a standalone, zero-dependency, self-contained single-page application: `knowledge/explorer.html`.
"""

import json
import re
from pathlib import Path
from rich.console import Console

console = Console()

class ExplorerBuilder:
    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir)
        self.knowledge_dir = self.root_dir / "knowledge"
        self.db_dir = self.root_dir / "data" / "database"
        self.output_html = self.knowledge_dir / "explorer.html"
        self.meta_html = self.knowledge_dir / "_meta" / "explorer.html"

    def build_explorer(self) -> Path:
        console.print("[bold cyan]Building Standalone Interactive Knowledge Explorer...[/bold cyan]")
        
        registry_file = self.db_dir / "concept_registry.jsonl"
        graph_file = self.db_dir / "prerequisite_graph.json"
        
        concepts = []
        with open(registry_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    concepts.append(json.loads(line))

        graph_data = {}
        if graph_file.exists():
            with open(graph_file, "r", encoding="utf-8") as f:
                graph_data = json.load(f)

        topological_order = graph_data.get("topological_reading_order", [])

        # Read actual document markdown contents
        doc_contents = {}
        for md_path in self.knowledge_dir.rglob("*.md"):
            if "_meta" in md_path.parts or md_path.name.startswith("00_"):
                continue
            text = md_path.read_text(encoding="utf-8")
            clean_stem = re.sub(r"^\d+_", "", md_path.stem).lower()
            doc_contents[clean_stem] = text
            doc_contents[md_path.stem] = text

        # Attach full text and order rank to concepts
        rank_map = {item["slug"]: item.get("rank", idx + 1) for idx, item in enumerate(topological_order)}
        for c in concepts:
            slug = c.get("slug", "")
            c["rank"] = rank_map.get(slug, 99)
            # Find markdown content
            for k in [slug, f"concept_{slug}", slug.replace("concept_", "")]:
                if k in doc_contents:
                    c["markdown_content"] = doc_contents[k]
                    break
            if "markdown_content" not in c:
                c["markdown_content"] = f"# {c['canonical_name']}\n\n{c.get('definition_short', '')}"

        # Sort by topological rank
        concepts.sort(key=lambda x: x["rank"])

        concepts_json_str = json.dumps(concepts, ensure_ascii=False)
        graph_json_str = json.dumps(graph_data, ensure_ascii=False)

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Volmarr Knowledge Explorer | The Heathen Third Path</title>
    <style>
        :root {{
            --bg-primary: #0d1117;
            --bg-secondary: #161b22;
            --bg-tertiary: #21262d;
            --border-color: #30363d;
            --text-primary: #c9d1d9;
            --text-secondary: #8b949e;
            --accent-cyan: #58a6ff;
            --accent-green: #3fb950;
            --accent-gold: #d29922;
            --accent-purple: #bc8cff;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            display: flex;
            height: 100vh;
            overflow: hidden;
        }}
        /* Sidebar */
        #sidebar {{
            width: 360px;
            background: var(--bg-secondary);
            border-right: 1px solid var(--border-color);
            display: flex;
            flex-direction: column;
            flex-shrink: 0;
        }}
        #sidebar-header {{
            padding: 16px;
            border-bottom: 1px solid var(--border-color);
        }}
        #sidebar-header h1 {{
            font-size: 1.1rem;
            color: var(--accent-cyan);
            margin-bottom: 4px;
        }}
        #sidebar-header p {{
            font-size: 0.8rem;
            color: var(--text-secondary);
        }}
        #search-box {{
            margin-top: 10px;
            width: 100%;
            padding: 8px 12px;
            background: var(--bg-primary);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            color: var(--text-primary);
            font-size: 0.9rem;
            outline: none;
        }}
        #search-box:focus {{ border-color: var(--accent-cyan); }}
        #nav-links {{
            display: flex;
            gap: 8px;
            margin-top: 8px;
        }}
        .nav-btn {{
            font-size: 0.75rem;
            padding: 4px 8px;
            background: var(--bg-tertiary);
            border: 1px solid var(--border-color);
            border-radius: 4px;
            color: var(--text-secondary);
            text-decoration: none;
            transition: all 0.2s;
        }}
        .nav-btn:hover {{
            color: var(--accent-cyan);
            border-color: var(--accent-cyan);
        }}
        #concept-list {{
            flex: 1;
            overflow-y: auto;
            padding: 8px;
        }}
        .concept-item {{
            padding: 10px 12px;
            margin-bottom: 4px;
            border-radius: 6px;
            cursor: pointer;
            transition: background 0.15s;
            border: 1px solid transparent;
        }}
        .concept-item:hover {{
            background: var(--bg-tertiary);
        }}
        .concept-item.active {{
            background: rgba(88, 166, 255, 0.15);
            border-color: var(--accent-cyan);
        }}
        .item-rank {{
            font-size: 0.75rem;
            color: var(--accent-gold);
            font-weight: 600;
        }}
        .item-title {{
            font-size: 0.9rem;
            font-weight: 600;
            color: var(--text-primary);
            margin: 2px 0;
        }}
        .item-tier {{
            font-size: 0.7rem;
            color: var(--text-secondary);
        }}
        /* Main View */
        #main {{
            flex: 1;
            display: flex;
            flex-direction: column;
            overflow-y: auto;
            padding: 32px 48px;
            background: var(--bg-primary);
        }}
        #detail-header {{
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 20px;
            margin-bottom: 24px;
        }}
        #detail-rank {{
            font-size: 0.85rem;
            color: var(--accent-gold);
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        #detail-title {{
            font-size: 2rem;
            color: #ffffff;
            margin: 6px 0;
        }}
        #detail-tier {{
            font-size: 0.85rem;
            color: var(--accent-purple);
            font-weight: 500;
        }}
        .badge-list {{
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
            margin-top: 12px;
        }}
        .badge {{
            font-size: 0.7rem;
            padding: 2px 8px;
            background: var(--bg-tertiary);
            border-radius: 12px;
            color: var(--text-secondary);
            border: 1px solid var(--border-color);
        }}
        .section-block {{
            margin-bottom: 24px;
        }}
        .section-block h3 {{
            font-size: 1rem;
            color: var(--accent-cyan);
            margin-bottom: 8px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .section-block p, .section-block li {{
            font-size: 0.95rem;
            line-height: 1.6;
            color: var(--text-primary);
        }}
        .section-block ul {{
            padding-left: 20px;
        }}
        .section-block li {{
            margin-bottom: 6px;
        }}
        .link-pill {{
            display: inline-block;
            padding: 4px 10px;
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            color: var(--accent-cyan);
            font-size: 0.85rem;
            text-decoration: none;
            margin: 4px 4px 4px 0;
            cursor: pointer;
        }}
        .link-pill:hover {{
            border-color: var(--accent-cyan);
            background: var(--bg-tertiary);
        }}
        #pagination-bar {{
            display: flex;
            justify-content: space-between;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid var(--border-color);
        }}
        .page-btn {{
            padding: 8px 16px;
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            color: var(--text-primary);
            cursor: pointer;
            font-size: 0.9rem;
            transition: all 0.2s;
        }}
        .page-btn:hover:not(:disabled) {{
            background: var(--bg-tertiary);
            border-color: var(--accent-cyan);
            color: var(--accent-cyan);
        }}
        .page-btn:disabled {{
            opacity: 0.3;
            cursor: not-allowed;
        }}
    </style>
</head>
<body>

<div id="sidebar">
    <div id="sidebar-header">
        <h1>Volmarr Knowledge Explorer</h1>
        <p>Canonical Heathen Third Path Synthesis</p>
        <div id="nav-links">
            <a href="graph_view.html" class="nav-btn" target="_blank">Visual DAG Graph</a>
            <a href="00_INDEX.md" class="nav-btn" target="_blank">Master Index</a>
            <a href="00_CONCEPT_MAP.md" class="nav-btn" target="_blank">Concept Map</a>
        </div>
        <input type="text" id="search-box" placeholder="Search concepts, principles, runes...">
    </div>
    <div id="concept-list"></div>
</div>

<div id="main">
    <div id="detail-view">
        <div id="detail-header">
            <div id="detail-rank">Concept 01 / 25</div>
            <h2 id="detail-title">Loading...</h2>
            <div id="detail-tier">Tier</div>
            <div class="badge-list" id="detail-badges"></div>
        </div>

        <div class="section-block">
            <h3>In Brief</h3>
            <p id="detail-definition"></p>
        </div>

        <div class="section-block">
            <h3>Key Principles</h3>
            <ul id="detail-principles"></ul>
        </div>

        <div class="section-block">
            <h3>Prerequisites (Must Understand First)</h3>
            <div id="detail-prereqs"></div>
        </div>

        <div class="section-block">
            <h3>Source Provenance</h3>
            <ul id="detail-sources"></ul>
        </div>

        <div id="pagination-bar">
            <button class="page-btn" id="btn-prev">&larr; Previous Concept</button>
            <button class="page-btn" id="btn-next">Next Concept &rarr;</button>
        </div>
    </div>
</div>

<script>
    const CONCEPTS = {concepts_json_str};
    const GRAPH = {graph_json_str};
    let currentIndex = 0;

    const conceptListEl = document.getElementById("concept-list");
    const searchBox = document.getElementById("search-box");

    function renderList(filterText = "") {{
        conceptListEl.innerHTML = "";
        const query = filterText.toLowerCase();

        CONCEPTS.forEach((c, idx) => {{
            const matchName = c.canonical_name.toLowerCase().includes(query);
            const matchDef = (c.definition_short || "").toLowerCase().includes(query);
            const matchPrinciples = (c.core_principles || []).some(p => p.toLowerCase().includes(query));

            if (!filterText || matchName || matchDef || matchPrinciples) {{
                const item = document.createElement("div");
                item.className = `concept-item ${{idx === currentIndex ? "active" : ""}}`;
                item.innerHTML = `
                    <div class="item-rank">#${{String(c.rank).padStart(2, '0')}}</div>
                    <div class="item-title">${{c.canonical_name}}</div>
                    <div class="item-tier">${{c.taxonomy_level}}</div>
                `;
                item.addEventListener("click", () => {{
                    currentIndex = idx;
                    renderDetail();
                    updateListActive();
                }});
                conceptListEl.appendChild(item);
            }}
        }});
    }}

    function updateListActive() {{
        const items = conceptListEl.querySelectorAll(".concept-item");
        items.forEach((item, idx) => {{
            item.classList.toggle("active", idx === currentIndex);
        }});
    }}

    function renderDetail() {{
        const c = CONCEPTS[currentIndex];
        if (!c) return;

        document.getElementById("detail-rank").textContent = `Topological Order #${{String(c.rank).padStart(2, '0')}} of ${{CONCEPTS.length}}`;
        document.getElementById("detail-title").textContent = c.canonical_name;
        document.getElementById("detail-tier").textContent = `Tier: ${{c.taxonomy_level.replace('_', ' ')}}`;

        const badgesEl = document.getElementById("detail-badges");
        badgesEl.innerHTML = (c.knowledge_types || []).map(t => `<span class="badge">${{t}}</span>`).join("");

        document.getElementById("detail-definition").textContent = c.definition_short || "No definition available.";

        const principlesEl = document.getElementById("detail-principles");
        principlesEl.innerHTML = (c.core_principles || []).map(p => `<li>${{p}}</li>`).join("") || "<li>Foundational root axiom</li>";

        // Prerequisites
        const prereqsEl = document.getElementById("detail-prereqs");
        const prereqs = c.prerequisites || [];
        if (prereqs.length > 0) {{
            prereqsEl.innerHTML = prereqs.map(pSlug => {{
                const target = CONCEPTS.find(x => x.slug === pSlug || x.concept_id === pSlug);
                const title = target ? target.canonical_name : pSlug;
                return `<span class="link-pill" onclick="selectBySlug('${{pSlug}}')">${{title}}</span>`;
            }}).join("");
        }} else {{
            prereqsEl.innerHTML = "<p style='color: var(--text-secondary);'>None (Corpus foundational axiom)</p>";
        }}

        // Sources
        const sourcesEl = document.getElementById("detail-sources");
        const urls = c.source_urls || [];
        sourcesEl.innerHTML = urls.map(u => `<li><a href="${{u}}" target="_blank" style="color: var(--accent-cyan); text-decoration: none;">${{u}}</a></li>`).join("") || "<li>Canonical Synthesis</li>";

        // Pagination buttons
        document.getElementById("btn-prev").disabled = currentIndex === 0;
        document.getElementById("btn-next").disabled = currentIndex === CONCEPTS.length - 1;

        document.getElementById("main").scrollTop = 0;
    }}

    function selectBySlug(slug) {{
        const idx = CONCEPTS.findIndex(x => x.slug === slug || x.concept_id === slug);
        if (idx !== -1) {{
            currentIndex = idx;
            renderDetail();
            updateListActive();
        }}
    }}

    document.getElementById("btn-prev").addEventListener("click", () => {{
        if (currentIndex > 0) {{
            currentIndex--;
            renderDetail();
            updateListActive();
        }}
    }});

    document.getElementById("btn-next").addEventListener("click", () => {{
        if (currentIndex < CONCEPTS.length - 1) {{
            currentIndex++;
            renderDetail();
            updateListActive();
        }}
    }});

    searchBox.addEventListener("input", (e) => {{
        renderList(e.target.value);
    }});

    // Initial render
    renderList();
    renderDetail();
</script>
</body>
</html>
"""
        self.output_html.write_text(html_content, encoding="utf-8")
        self.meta_html.parent.mkdir(parents=True, exist_ok=True)
        self.meta_html.write_text(html_content, encoding="utf-8")

        console.print(f"[bold green][OK] Standalone Explorer generated: {self.output_html}[/bold green]")
        return self.output_html

if __name__ == "__main__":
    ExplorerBuilder().build_explorer()
