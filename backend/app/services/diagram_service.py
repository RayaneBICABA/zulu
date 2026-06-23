from ..extensions import db
from sqlalchemy import inspect as sa_inspect


def _is_abstract(cls):
    return "__abstract__" in cls.__dict__ and cls.__dict__["__abstract__"] is True


def _get_all_models():
    models = []
    seen = set()

    def collect(cls):
        for sub in cls.__subclasses__():
            if sub.__name__ not in seen:
                seen.add(sub.__name__)
                if not _is_abstract(sub):
                    models.append(sub)
                collect(sub)

    collect(db.Model)
    return models


def _get_all_abstract():
    abstracts = []
    seen = set()

    def collect(cls):
        for sub in cls.__subclasses__():
            if sub.__name__ not in seen:
                seen.add(sub.__name__)
                if _is_abstract(sub):
                    abstracts.append(sub)
                collect(sub)

    collect(db.Model)
    return abstracts


def _get_parent(model):
    for cls in model.__mro__[1:]:
        if cls is not db.Model and issubclass(cls, db.Model):
            return cls.__name__
    return None


def _mermaid_type(col):
    try:
        python_type = col.type.python_type.__name__
    except Exception:
        return str(col.type)
    mapping = {
        "int": "int", "str": "string", "datetime": "datetime",
        "bool": "bool", "float": "float", "Decimal": "decimal",
        "bytes": "bytes", "dict": "json",
    }
    return mapping.get(python_type, python_type)


def _safe_inspector(model):
    try:
        return sa_inspect(model)
    except Exception:
        return None


def generate_mermaid():
    models = _get_all_models()
    abstracts = _get_all_abstract()
    lines = ["classDiagram"]

    seen = set()

    for m in abstracts:
        if m.__name__ not in seen:
            seen.add(m.__name__)
            lines.append(f"    class {m.__name__} {{")
            lines.append("        <<abstract>>")
            for key, value in m.__dict__.items():
                if hasattr(value, "type") and hasattr(value, "primary_key"):
                    pk = " (PK)" if value.primary_key else ""
                    nullable = "?" if value.nullable else ""
                    lines.append(f"        +{_mermaid_type(value)}{nullable} {key}{pk}")
            lines.append("    }")

    for m in models:
        if m.__name__ in seen:
            continue
        seen.add(m.__name__)
        parent = _get_parent(m)
        parent_cols = set()
        if parent:
            for am in abstracts:
                if am.__name__ == parent:
                    for key, value in am.__dict__.items():
                        if hasattr(value, "type") and hasattr(value, "primary_key"):
                            parent_cols.add(key)
                    break

        inspector = _safe_inspector(m)
        lines.append(f"    class {m.__name__} {{")
        if inspector:
            for col in getattr(inspector, "columns", []):
                if col.name in parent_cols:
                    continue
                pk = " (PK)" if col.primary_key else ""
                fk = ""
                for fkc in col.foreign_keys:
                    target = fkc.column.table.name
                    target_col = fkc.column.name
                    fk = f" (FK→{target}.{target_col})"
                nullable = "?" if col.nullable else ""
                lines.append(f"        +{_mermaid_type(col)}{nullable} {col.name}{pk}{fk}")
        lines.append("    }")
        if parent:
            lines.append(f"    {m.__name__} --|> {parent} : inherits")

    rels = []
    for m in models + abstracts:
        inspector = _safe_inspector(m)
        if not inspector:
            continue
        for name, rel in getattr(inspector, "relationships", {}).items():
            if rel.direction.name == "MANYTOMANY":
                secondary = rel.secondary.name if rel.secondary is not None else None
                rels.append((m.__name__, rel.mapper.class_.__name__, "many-to-many", name, secondary))
            elif rel.direction.name == "ONETOMANY":
                rels.append((m.__name__, rel.mapper.class_.__name__, "1-->*", name, None))
            elif rel.direction.name == "MANYTOONE":
                rels.append((m.__name__, rel.mapper.class_.__name__, "*-->1", name, None))

    assoc_seen = set()
    for src, tgt, kind, attr, secondary in rels:
        if kind == "many-to-many" and secondary:
            if secondary not in assoc_seen:
                assoc_seen.add(secondary)
                lines.append(f"    class {secondary} {{")
                lines.append("        <<association>>")
                lines.append("    }")
            lines.append(f"    {src} \"*\" --> \"*\" {tgt} : {attr}")
        elif kind == "1-->*":
            lines.append(f"    {src} \"1\" --> \"*\" {tgt} : {attr}")
        elif kind == "*-->1":
            lines.append(f"    {src} \"*\" --> \"1\" {tgt} : {attr}")

    return "\n".join(lines)


