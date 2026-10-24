from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source_path = ROOT / 'scripts' / 'build_academic_cv.py'
source = source_path.read_text(encoding='utf-8')

# Robust public Zenodo search: match the ORCID or the creator name.
ZENODO_ALL = 'https://zenodo.org/search?q=0000-0003-4844-3508%20OR%20%22%C4%B0lyas%20Ferman%22'

# Zenodo: top button and CV profile link should list all works.
source = source.replace("ZENODO_URL=CHAPTER_URL", f"ZENODO_URL='{ZENODO_ALL}'")
source = source.replace("('Zenodo - Kitap Bölümü',ZENODO_URL)", "('Zenodo - Tüm Çalışmalar',ZENODO_URL)")
source = source.replace(
    "html=html.replace('https://zenodo.org/search?q=%220000-0003-4844-3508%22', ZENODO_URL)",
    "html=html.replace('https://zenodo.org/search?q=%220000-0003-4844-3508%22', ZENODO_URL)\n    html=html.replace('https://zenodo.org/search?q=creators.orcid%3A%220000-0003-4844-3508%22', ZENODO_URL)\n    html=html.replace(CHAPTER_URL, ZENODO_URL)"
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
