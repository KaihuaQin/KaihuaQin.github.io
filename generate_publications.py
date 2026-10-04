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


FILE_ICON = (
    '<svg class="far fa-file-pdf svg-inline--fa" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" '
    'role="img" aria-hidden="true" focusable="false"><path fill="currentColor" d="M0 64C0 28.7 28.7 0 64 0L224 0l0 128c0 17.7 14.3 32 32 32l128 0 0 144-208 0c-35.3 0-64 28.7-64 64l0 144-48 0c-35.3 0-64-28.7-64-64L0 64zm384 64l-128 0L256 0 384 128zM176 352l32 0c30.9 0 56 25.1 56 56s-25.1 56-56 56l-16 0 0 32c0 8.8-7.2 16-16 16s-16-7.2-16-16l0-48 0-80c0-8.8 7.2-16 16-16zm32 80c13.3 0 24-10.7 24-24s-10.7-24-24-24l-16 0 0 48 16 0zm96-80l32 0c26.5 0 48 21.5 48 48l0 64c0 26.5-21.5 48-48 48l-32 0c-8.8 0-16-7.2-16-16l0-128c0-8.8 7.2-16 16-16zm32 128c8.8 0 16-7.2 16-16l0-64c0-8.8-7.2-16-16-16l-16 0 0 96 16 0zm80-112c0-8.8 7.2-16 16-16l48 0c8.8 0 16 7.2 16 16s-7.2 16-16 16l-32 0 0 32 32 0c8.8 0 16 7.2 16 16s-7.2 16-16 16l-32 0 0 48c0 8.8-7.2 16-16 16s-16-7.2-16-16l0-64 0-64z"/></svg>'
)
BLOG_ICON = (
    '<svg class="fas fa-blog svg-inline--fa" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" '
    'role="img" aria-hidden="true" focusable="false"><path fill="currentColor" d="M192 32c0 17.7 14.3 32 32 32c123.7 0 224 100.3 224 224c0 17.7 14.3 32 32 32s32-14.3 32-32C512 128.9 383.1 0 224 0c-17.7 0-32 14.3-32 32zm0 96c0 17.7 14.3 32 32 32c70.7 0 128 57.3 128 128c0 17.7 14.3 32 32 32s32-14.3 32-32c0-106-86-192-192-192c-17.7 0-32 14.3-32 32zM96 144c0-26.5-21.5-48-48-48S0 117.5 0 144V368c0 79.5 64.5 144 144 144s144-64.5 144-144s-64.5-144-144-144H128v96h16c26.5 0 48 21.5 48 48s-21.5 48-48 48s-48-21.5-48-48V144z"/></svg>'
)
BIB_ICON = (
    '<svg class="svg-inline--fa" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" '
    'role="img" aria-hidden="true" focusable="false"><path fill="currentColor" d="M8.2 4.5L4.5 12l3.7 7.5h2.4L6.7 12 10.6 4.5H8.2zm7.6 0h-2.4L16.3 12l-3.9 7.5h2.4L19.5 12 15.8 4.5z"/></svg>'
)

SKIP_BIB_FIELDS = {'_type', '_id', 'abbr', 'tags', 'arxiv', 'eprint', 'blog', 'pdf'}
BIB_FIELD_ORDER = [
    'author', 'title', 'booktitle', 'journal', 'year', 'volume', 'number',
    'pages', 'publisher', 'address', 'organization', 'doi',
]


def venue_label(entry):
    venue = html_escape(entry.get('abbr', ''))
    return re.sub(r'\s+\d{2}$', '', venue)


def parse_tags(entry):
    raw = entry.get('tags', '')
    if not raw:
        return []
    return [tag.strip() for tag in raw.split(',') if tag.strip()]


def make_tags_html(entry):
    tags = parse_tags(entry)
    if not tags:
        return ''
    chips = ''.join(f'<span class="pub-tag">{html_escape(tag)}</span>' for tag in tags)
    return f'<div class="pub-tags">\n                  {chips}\n                </div>'


