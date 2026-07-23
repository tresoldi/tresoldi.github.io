#!/usr/bin/env python3
"""Silvæ — a small, hand-rolled static site generator.

Pipeline, one file at a time:

    content/**.md  ──►  Pandoc (Markdown → HTML fragment)  ──►  Jinja2 template  ──►  _site/

No framework. Just Python, Pandoc, and Jinja2. Pandoc gives us footnotes-as-
sidenotes (via filters/sidenotes.lua), citations from a BibTeX file (--citeproc),
MathML, and syntax highlighting for free. Everything else is a few hundred lines
below. See /colophon/ for the rationale.

Usage:
    python build.py            # build into _site/
    python build.py --serve    # build, then serve _site/ at http://localhost:8000
"""
from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import re
import shutil
from pathlib import Path

import yaml
import pypandoc
from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content"
TEMPLATES = ROOT / "templates"
STATIC = ROOT / "static"
DATA = ROOT / "data"
FILTERS = ROOT / "filters"
OUT = ROOT / "_site"

SITE = yaml.safe_load((ROOT / "site.yaml").read_text(encoding="utf-8"))

# Markdown dialect and Pandoc arguments shared by every document.
MD_FORMAT = (
    "markdown"
    "+smart"                 # curly quotes, en/em dashes, ellipses
    "+tex_math_dollars"      # $…$ and $$…$$
    "+footnotes"             # [^1] → sidenotes (see the lua filter)
    "+bracketed_spans"       # [text]{.newthought}
    "+fenced_divs"           # ::: {.fullwidth} … :::
    "+backtick_code_blocks"
)
PANDOC_BASE_ARGS = [
    "--lua-filter", str(FILTERS / "sidenotes.lua"),
    "--mathml",              # self-contained math, no JS
    "--wrap", "none",
]

FRONT_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", re.S)


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def parse_doc(path: Path):
    """Split a file into (front-matter dict, body markdown)."""
    text = path.read_text(encoding="utf-8")
    m = FRONT_RE.match(text)
    if not m:
        return {}, text
    meta = yaml.safe_load(m.group(1)) or {}
    return meta, m.group(2)


def parse_date(value):
    """Accept datetime, date, or a string like '2025-10-06 08:00:00 +0200'."""
    if isinstance(value, dt.datetime):
        return value
    if isinstance(value, dt.date):
        return dt.datetime(value.year, value.month, value.day)
    s = str(value).strip()
    for fmt in ("%Y-%m-%d %H:%M:%S %z", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            return dt.datetime.strptime(s, fmt)
        except ValueError:
            continue
    raise ValueError(f"Unrecognised date: {value!r}")


def render_markdown(body: str, bibliography: str | None = None) -> str:
    """Markdown → HTML fragment through Pandoc."""
    args = list(PANDOC_BASE_ARGS)
    if bibliography:
        args += ["--citeproc", "--bibliography", str(DATA / bibliography)]
    return pypandoc.convert_text(body, "html5", format=MD_FORMAT, extra_args=args)


def render_bibliography(bib_file: str) -> str:
    """Render an entire .bib file as a formatted reference list (single source)."""
    doc = "---\nnocite: |\n  @*\n---\n"
    args = ["--citeproc", "--bibliography", str(DATA / bib_file), "--wrap", "none"]
    return pypandoc.convert_text(doc, "html5", format="markdown", extra_args=args)


def strip_html(s: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s)).strip()


def excerpt(meta: dict, body_html: str, limit: int = 200) -> str:
    if meta.get("summary"):
        return meta["summary"]
    text = strip_html(body_html)
    return (text[:limit].rsplit(" ", 1)[0] + "…") if len(text) > limit else text


def slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def write_page(url_path: str, html_str: str):
    rel = url_path.strip("/")
    dest = OUT / "index.html" if rel == "" else OUT / rel / "index.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(html_str, encoding="utf-8")


# --------------------------------------------------------------------------- #
# Jinja environment
# --------------------------------------------------------------------------- #
env = Environment(
    loader=FileSystemLoader(str(TEMPLATES)),
    autoescape=select_autoescape(["html", "xml"]),
    trim_blocks=True,
    lstrip_blocks=True,
)
env.filters["date"] = lambda d, fmt="%B %-d, %Y": d.strftime(fmt)
env.filters["year"] = lambda d: d.strftime("%Y")
env.filters["isodate"] = lambda d: d.strftime("%Y-%m-%dT%H:%M:%S%z") or d.strftime("%Y-%m-%dT%H:%M:%SZ")


