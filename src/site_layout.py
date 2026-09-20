"""Shared HTML shell for every page of the GitHub Pages site (Phase 15).

All links are relative (section 104 - no local path hardcoding, works when
served from a subpath like https://user.github.io/repo/). `root_prefix` is
"" for top-level pages under docs/ and "../" for one-level-deep pages
(docs/stories/S01.html, docs/characters/salur_kazan.html).
"""

NAV_ITEMS = [
    ("Home", "index.html"),
    ("Dataset", "dataset.html"),
    ("Methodology", "methodology.html"),
    ("Network Explorer", "explorer.html"),
    ("Stories", "stories.html"),
    ("Characters", "characters.html"),
    ("Layers", "layers.html"),
    ("Communities", "communities.html"),
    ("Similarity", "similarity.html"),
    ("Analysis", "analysis.html"),
    ("Evidence", "evidence.html"),
    ("Downloads", "downloads.html"),
    ("Reproduce", "reproduce.html"),
    ("About", "about.html"),
]

DISCLAIMER = (
    "Network metrics are structural representations derived from the encoded dataset and "
    "should not be interpreted as complete literary judgments about character importance."
)


def page(title: str, description: str, active: str, content: str, root_prefix: str = "") -> str:
    nav_html = "\n".join(
        f'<a href="{root_prefix}{href}"{" class=\"active\"" if label == active else ""}>{label}</a>'
        for label, href in NAV_ITEMS
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — Dede Korkut Narrative Networks</title>
<meta name="description" content="{description}">
<link rel="stylesheet" href="{root_prefix}assets/style.css">
</head>
<body>
<header class="site-header">
  <div class="wrap brand-row">
    <div>
      <a class="brand" href="{root_prefix}index.html">Dede Korkut Narrative Networks</a><br>
      <span class="subtitle">A reproducible multilayer network analysis of characters and relations in the Book of Dede Korkut</span>
    </div>
  </div>
  <nav class="main-nav"><div class="wrap">{nav_html}</div></nav>
</header>
<main class="wrap">
{content}
</main>
<footer class="site-footer">
  <div class="wrap">
    <p>{DISCLAIMER}</p>
    <p>Built entirely from files in this repository — no analysis result on this site is hand-typed. See <a href="{root_prefix}reproduce.html">Reproduce</a>.</p>
  </div>
</footer>
</body>
</html>
"""