def make_bibtex(entry):
    keys = [key for key in BIB_FIELD_ORDER if key in entry]
    keys += [key for key in entry if key not in SKIP_BIB_FIELDS and key not in keys]
    lines = [f"@{entry.get('_type', 'inproceedings')}{{{entry.get('_id', 'entry')},"]
    for key in keys:
        lines.append(f"  {key} = {{{entry[key]}}},")
    lines.append('}')
    return '\n'.join(lines)


def make_links(entry):
    links = []
    if 'arxiv' in entry:
        links.append(f'<a href="https://arxiv.org/abs/{entry["arxiv"]}" target="_blank">{FILE_ICON} arXiv</a>')
    if 'eprint' in entry:
        links.append(f'<a href="https://eprint.iacr.org/{entry["eprint"]}" target="_blank">{FILE_ICON} ePrint</a>')
    if 'blog' in entry:
        links.append(f'<a href="{entry["blog"]}" target="_blank">{BLOG_ICON} Blog</a>')
    if 'pdf' in entry:
        links.append(f'<a href="{entry["pdf"]}" target="_blank">{FILE_ICON} PDF</a>')
    bibtex = html_escape(make_bibtex(entry))
    links.append(
        f'<button type="button" class="bibtex-copy" data-bibtex="{bibtex}">{BIB_ICON} '
        f'<span class="bibtex-label">BibTeX</span></button>'
    )
    return '\n                  '.join(links)


def make_entry_html(entry):
    venue = venue_label(entry)
    title = html_escape(entry.get('title', ''))
    authors = format_authors(entry.get('author', ''))
    tags_html = make_tags_html(entry)
    links_html = make_links(entry)
    links_div = f'<div class="pub-links">\n                  {links_html}\n                </div>' if links_html else ''

    parts = [
        f'<div class="pub-title">{title}</div>',
        f'<div class="pub-authors">\n                  {authors}\n                </div>',
        tags_html,
        links_div,
    ]
    details = '\n                '.join(part for part in parts if part)

    return f'''            <li class="pub-item">
              <div class="pub-venue-tag">{venue}</div>
              <div class="pub-details">
                {details}
              </div>
            </li>'''


def load_entries():
    return parse_bibtex(BIB_PATH.read_text(encoding='utf-8'))


def generate_publications_html():
    entries = load_entries()
    years = {}
    for entry in entries:
        years.setdefault(entry.get('year', '0'), []).append(entry)

    html_sections = []
    for year in sorted(years.keys(), key=int, reverse=True):
        year_html = f'        <div class="year-group">\n'
        year_html += f'          <div class="year-header">{year}</div>\n'
        year_html += f'          <ul class="pub-list">\n'
        for entry in years[year]:
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
    venue = re.sub(r'\s+\d{2}$', '', entry.get('abbr', ''))
    title = entry.get('title', '')
    authors = format_authors(entry.get('author', ''))
    authors = authors.replace('<strong class="author-highlight">', '**').replace('</strong>', '**')

    lines = [f"- **[{venue}]** {title}" if venue else f"- {title}"]
    lines.append(f"  - {authors}")

    tags = parse_tags(entry)
    if tags:
        lines.append(f"  - Tags: {'; '.join(tags)}")

    links = []
    if 'arxiv' in entry:
        links.append(f"[arXiv](https://arxiv.org/abs/{entry['arxiv']})")
    if 'eprint' in entry:
        links.append(f"[ePrint](https://eprint.iacr.org/{entry['eprint']})")
    if 'blog' in entry:
        links.append(f"[Blog]({entry['blog']})")
    if 'pdf' in entry:
        links.append(f"[PDF]({entry['pdf']})")
    if links:
        lines.append(f"  - {' | '.join(links)}")

    return "\n".join(lines)


def generate_publications_md():
    entries = load_entries()
    years = {}
    for entry in entries:
        years.setdefault(entry.get('year', '0'), []).append(entry)

    md_sections = []
    for year in sorted(years.keys(), key=int, reverse=True):
        section = f"### {year}\n"
        for entry in years[year]:
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