def base_ctx(**kw):
    ctx = {"site": SITE, "build_time": dt.datetime.now(dt.timezone.utc)}
    ctx.update(kw)
    return ctx


# --------------------------------------------------------------------------- #
# Content loading
# --------------------------------------------------------------------------- #
def load_posts():
    posts = []
    for path in sorted((CONTENT / "posts").glob("*.md")):
        meta, body = parse_doc(path)
        if meta.get("draft"):
            continue
        date = parse_date(meta["date"])
        slug = meta.get("slug") or re.sub(r"^\d{4}-\d{2}-\d{2}-", "", path.stem)
        body_html = render_markdown(body, meta.get("bibliography"))
        posts.append({
            "meta": meta,
            "title": meta["title"],
            "date": date,
            "slug": slug,
            "url": f"/writing/{slug}/",
            "tags": meta.get("tags", []) or [],
            "body": body_html,
            "excerpt": excerpt(meta, body_html),
        })
    posts.sort(key=lambda p: p["date"], reverse=True)
    return posts


def load_notes():
    notes = []
    ndir = CONTENT / "notes"
    if not ndir.exists():
        return notes
    for path in sorted(ndir.glob("*.md")):
        meta, body = parse_doc(path)
        if meta.get("draft"):
            continue
        date = parse_date(meta["date"])
        slug = meta.get("slug") or re.sub(r"^\d{4}-\d{2}-\d{2}-", "", path.stem)
        notes.append({
            "meta": meta,
            "date": date,
            "slug": slug,
            "url": f"/notes/{slug}/",
            "body": render_markdown(body),
        })
    notes.sort(key=lambda n: n["date"], reverse=True)
    return notes


# --------------------------------------------------------------------------- #
# Build steps
# --------------------------------------------------------------------------- #
def copy_static():
    if STATIC.exists():
        shutil.copytree(STATIC, OUT, dirs_exist_ok=True)
    for extra in ("CNAME",):
        src = ROOT / extra
        if src.exists():
            shutil.copy2(src, OUT / extra)


def build_posts(posts):
    tpl = env.get_template("post.html")
    for i, post in enumerate(posts):
        newer = posts[i - 1] if i > 0 else None
        older = posts[i + 1] if i + 1 < len(posts) else None
        html_str = tpl.render(base_ctx(
            page=post["meta"], post=post, nav_active="/writing/",
            title=f"{post['title']} — {SITE['title']}",
            description=post["excerpt"],
            canonical=SITE["url"] + post["url"],
            newer=newer, older=older,
        ))
        write_page(post["url"], html_str)


def build_notes(notes):
    tpl = env.get_template("note.html")
    for note in notes:
        html_str = tpl.render(base_ctx(
            page=note["meta"], note=note, nav_active="/notes/",
            title=f"Note — {SITE['title']}",
            description=strip_html(note["body"])[:160],
            canonical=SITE["url"] + note["url"],
        ))
        write_page(note["url"], html_str)


def build_pages(posts):
    """Render everything under content/pages/. index.md and a few pages are special."""
    for path in sorted((CONTENT / "pages").glob("*.md")):
        meta, body = parse_doc(path)
        stem = path.stem
        permalink = meta.get("permalink") or ("/" if stem == "index" else f"/{stem}/")
        template = meta.get("template", "page")
        body_html = render_markdown(body, meta.get("bibliography"))

        extra = {}
        if meta.get("bibliography_list"):
            extra["bibliography_html"] = render_bibliography(meta["bibliography_list"])
        if template == "home":
            extra["posts"] = posts[: SITE.get("home_posts", 5)]
        if template == "software":
            extra["software"] = yaml.safe_load((DATA / "software.yaml").read_text(encoding="utf-8"))
        if template == "blogroll":
            extra["blogroll"] = yaml.safe_load((DATA / "blogroll.yaml").read_text(encoding="utf-8"))

        html_str = env.get_template(f"{template}.html").render(base_ctx(
            page=meta, content=body_html,
            nav_active=meta.get("nav_active", permalink),
            title=meta.get("head_title") or (SITE["title"] if stem == "index"
                  else f"{meta.get('title', stem.title())} — {SITE['title']}"),
            description=meta.get("description", SITE["description"]),
            canonical=SITE["url"] + permalink,
            **extra,
        ))
        write_page(permalink, html_str)


