from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source_path = ROOT / 'scripts' / 'build_academic_cv.py'
source = source_path.read_text(encoding='utf-8')

# Zenodo: exact creator-field search so only İlyas Ferman records are listed.
ZENODO_ALL = 'https://zenodo.org/search?q=metadata.creators.person_or_org.name%3A%22Ferman%2C%20%C4%B0lyas%22&l=list&p=1&s=10&sort=newest'

# Zenodo: top button and CV profile link should list all works.
source = source.replace("ZENODO_URL=CHAPTER_URL", f"ZENODO_URL='{ZENODO_ALL}'")
source = source.replace("('Zenodo - Kitap Bölümü',ZENODO_URL)", "('Zenodo - Tüm Çalışmalar',ZENODO_URL)")
source = source.replace(
    "html=html.replace('https://zenodo.org/search?q=%220000-0003-4844-3508%22', ZENODO_URL)",
    "html=html.replace('https://zenodo.org/search?q=%220000-0003-4844-3508%22', ZENODO_URL)\n"
    "    html=html.replace('https://zenodo.org/search?q=creators.orcid%3A%220000-0003-4844-3508%22', ZENODO_URL)\n"
    "    html=html.replace('https://zenodo.org/search?q=0000-0003-4844-3508%20OR%20%22%C4%B0lyas%20Ferman%22', ZENODO_URL)\n"
    "    html=html.replace(CHAPTER_URL, ZENODO_URL)"
)

# CV certificate thumbnails: open the site's certificate modal and mark that the click came from the CV.
# The page then restores the CV (page 2) when the certificate X button is pressed.
source = source.replace(
    "url='https://ilyasferman.com/?cert='+ci['key']+'#sertifikalar'",
    "url='https://ilyasferman.com/?cert='+ci['key']+'&from=cv'"
)

# CV: preserve the existing PDF design, only improve vertical spacing.
source = source.replace("return y-15", "return y-18")
source = source.replace("y=wrapped(c,profile,34,y,W-68,size=7.1,leading=8.3); y-=3", "y=wrapped(c,profile,34,y,W-68,size=7.1,leading=8.3); y-=7")
source = source.replace("y+=2; y=section(c,y,'Mesleki Deneyim')", "y-=7; y=section(c,y,'Mesleki Deneyim')")
source = source.replace("y+=2; y=section(c,y,'Akademik Çalışmalar')", "y-=7; y=section(c,y,'Akademik Çalışmalar')")
source = source.replace("ext_link(c,'DOI: https://doi.org/10.5281/zenodo.23544985',CHAPTER_URL,34,y,6.1); y-=14", "ext_link(c,'DOI: https://doi.org/10.5281/zenodo.23544985',CHAPTER_URL,34,y,6.1); y-=20")
source = source.replace("size=6.5,leading=7.8); y-=2", "size=6.5,leading=7.8); y-=8")

# Remove only the foreign-language exam score; keep the rest of the language text.
source = source.replace(
    "İngilizce: Akademik okuma ileri düzey (öz değerlendirme); konuşma becerisi gelişmekte. Yabancı dil sınav puanı: 55.",
    "İngilizce: Akademik okuma ileri düzey (öz değerlendirme); konuşma becerisi gelişmekte."
)

# Execute the corrected generator without changing the original reusable source.
exec(compile(source, str(source_path), 'exec'), {'__file__': str(source_path), '__name__': '__main__'})

# When a certificate is opened from the PDF, X should return to the CV instead of the homepage.
index_path = ROOT / 'index.html'
html = index_path.read_text(encoding='utf-8')
old = """    const requestedCertificate = new URLSearchParams(window.location.search).get('cert');
    if(requestedCertificate){
      const certificateButton = document.querySelector('.certificate-trigger[data-template=\"' + requestedCertificate + '\"]');
      if(certificateButton) setTimeout(() => certificateButton.click(), 0);
    }
    closeButton.addEventListener('click', closeModal);
    modal.addEventListener('click', event => { if(event.target === modal) closeModal(); });
    document.addEventListener('keydown', event => { if(event.key === 'Escape' && !modal.hidden) closeModal(); });"""
new = """    const queryParams = new URLSearchParams(window.location.search);
    const requestedCertificate = queryParams.get('cert');
    let restoreCvOnClose = Boolean(requestedCertificate);

    function restoreCv(){
      htmlViewer.hidden = true;
      htmlViewer.replaceChildren();
      frame.src = 'cv/ilyas-ferman-akademik-cv.pdf#page=2&view=FitH';
      frame.hidden = false;
      newTab.href = 'cv/ilyas-ferman-akademik-cv.pdf';
      newTab.hidden = false;
      modalTitle.textContent = 'İlyas Ferman · Akademik CV';
      restoreCvOnClose = false;
      history.replaceState(null, '', window.location.pathname);
      openModal('İlyas Ferman · Akademik CV');
    }

    if(requestedCertificate){
      frame.src = 'cv/ilyas-ferman-akademik-cv.pdf#page=2&view=FitH';
      const certificateButton = document.querySelector('.certificate-trigger[data-template=\"' + requestedCertificate + '\"]');
      if(certificateButton) setTimeout(() => certificateButton.click(), 0);
    }

    function handleDocumentClose(){
      if(restoreCvOnClose && !htmlViewer.hidden){
        restoreCv();
        return;
      }
      closeModal();
    }

    closeButton.addEventListener('click', handleDocumentClose);
    modal.addEventListener('click', event => { if(event.target === modal) handleDocumentClose(); });
    document.addEventListener('keydown', event => { if(event.key === 'Escape' && !modal.hidden) handleDocumentClose(); });"""
if old in html:
    html = html.replace(old, new)
else:
    raise RuntimeError('Expected certificate modal close block was not found in index.html')
index_path.write_text(html, encoding='utf-8')
