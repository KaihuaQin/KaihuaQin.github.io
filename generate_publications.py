import re
from pathlib import Path

BIB_PATH = Path('publications.bib')

# Minimal BibTeX parser
def parse_bibtex(bib_content):
    entries = []
    entry = None
    for line in bib_content.splitlines():
        line = line.strip()
        if line.startswith('@'):
            if entry:
                entries.append(entry)
            entry = {'_type': line[1:line.index('{')], '_id': line[line.index('{')+1:line.index(',')].strip()}
        elif entry is not None and '=' in line:
            key, value = line.split('=', 1)
            value = value.strip().strip(',').strip('{}').strip('"')
            entry[key.strip()] = value
        elif entry is not None and line == '}':
            entries.append(entry)
            entry = None
    if entry:
        entries.append(entry)
    return entries

def convert_latex_chars(text):
    """Convert LaTeX special characters to Unicode"""
    latex_to_unicode = {
        # Umlaut/diaeresis
        '{\"a}': 'ä',
        '{\"o}': 'ö', 
        '{\"u}': 'ü',
        '{\"A}': 'Ä',
        '{\"O}': 'Ö',
        '{\"U}': 'Ü',
        '{\"e}': 'ë',
        '{\"i}': 'ï',
        '{\"E}': 'Ë',
        '{\"I}': 'Ï',
        # Alternative umlaut syntax
        r'{\\"a}': 'ä',
        r'{\\"o}': 'ö',
        r'{\\"u}': 'ü',
        r'{\\"A}': 'Ä',
        r'{\\"O}': 'Ö',
        r'{\\"U}': 'Ü',
        # Special characters
        r'{\ss}': 'ß',
        r'{\ae}': 'æ',
        r'{\AE}': 'Æ',
        r'{\oe}': 'œ',
        r'{\OE}': 'Œ',
        r'{\c c}': 'ç',
        r'{\c C}': 'Ç',
        # Acute accent
        r"{\\'a}": 'á',
        r"{\\'e}": 'é',
        r"{\\'i}": 'í',
        r"{\\'o}": 'ó',
        r"{\\'u}": 'ú',
        r"{\\'A}": 'Á',
        r"{\\'E}": 'É',
        r"{\\'I}": 'Í',
        r"{\\'O}": 'Ó',
        r"{\\'U}": 'Ú',
        # Grave accent
        r'{\`a}': 'à',
        r'{\`e}': 'è',
        r'{\`i}': 'ì',
        r'{\`o}': 'ò',
        r'{\`u}': 'ù',
        r'{\`A}': 'À',
        r'{\`E}': 'È',
        r'{\`I}': 'Ì',
        r'{\`O}': 'Ò',
        r'{\`U}': 'Ù',
        # Circumflex
        r'{\^a}': 'â',
        r'{\^e}': 'ê',
        r'{\^i}': 'î',
        r'{\^o}': 'ô',
        r'{\^u}': 'û',
        r'{\^A}': 'Â',
        r'{\^E}': 'Ê',
        r'{\^I}': 'Î',
        r'{\^O}': 'Ô',
        r'{\^U}': 'Û',
        # Tilde
        r'{\~a}': 'ã',
        r'{\~n}': 'ñ',
        r'{\~o}': 'õ',
        r'{\~A}': 'Ã',
        r'{\~N}': 'Ñ',
        r'{\~O}': 'Õ',
    }
    
    result = text
    for latex, unicode_char in latex_to_unicode.items():
        result = result.replace(latex, unicode_char)
    
    return result

def html_escape(text):
    # First convert LaTeX characters, then HTML escape
    text = convert_latex_chars(text)
    return (text.replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('"', '&quot;'))

def format_authors(authors):
    # Split on ' and ', then split each name on ',' and reformat as 'First Last'
    names = [a.strip() for a in authors.split(' and ')]
    formatted = []
    for name in names:
        # Convert LaTeX characters first
        name = convert_latex_chars(name)
        
        if ',' in name:
            last, first = [x.strip() for x in name.split(',', 1)]
            full_name = f"{first} {last}".strip()
        else:
            full_name = name
        
        # Highlight Kaihua Qin's name
        if 'Kaihua Qin' in full_name:
            full_name = full_name.replace('Kaihua Qin', '<strong class="author-highlight">Kaihua Qin</strong>')
        
        formatted.append(full_name)
    return ', '.join(formatted)


def make_links(entry):
    links = []
    if 'arxiv' in entry:
        links.append(f'<a href="https://arxiv.org/abs/{entry["arxiv"]}" target="_blank"><i class="far fa-file-pdf"></i> arXiv</a>')
    if 'eprint' in entry:
        links.append(f'<a href="https://eprint.iacr.org/{entry["eprint"]}" target="_blank"><i class="far fa-file-pdf"></i> ePrint</a>')
    if 'blog' in entry:
        links.append(f'<a href="{entry["blog"]}" target="_blank"><i class="fas fa-blog"></i> Blog</a>')
    
    # Add other common links if present
    if 'pdf' in entry:
        links.append(f'<a href="{entry["pdf"]}" target="_blank"><i class="far fa-file-pdf"></i> PDF</a>')
    
    return '\n                  '.join(links)

