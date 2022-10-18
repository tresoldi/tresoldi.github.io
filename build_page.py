# TODO: develop our own pybtex style(s), starting from the default one
# TODO: consider integrating jinja2 for generating the markdown
# TODO: take pandoc css and make it our own, independent, for later styling

# Import Python standard libraries
from pathlib import Path
import subprocess
from collections import defaultdict

# Import 3rd-party libraries
from pybtex import PybtexEngine
from pybtex.database import parse_file, BibliographyData

BASE_PATH = Path(__file__).parent


def get_bib_highlights():
    # Read full bibliographic data and filter the entries manually annotated as "most important";
    # this is done by manually filtering those which carry a field "highlight" and a value "true".
    # Note that due to the complex way pybtex works, and not wanting to depend on an actual
    # LaTeX installation, there is a lot of data wrangling in here.
    bibtex_full = parse_file(BASE_PATH / "biblio.bib")
    highlights = {}
    for entry_key, entry in bibtex_full.entries.items():
        if entry.fields.get("highlight") == "true":
            highlights[entry_key] = entry

    engine = PybtexEngine()
    bib_highlights = BibliographyData(entries=highlights)
    str_highlights = engine.format_from_string(
        bib_highlights.to_string(bib_format="bibtex"),
        style="plain",
        output_backend="markdown",
    )

    return str_highlights


def get_bib_full():
    # Collect all entries by type, so we can list them separately
    # TODO: add fields to distinguish the various "misc"
    bibtex_full = parse_file(BASE_PATH / "biblio.bib")
    entries_by_type = defaultdict(dict)
    for entry_key, entry in bibtex_full.entries.items():
        entries_by_type[entry.type][entry_key] = entry

    # Build the entries for all entry types
    engine = PybtexEngine()
    bib_full = {}
    for entry_type, entries in entries_by_type.items():
        bib_entry_type = BibliographyData(entries=entries)
        bib_full[entry_type] = engine.format_from_string(
            bib_entry_type.to_string(bib_format="bibtex"),
            style="plain",
            output_backend="markdown",
        )

    return bib_full


def build_biblio() -> dict:
    # Obtain the full bibliography, by category
    biblio = get_bib_full()

    # Obtain the bibliography highlights, for the main page
    biblio["highlights"] = get_bib_highlights()

    return biblio


def build_md(template: str, replaces: dict):
    """
    Build a Markdown source from a template, applying replaces.
    """

    template_path = BASE_PATH / f"{template}.template.md"
    output_path = BASE_PATH / f"{template}.md"

    # Read source
    with open(template_path, encoding="utf-8") as handler:
        source = handler.read()

    # Apply replaces
    for rep_from, rep_to in replaces.items():
        source = source.replace(f"[[{rep_from}]]", rep_to)

    # Write Markdown file
    with open(output_path, "w", encoding="utf-8") as handler:
        handler.write(source)


def run_pandoc(source_file):
    # Get output filename
    # TODO: write safer code
    output_file = source_file.replace(".md", ".html")

    subprocess.run(
        [
            "pandoc",
            "-s",
            "-f",
            "markdown+smart",
            "--to=html5",
            "-H",
            "header.include",
            "-A",
            "afterbody.include",
            "-o",
            output_file,
            source_file,
        ]
    )


def main():
    # Obtain the various bibliographic information
    biblio = build_biblio()

    # Build list of replacements and generate the Markdown files for pandoc
    replaces = {
        "bib_highlights": biblio["highlights"],
        "bib_misc": biblio["misc"],
        "bib_article": biblio["article"],
        "bib_book": biblio["book"],
        "bib_inproceedings": biblio["inproceedings"],
        "bib_incollection": biblio["incollection"],
    }
    for page in ["index", "publications"]:
        build_md(page, replaces)
        run_pandoc(f"{page}.md")


# Script entry point
if __name__ == "__main__":
    main()