def get_html_diagram():
    mermaid_text = generate_mermaid()
    from html import escape
    safe_text = escape(mermaid_text)
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Zulu — Diagramme de classes</title>
<script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ background: #f4f6f9; font-family: system-ui, -apple-system, sans-serif; padding: 24px; }}
  .toolbar {{ display: flex; gap: 12px; align-items: center; margin-bottom: 16px; flex-wrap: wrap; }}
  .toolbar h1 {{ font-size: 20px; color: #08275d; font-weight: 600; }}
  .btn {{ padding: 8px 20px; border: none; border-radius: 6px; font-size: 14px; font-weight: 500; cursor: pointer; background: #c61458; color: #fff; text-decoration: none; transition: opacity .15s; }}
  .btn:hover {{ opacity: .85; }}
  .btn-outline {{ background: transparent; border: 1px solid #c61458; color: #c61458; }}
  .btn-outline:hover {{ background: #c61458; color: #fff; }}
  .diagram-container {{ background: #fff; border-radius: 12px; padding: 32px; box-shadow: 0 1px 3px rgba(0,0,0,.08); overflow-x: auto; min-height: 200px; }}
  .loading {{ color: #08275d; padding: 40px; text-align: center; font-size: 14px; }}
  .raw {{ margin-top: 12px; background: #08275d; color: #e2e8f0; padding: 16px; border-radius: 8px; font-size: 13px; overflow-x: auto; white-space: pre; font-family: 'JetBrains Mono', monospace; display: none; }}
  .footer {{ margin-top: 12px; color: #667085; font-size: 13px; }}
  #mermaidTarget svg {{ max-width: 100%; height: auto; }}
</style>
</head>
<body>
<div class="toolbar">
  <h1>Diagramme de classes</h1>
  <button class="btn" onclick="downloadPNG()">Telecharger PNG</button>
  <button class="btn btn-outline" onclick="toggleRaw()">Code source</button>
  <button class="btn btn-outline" id="copyBtn" onclick="copyCode()">Copier le code</button>
</div>
<div class="diagram-container">
  <div id="mermaidLoading" class="loading">Generation du diagramme...</div>
  <div id="mermaidTarget"></div>
</div>
<pre class="raw" id="raw">{safe_text}</pre>
<div class="footer">Genere automatiquement depuis les models SQLAlchemy.</div>
<script id="mermaidSource" type="text/template">{mermaid_text}</script>
<script>
mermaid.initialize({{ startOnLoad: false, theme: "base", themeVariables: {{
  primaryColor: "#c61458",
  primaryTextColor: "#08275d",
  primaryBorderColor: "#c61458",
  lineColor: "#475569",
  secondaryColor: "#eef2ff",
  tertiaryColor: "#f8fafc",
  mainBkg: "#fff",
  nodeBorder: "#c61458",
  clusterBkg: "#f8fafc",
  clusterBorder: "#cbd5e1",
  titleColor: "#08275d",
  edgeLabelBackground: "#fff",
  nodeTextColor: "#08275d",
}} }});

async function render() {{
  const src = document.getElementById('mermaidSource');
  const target = document.getElementById('mermaidTarget');
  const loading = document.getElementById('mermaidLoading');
  try {{
    const result = await mermaid.render('renderedDiagram', src.textContent.trim());
    loading.style.display = 'none';
    target.innerHTML = result.svg;
    const svgEl = target.querySelector('svg');
    if (svgEl && !svgEl.getAttribute('width')) {{
      const vb = svgEl.getAttribute('viewBox');
      if (vb) {{
        const parts = vb.split(/\\s+/);
        svgEl.setAttribute('width', parts[2]);
        svgEl.setAttribute('height', parts[3]);
      }}
    }}
  }} catch (e) {{
    loading.textContent = 'Erreur de rendu du diagramme.';
    loading.style.color = '#c61458';
  }}
}}

function toggleRaw() {{
  const el = document.getElementById('raw');
  el.style.display = el.style.display === 'block' ? 'none' : 'block';
}}

function copyCode() {{
  const text = document.getElementById('mermaidSource').textContent.trim();
  navigator.clipboard.writeText(text).then(function () {{
    const btn = document.getElementById('copyBtn');
    const orig = btn.textContent;
    btn.textContent = 'Copie !';
    setTimeout(() => {{ btn.textContent = orig; }}, 2000);
  }}).catch(function () {{
    alert('Impossible de copier le code.');
  }});
}}

function downloadPNG() {{
  const svg = document.querySelector('#mermaidTarget svg');
  if (!svg) {{ alert("Diagramme pas encore rendu."); return; }}
  const w = parseInt(svg.getAttribute('width')) || 800;
  const h = parseInt(svg.getAttribute('height')) || 600;
  const svgData = new XMLSerializer().serializeToString(svg);
  const svgBase64 = btoa(unescape(encodeURIComponent(svgData)));
  const dataUrl = 'data:image/svg+xml;base64,' + svgBase64;
  const canvas = document.createElement('canvas');
  canvas.width = w * 2;
  canvas.height = h * 2;
  const ctx = canvas.getContext('2d');
  ctx.scale(2, 2);
  ctx.fillStyle = '#fff';
  ctx.fillRect(0, 0, w, h);
  const img = new Image();
  img.onload = function () {{
    ctx.drawImage(img, 0, 0);
    try {{
      canvas.toBlob(function (b) {{
        if (b) {{
          const a = document.createElement('a');
          a.href = URL.createObjectURL(b);
          a.download = 'diagramme-classes.png';
          a.click();
          return;
        }}
        fallback();
      }});
    }} catch (e) {{ fallback(); }}
  }};
  img.onerror = fallback;
  img.src = dataUrl;
  function fallback() {{
    const a = document.createElement('a');
    a.href = dataUrl;
    a.download = 'diagramme-classes.svg';
    a.click();
  }}
}}

render();
</script>
</body>
</html>"""
