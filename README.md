# Kaihua Qin Academic Website

This repository contains the source code for my academic homepage at [qin.ac](https://qin.ac).

## Repository Structure

### Source Files (Main Branch)
- `generate_publications.py` - Python script to generate publications HTML from BibTeX
- `publications.bib` - BibTeX file containing publication data
- `index.html` - Main website HTML (auto-generated from publications.bib)
- `style.css` - Website styling
- `prof_pic.jpg` - Profile picture
- `cv.pdf` - CV document
- `favicon.*` - Website favicon files
- `robots.txt` - Search engine crawling instructions
- `sitemap.xml` - Website structure for search engines

### Deployment Files (gh-pages Branch)
The `gh-pages` branch contains only the necessary files for the website:
- HTML, CSS, images, PDFs, favicons
- **Excludes**: Python scripts, BibTeX files, source code

## Deployment Process

### Automatic Deployment
1. **Push to main branch** triggers GitHub Action
2. **Publication generator** runs to update `index.html`
3. **Clean deployment** creates `gh-pages` branch with only web files
4. **GitHub Pages** serves from `gh-pages` branch

### Manual Deployment
```bash
# Run publication generator
python generate_publications.py

# Deploy manually (if needed)
gh workflow run deploy.yml
```

## GitHub Actions

### `deploy.yml`
- **Triggers**: Push to main branch or manual dispatch
- **Actions**: 
  - Runs publication generator
  - Creates clean deployment branch
  - Updates main branch with generated files

## Website Features

- **Responsive Design**: Works on all devices
- **Dark/Light Theme**: User preference toggle
- **Publications**: Auto-generated from BibTeX
- **CV Viewer**: PDF viewer with zoom controls
- **SEO Optimized**: Meta tags, structured data, sitemap
- **Favicon**: Multiple formats for all devices

## Local Development

```bash
# Clone repository
git clone https://github.com/KaihuaQin/KaihuaQin.github.io.new.git

# Install Python dependencies (if any)
# No external dependencies required

# Run publication generator
python generate_publications.py

# Open index.html in browser
open index.html
```

## Contact

- **Email**: kaihua[at]qin[dot]ac
- **Website**: [qin.ac](https://qin.ac)
- **GitHub**: [@kaihuaqin](https://github.com/kaihuaqin)
- **Google Scholar**: [Profile](https://scholar.google.com/citations?user=-NPCrhcAAAAJ)
