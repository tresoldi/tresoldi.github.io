#!/usr/bin/env python3
"""
Generate bibliography from BibTeX file.

Parses _data/publications.bib and creates a formatted bibliography
section for the research page using traditional academic citation style.
"""

import re
from pathlib import Path


def parse_bibtex_entry(entry):
    """
    Parse a single BibTeX entry into a dictionary.

    @param entry: String containing a BibTeX entry
    @return: Dictionary with parsed fields
    """
    result = {}

    # Get entry type and cite key
    match = re.match(r'@(\w+)\{([^,]+),', entry)
    if match:
        result['type'] = match.group(1)
        result['key'] = match.group(2)

    # Extract fields
    for field_match in re.finditer(r'(\w+)\s*=\s*\{([^}]+)\}', entry):
        field_name = field_match.group(1)
        field_value = field_match.group(2).strip()
        result[field_name] = field_value

    return result


def format_authors(authors_str):
    """
    Format author string for citation.

    @param authors_str: String of authors from BibTeX
    @return: Formatted author string
    """
    authors = [a.strip() for a in authors_str.split(' and ')]

    if len(authors) == 1:
        return authors[0]
    elif len(authors) == 2:
        return f"{authors[0]} & {authors[1]}"
    elif len(authors) <= 5:
        return ', '.join(authors[:-1]) + ', & ' + authors[-1]
    else:
        # More than 5 authors, use et al.
        return f"{authors[0]} et al."


def format_citation(entry):
    """
    Format a BibTeX entry as a traditional academic citation.

    @param entry: Dictionary with parsed BibTeX fields
    @return: HTML string with formatted citation
    """
    authors = format_authors(entry.get('author', ''))
    year = entry.get('year', '')
    title = entry.get('title', '')

    # Build citation based on entry type
    if entry['type'] == 'article':
        journal = entry.get('journal', '')
        volume = entry.get('volume', '')
        number = entry.get('number', '')
        pages = entry.get('pages', '')

        citation = f"{authors} ({year}). {title}. *{journal}*"
        if volume:
            citation += f", {volume}"
        if number:
            citation += f"({number})"
        if pages:
            citation += f", {pages}"
        citation += "."

    elif entry['type'] == 'incollection':
        booktitle = entry.get('booktitle', '')
        publisher = entry.get('publisher', '')

        citation = f"{authors} ({year}). {title}. In *{booktitle}*"
        if publisher:
            citation += f". {publisher}"
        citation += "."

    else:
        # Generic format
        citation = f"{authors} ({year}). {title}."

    return citation


def generate_bibliography():
    """
    Generate bibliography HTML from BibTeX file.

    Reads _data/publications.bib and creates formatted HTML output.
    """
    bib_file = Path('_data/publications.bib')

    if not bib_file.exists():
        print("No publications.bib file found")
        return

    # Read BibTeX file
    content = bib_file.read_text(encoding='utf-8')

    # Split into entries
    entries = re.findall(r'@\w+\{[^@]+', content)

    # Parse and sort entries by year (descending)
    parsed_entries = [parse_bibtex_entry(e) for e in entries]
    parsed_entries.sort(key=lambda x: x.get('year', ''), reverse=True)

    # Generate HTML
    html_lines = ['<section class="bibliography">', '<h2>Publications</h2>', '<ul class="bibliography-list">']

    for entry in parsed_entries:
        citation = format_citation(entry)
        html_lines.append(f'<li>{citation}</li>')

    html_lines.extend(['</ul>', '</section>'])

    # Write to include file
    output_file = Path('_includes/bibliography.html')
    output_file.write_text('\n'.join(html_lines), encoding='utf-8')

    print(f"Generated bibliography with {len(parsed_entries)} entries")


if __name__ == '__main__':
    generate_bibliography()