def make_entry_html(entry):
    # Venue tag (abbreviation)
    venue = html_escape(entry.get('abbr', ''))
    
    title = html_escape(entry.get('title', ''))
    # Don't escape authors since we're adding HTML highlighting
    authors = format_authors(entry.get('author', ''))
    
    links_html = make_links(entry)
    links_div = f'<div class="pub-links">\n                  {links_html}\n                </div>' if links_html else ''
    
    html = f'''            <li class="pub-item">
              <div class="pub-venue-tag">{venue}</div>
              <div class="pub-details">
                <div class="pub-title">{title}</div>
                <div class="pub-authors">
                  {authors}
                </div>
                {links_div}
              </div>
            </li>'''
    return html

def generate_publications_html():
    bib_content = BIB_PATH.read_text(encoding='utf-8')
    entries = parse_bibtex(bib_content)
    
    # Group by year
    years = {}
    for entry in entries:
        year = entry.get('year', '0')
        if year not in years:
            years[year] = []
        years[year].append(entry)
    
    # Sort years in descending order
    sorted_years = sorted(years.keys(), key=int, reverse=True)
    
    # Generate HTML for each year section
    html_sections = []
    
    for year in sorted_years:
        year_entries = years[year]
        # Sort entries within year alphabetically by title (or use a 'selected' flag or other logic if needed)
        # Defaulting to bib order or title for now
        
        year_html = f'        <div class="year-group">\n'
        year_html += f'          <div class="year-header">{year}</div>\n'
        year_html += f'          <ul class="pub-list">\n'
        
        for entry in year_entries:
            year_html += f'{make_entry_html(entry)}\n'
        
        year_html += f'          </ul>\n'
        year_html += f'        </div>'
        
        html_sections.append(year_html)
    
    return '\n\n'.join(html_sections)

def update_index_html():
    index_path = Path('index.html')
    pub_html = generate_publications_html()
    index_content = index_path.read_text(encoding='utf-8')
    
    # Target the content AFTER the Google Scholar link
    # We look for <section id="publications" ...> ... <p ...>Full list ...</p> (CAPTURE START) ... (CAPTURE END) </section>
    
    # More robust regex: Find the Publications section, keep the header and google scholar link, replace the rest up to </section>
    pattern = r'(<section id="publications" class="content-section">\s*<h2>Publications</h2>\s*<p[^>]*>.*?Google Scholar</a>\.</p>)([\s\S]*?)(</section>)'
    
    match = re.search(pattern, index_content, re.DOTALL)
    
    if match:
        header_part = match.group(1)
        closing_tag = match.group(3)
        
        new_content = index_content[:match.start()] + header_part + '\n\n' + pub_html + '\n\n      ' + closing_tag + index_content[match.end():]
        index_path.write_text(new_content, encoding='utf-8')
        print("Updated index.html with new publications list.")
    else:
        print("Could not find publications section to update. Please check index.html structure.")




def make_entry_md(entry):
    venue = entry.get('abbr', '')
    title = entry.get('title', '')
    authors = format_authors(entry.get('author', ''))
    # Remove HTML bolding from authors for MD
    authors = authors.replace('<strong class="author-highlight">', '**').replace('</strong>', '**')
    
    links = []
    if 'arxiv' in entry:
        links.append(f"[arXiv](https://arxiv.org/abs/{entry['arxiv']})")
    if 'eprint' in entry:
        links.append(f"[ePrint](https://eprint.iacr.org/{entry['eprint']})")
    if 'blog' in entry:
        links.append(f"[Blog]({entry['blog']})")
    if 'pdf' in entry:
        links.append(f"[PDF]({entry['pdf']})")
        
    links_str = " | ".join(links)
    
    venue_str = f"**[{venue}]** " if venue else ""
    return f"- {venue_str}{title}\n  - {authors}\n  - {links_str}"

def generate_publications_md():
    bib_content = BIB_PATH.read_text(encoding='utf-8')
    entries = parse_bibtex(bib_content)
    
    # Group by year
    years = {}
    for entry in entries:
        year = entry.get('year', '0')
        if year not in years:
            years[year] = []
        years[year].append(entry)
    
    sorted_years = sorted(years.keys(), key=int, reverse=True)
    md_sections = []
    
    for year in sorted_years:
        year_entries = years[year]
        # Sort by title
        year_entries.sort(key=lambda e: e.get('title', ''))
        
        section = f"### {year}\n"
        for entry in year_entries:
            section += make_entry_md(entry) + "\n"
        md_sections.append(section)
        
    return "\n".join(md_sections)

def update_index_md():
    md_path = Path('index.md')
    if not md_path.exists():
        print("index.md not found, skipping.")
        return

    pub_md = generate_publications_md()
    md_content = md_path.read_text(encoding='utf-8')
    
    # Replace content between markers
    pattern = r'(<!-- PUBLICATIONS START -->)([\s\S]*?)(<!-- PUBLICATIONS END -->)'
    
    if re.search(pattern, md_content):
        new_content = re.sub(
            pattern, 
            lambda m: m.group(1) + '\n' + pub_md + '\n' + m.group(3),
            md_content
        )
        md_path.write_text(new_content, encoding='utf-8')
        print("Updated index.md with new publications list.")
    else:
        print("Could not find markers in index.md")

if __name__ == '__main__':
    update_index_html()
    update_index_md() 