#!/usr/bin/env python3
"""
Generate markdown pages from data files (JSON for software, BibTeX for publications).
"""

import json
import re
from datetime import datetime
from pathlib import Path


def parse_bibtex_entry(entry):
    """Parse a single BibTeX entry into a dictionary."""
    # Extract the type and key
    type_match = re.match(r'@(\w+)\{([^,]+),', entry)
    if not type_match:
        return None
    
    entry_type = type_match.group(1)
    key = type_match.group(2)
    
    # Extract fields with better handling of nested braces
    fields = {}
    field_pattern = r'(\w+)\s*=\s*\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}(?=\s*,|\s*\}|\s*$)'
    
    for match in re.finditer(field_pattern, entry):
        field_name = match.group(1).lower()
        field_value = match.group(2).strip()
        # Clean up the field value
        field_value = re.sub(r'\s+', ' ', field_value)
        fields[field_name] = field_value
    
    return {
        'type': entry_type,
        'key': key,
        'fields': fields
    }


def parse_bibtex_file(file_path):
    """Parse a BibTeX file and return a list of entries."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split entries by @ symbol
    entries = re.split(r'\n(?=@)', content)
    entries = [entry.strip() for entry in entries if entry.strip()]
    
    parsed_entries = []
    for entry in entries:
        if not entry.startswith('@'):
            entry = '@' + entry
        parsed = parse_bibtex_entry(entry)
        if parsed:
            parsed_entries.append(parsed)
    
    return parsed_entries


def format_authors(authors_str):
    """Format author names for display."""
    # Split by 'and' and clean up
    authors = [author.strip() for author in authors_str.split(' and ')]
    if len(authors) > 3:
        return f"{authors[0]} et al."
    return ', '.join(authors)


def generate_software_page(software_data):
    """Generate the software.md page from JSON data."""
    page_content = [
        "---",
        "layout: page",
        "title: Software",
        "permalink: /software/",
        "---",
        "",
        "# Software",
        "",
        "I develop open-source tools for computational linguistics and data analysis. All projects are available on [GitHub](https://github.com/tresoldi).",
        ""
    ]
    
    for category_name, projects in software_data['categories'].items():
        if not projects:  # Skip empty categories
            continue
            
        page_content.append(f"## {category_name}")
        page_content.append("")
        
        for project in projects:
            page_content.append(f"### {project['name']}")
            page_content.append(project['description'])
            page_content.append("")
            page_content.append(f"**Repository:** [{project['repository_url']}]({project['repository_url']})")
            
            if project.get('pypi_url'):
                page_content.append(f"**PyPI:** [{project['pypi_url']}]({project['pypi_url']})")
            
            page_content.append("")
    
    # Add footer content
    page_content.extend([
        "## Philosophy",
        "",
        "My software development follows these principles:",
        "",
        "- **Open Source**: All tools are freely available",
        "- **Documentation**: Comprehensive documentation and examples",
        "- **Testing**: Robust test suites for reliability",
        "- **Standards**: Following community best practices",
        "- **Reproducibility**: Enabling reproducible research workflows",
        "",
        "## Installation & Usage",
        "",
        "Most Python packages can be installed via pip:",
        "",
        "```bash",
        "pip install package-name",
        "```",
        "",
        "See individual repositories for specific installation instructions and usage examples."
    ])
    
    return '\n'.join(page_content)


def generate_research_page(publications):
    """Generate the research.md page from BibTeX data."""
    page_content = [
        "---",
        "layout: page",
        "title: Research",
        "permalink: /research/",
        "---",
        "",
        "# Research",
        "",
        "My research focuses on computational historical linguistics, with particular emphasis on native South American languages and phylogenetic methods.",
        "",
        "## Current Projects",
        "",
        "### PhyloVector",
        "Vector-based approaches to phylogenetic analysis in historical linguistics.",
        "",
        "### Uralic Language Phylogeny", 
        "Computational methods for understanding relationships within the Uralic language family.",
        "",
        "### Arawan Family Analysis",
        "Phylogenetic study of the Arawan language family of South America.",
        "",
        "### Large Language Models in Production",
        "Extensive work with LLMs both via APIs and locally deployed systems for linguistic analysis.",
        "",
        "### Tafl Game Programming",
        "Computer game development inspired by chess programming techniques for ancient Nordic board games.",
        "",
        '<div class="decorative-border"></div>',
        "",
        "## Publications",
        ""
    ]
    
    # Sort publications by year (descending)
    publications.sort(key=lambda x: int(x['fields'].get('year', 0)), reverse=True)
    
    # Group by type
    articles = [p for p in publications if p['type'] == 'article']
    incollections = [p for p in publications if p['type'] == 'incollection']
    
    if articles:
        page_content.append("### Journal Articles")
        page_content.append("")
        
        for i, pub in enumerate(articles, 1):
            fields = pub['fields']
            title = fields.get('title', 'Untitled')
            authors = format_authors(fields.get('author', ''))
            year = fields.get('year', '')
            journal = fields.get('journal', '')
            volume = fields.get('volume', '')
            number = fields.get('number', '')
            pages = fields.get('pages', '')
            
            citation = f"**{title}**  \n{authors}  \n*{journal}*"
            
            if volume:
                citation += f", {volume}"
                if number:
                    citation += f"({number})"
                if pages:
                    citation += f":{pages}"
            elif pages:
                citation += f", {pages}"
                
            citation += f", {year}."
            
            page_content.append(citation)
            page_content.append("")
    
    if incollections:
        page_content.append("### Book Chapters")
        page_content.append("")
        
        for i, pub in enumerate(incollections, 1):
            fields = pub['fields']
            title = fields.get('title', 'Untitled')
            authors = format_authors(fields.get('author', ''))
            year = fields.get('year', '')
            booktitle = fields.get('booktitle', '')
            publisher = fields.get('publisher', '')
            
            citation = f"**{title}**  \n{authors}  \nIn *{booktitle}*"
            if publisher:
                citation += f". {publisher}"
            citation += f", {year}."
            
            page_content.append(citation)
            page_content.append("")
    
    # Add footer content
    page_content.extend([
        "## Talks & Presentations",
        "",
        "*Talks list to be updated*",
        "",
        "## Datasets", 
        "",
        "*Research datasets to be listed*",
        "",
        "## Collaborations",
        "",
        "I collaborate with researchers at various institutions, including:",
        "- Uppsala University (Department of Linguistics and Philology)",
        "- Max Planck Institute for the Science of Human History",
        "- Various South American universities and research centers",
        "",
        "## Research Philosophy",
        "",
        "I am committed to:",
        "- **Open Science**: Making research data and methods openly available",
        "- **Reproducibility**: Ensuring research can be independently verified",
        "- **Collaboration**: Working across disciplines and institutions",
        "- **Community Engagement**: Involving language communities in research processes"
    ])
    
    return '\n'.join(page_content)


def main():
    """Main function to generate pages."""
    base_path = Path(__file__).parent
    
    # Load software data
    software_file = base_path / '_data' / 'software.json'
    with open(software_file, 'r', encoding='utf-8') as f:
        software_data = json.load(f)
    
    # Generate software page
    software_content = generate_software_page(software_data)
    with open(base_path / 'software.md', 'w', encoding='utf-8') as f:
        f.write(software_content)
    
    # Load publications data
    publications_file = base_path / '_data' / 'publications.bib'
    publications = parse_bibtex_file(publications_file)
    
    # Generate research page
    research_content = generate_research_page(publications)
    with open(base_path / 'research.md', 'w', encoding='utf-8') as f:
        f.write(research_content)
    
    print(f"Generated software.md with {len(software_data['categories'])} categories")
    print(f"Generated research.md with {len(publications)} publications")


if __name__ == '__main__':
    main()