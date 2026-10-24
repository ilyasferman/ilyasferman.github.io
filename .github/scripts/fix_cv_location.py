from pathlib import Path
import re

index_path = Path('index.html')
css_path = Path('assets/site-final.css')
html = index_path.read_text(encoding='utf-8')
css = css_path.read_text(encoding='utf-8')

# 1) Keep CV only in the top navigation; clicking it opens the existing modal viewer.
html = html.replace(
    '<a href="#cv">CV</a>',
    '<a class="document-trigger" href="cv/ilyas-ferman-akademik-cv.pdf" data-document="cv/ilyas-ferman-akademik-cv.pdf" data-document-title="İlyas Ferman · Akademik CV">CV</a>',
    1,
)

# 2) Remove the hero-area CV button next to the profile photo.
html = re.sub(
    r'\s*<button class="btn btn-primary document-trigger" type="button" data-document="cv/ilyas-ferman-akademik-cv\.pdf" data-document-title="İlyas Ferman · Akademik CV"><span class="doc-icon">▤</span> CV Görüntüle <span>→</span></button>\n?',
    '\n',
    html,
    count=1,
)

# 3) Remove the extra Academic CV section added near the bottom.
html = re.sub(
    r'\n\s*<section class="detail-section soft cv-section" id="cv">.*?</section>\n',
    '\n',
    html,
    count=1,
    flags=re.S,
)

# 4) Remove the footer CV link so CV appears only in the top navigation.
html = html.replace('        <a href="#cv">CV</a>\n', '', 1)

# 5) Make anchor-based document triggers open the same modal without navigating away.
old = "document.querySelectorAll('.document-trigger').forEach(button => button.addEventListener('click', () => {\n      const src = button.dataset.document;"
new = "document.querySelectorAll('.document-trigger').forEach(button => button.addEventListener('click', event => {\n      event.preventDefault();\n      const src = button.dataset.document;"
if old in html:
    html = html.replace(old, new, 1)
elif "event.preventDefault();" not in html:
    raise SystemExit('Document trigger handler pattern not found')

# 6) Remove CSS for the deleted standalone CV section.
marker = '/* Academic CV showcase */'
if marker in css:
    css = css.split(marker, 1)[0].rstrip() + '\n'

index_path.write_text(html, encoding='utf-8')
css_path.write_text(css, encoding='utf-8')
