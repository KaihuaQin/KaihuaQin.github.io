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
        links.append(f'<a href="https://arxiv.org/abs/{entry["arxiv"]}" target="_blank">arXiv</a>')
    if 'eprint' in entry:
        links.append(f'<a href="https://eprint.iacr.org/{entry["eprint"]}" target="_blank">ePrint</a>')
    if 'blog' in entry:
        links.append(f'<a href="{entry["blog"]}" target="_blank">Blog</a>')
    return ' | '.join(links)

def make_entry_html(entry):
    abbr = f'<span class="pub-abbr">{html_escape(entry["abbr"])}</span> ' if 'abbr' in entry else ''
    title = html_escape(entry.get('title', ''))
    # Don't escape authors since we're adding HTML highlighting
    authors = format_authors(entry.get('author', ''))
    links = make_links(entry)
    return f'<li class="pub-entry">{abbr}<span class="pub-title">{title}</span><br><span class="pub-authors">{authors}</span>' + (f'<br><span class="pub-links">{links}</span>' if links else '') + '</li>'

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
        # Sort entries within year alphabetically by title
        year_entries.sort(key=lambda e: e.get('title', ''))
        
        # Generate year section - collapse older years (keep recent 3 years expanded)
        current_year = 2025
        collapsed_class = ' collapsed' if int(year) < (current_year - 2) else ''
        year_html = f'      <div class="year-section{collapsed_class}">\n'
        year_html += f'        <h3 class="year-header" onclick="toggleYear(this)">\n'
        year_html += f'          <span>{year}</span>\n'
        year_html += f'          <span class="year-toggle">▼</span>\n'
        year_html += f'        </h3>\n'
        year_html += f'        <ul class="pub-list">\n'
        
        for entry in year_entries:
            year_html += f'          {make_entry_html(entry)}\n'
        
        year_html += f'        </ul>\n'
        year_html += f'      </div>'
        
        html_sections.append(year_html)
    
    return '\n\n'.join(html_sections)

def update_index_html():
    index_path = Path('index.html')
    pub_html = generate_publications_html()
    index_content = index_path.read_text(encoding='utf-8')
    
    # Find the publications section and preserve the bibliometrics line
    pattern = r'(<section[^>]+id="publications"[^>]*>\s*)(.*?)(<div class="year-section">.*?)(</section>)'
    
    def replace_publications(match):
        section_start = match.group(1)
        before_publications = match.group(2)  # This should contain the bibliometrics line
        section_end = match.group(4)
        
        # Keep any content before the first year-section (like bibliometrics line)
        return section_start + before_publications + pub_html + '\n    ' + section_end
    
    # Try the targeted replacement first
    new_content = re.sub(pattern, replace_publications, index_content, flags=re.DOTALL)
    
    # If no match, fall back to simpler replacement
    if new_content == index_content:
        # Fallback: replace content between publications section tags
        new_content = re.sub(
            r'(<section[^>]+id="publications"[^>]*>)([\s\S]*?)(</section>)',
            lambda m: m.group(1) + '\n      <p class="bibliometrics-note">Bibliometrics can be found on <a href="https://scholar.google.com/citations?user=-NPCrhcAAAAJ" target="_blank">Google Scholar</a>.</p>\n' + pub_html + '\n    ' + m.group(3),
            index_content,
            flags=re.MULTILINE
        )
    
    index_path.write_text(new_content, encoding='utf-8')

if __name__ == '__main__':
    update_index_html() 