def build_writing_index(posts):
    by_year = {}
    for p in posts:
        by_year.setdefault(p["date"].year, []).append(p)
    years = sorted(by_year.items(), reverse=True)
    tags = {}
    for p in posts:
        for t in p["tags"]:
            tags.setdefault(t, []).append(p)
    html_str = env.get_template("list.html").render(base_ctx(
        posts=posts, years=years, tags=sorted(tags.items()),
        nav_active="/writing/",
        title=f"Writing — {SITE['title']}",
        description="Essays on linguistics, computation, and academic life.",
        canonical=SITE["url"] + "/writing/",
    ))
    write_page("/writing/", html_str)


def build_notes_index(notes):
    html_str = env.get_template("notes.html").render(base_ctx(
        notes=notes, nav_active="/notes/",
        title=f"Notes — {SITE['title']}",
        description="Short-form notes and observations.",
        canonical=SITE["url"] + "/notes/",
    ))
    write_page("/notes/", html_str)


def build_feeds(posts):
    items = posts[: SITE.get("feed_posts", 20)]
    atom = env.get_template("feed.xml").render(base_ctx(posts=items))
    (OUT / "feed.xml").write_text(atom, encoding="utf-8")

    feed = {
        "version": "https://jsonfeed.org/version/1.1",
        "title": SITE["title"],
        "home_page_url": SITE["url"] + "/",
        "feed_url": SITE["url"] + "/feed.json",
        "description": SITE["description"],
        "authors": [{"name": SITE["author"], "url": SITE["url"] + "/"}],
        "language": SITE["lang"],
        "items": [{
            "id": SITE["url"] + p["url"],
            "url": SITE["url"] + p["url"],
            "title": p["title"],
            "content_html": p["body"],
            "summary": p["excerpt"],
            "date_published": p["date"].strftime("%Y-%m-%dT%H:%M:%S%z") or p["date"].isoformat(),
            "tags": p["tags"],
        } for p in items],
    }
    (OUT / "feed.json").write_text(json.dumps(feed, indent=2, ensure_ascii=False), encoding="utf-8")


def build_sitemap(urls):
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in sorted(set(urls)):
        lines.append(f"  <url><loc>{html.escape(SITE['url'] + u)}</loc></url>")
    lines.append("</urlset>")
    (OUT / "sitemap.xml").write_text("\n".join(lines), encoding="utf-8")
    (OUT / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\nSitemap: {SITE['url']}/sitemap.xml\n", encoding="utf-8")


def build_404():
    html_str = env.get_template("404.html").render(base_ctx(
        nav_active="", title=f"Not found — {SITE['title']}",
        description="Page not found.", canonical=SITE["url"] + "/404.html"))
    (OUT / "404.html").write_text(html_str, encoding="utf-8")


# --------------------------------------------------------------------------- #
# Orchestration
# --------------------------------------------------------------------------- #
def build():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    posts = load_posts()
    notes = load_notes()

    copy_static()
    (OUT / ".nojekyll").write_text("", encoding="utf-8")  # deploy as-is, skip Jekyll
    build_pages(posts)
    build_posts(posts)
    build_writing_index(posts)
    build_notes(notes)
    build_notes_index(notes)
    build_feeds(posts)
    build_404()

    urls = ["/", "/writing/", "/notes/", "/research/", "/software/", "/about/",
            "/now/", "/uses/", "/blogroll/", "/colophon/"]
    urls += [p["url"] for p in posts] + [n["url"] for n in notes]
    build_sitemap(urls)

    print(f"Built {len(posts)} posts, {len(notes)} notes → {OUT.relative_to(ROOT)}/")


def serve():
    import http.server, socketserver, functools, os
    os.chdir(OUT)
    handler = functools.partial(http.server.SimpleHTTPRequestHandler)
    with socketserver.TCPServer(("", 8000), handler) as httpd:
        print("Serving _site/ at http://localhost:8000  (Ctrl-C to stop)")
        httpd.serve_forever()


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Build the Silvæ site.")
    ap.add_argument("--serve", action="store_true", help="serve _site/ after building")
    args = ap.parse_args()
    build()
    if args.serve:
        serve()
