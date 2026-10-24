from pathlib import Path

index_path = Path('index.html')
css_path = Path('assets/site-final.css')
html = index_path.read_text(encoding='utf-8')
css = css_path.read_text(encoding='utf-8')

html = html.replace(
    '<a href="cv/ilyas-ferman-akademik-cv.pdf" target="_blank" rel="noopener">CV</a>',
    '<a href="#cv">CV</a>'
)

cv_section = '''
    <section class="detail-section soft cv-section" id="cv">
      <div class="section-title">
        <p>AKADEMİK ÖZGEÇMİŞ</p>
        <h2>Akademik CV</h2>
      </div>
      <div class="cv-showcase">
        <button class="cv-preview-card document-trigger" type="button" data-document="cv/ilyas-ferman-akademik-cv.pdf" data-document-title="İlyas Ferman · Akademik CV" aria-label="Akademik CV'yi büyük görüntüle">
          <img src="assets/cv-preview.jpg" alt="İlyas Ferman akademik CV ilk sayfa önizlemesi" loading="lazy">
          <span class="cv-preview-overlay">Büyük görüntüle ↗</span>
        </button>
        <article class="cv-info-card">
          <span class="cv-kicker">İLYAS FERMAN · AKADEMİK CV</span>
          <h3>Eğitim, mesleki deneyim ve akademik çalışmalar</h3>
          <p>Akademik özgeçmiş; eğitim geçmişi, kamu sağlık hizmetlerindeki mesleki deneyim, araştırma alanları ve akademik çalışmaların güncel özetini içerir.</p>
          <div class="cv-facts">
            <span><strong>Alanlar</strong> Yönetim · Sağlık Hizmetleri · Yönetim Bilişim Sistemleri</span>
            <span><strong>Konum</strong> Yalova, Türkiye</span>
            <span><strong>Profil</strong> Akademik ve profesyonel özgeçmiş</span>
          </div>
          <div class="cv-actions">
            <button class="btn btn-primary document-trigger" type="button" data-document="cv/ilyas-ferman-akademik-cv.pdf" data-document-title="İlyas Ferman · Akademik CV"><span class="doc-icon">▤</span> CV'yi büyük görüntüle <span>→</span></button>
            <a class="btn btn-light" href="cv/ilyas-ferman-akademik-cv.pdf" target="_blank" rel="noopener">Yeni sekmede aç ↗</a>
          </div>
        </article>
      </div>
    </section>
'''

marker = '    <section class="thesis-feature">'
if 'id="cv"' not in html:
    if marker not in html:
        raise SystemExit('CV insertion marker not found')
    html = html.replace(marker, cv_section + '\n' + marker, 1)

css_block = r'''

/* Academic CV showcase */
.cv-section{scroll-margin-top:72px}
.cv-showcase{display:grid;grid-template-columns:minmax(300px,430px) 1fr;gap:26px;align-items:stretch}
.cv-preview-card{appearance:none;border:1px solid var(--line);border-radius:12px;background:#eef2f5;padding:12px;box-shadow:var(--shadow);cursor:pointer;position:relative;overflow:hidden;min-height:520px;display:flex;align-items:flex-start;justify-content:center}
.cv-preview-card img{width:100%;height:auto;border-radius:6px;background:#fff;box-shadow:0 8px 28px rgba(8,39,70,.12)}
.cv-preview-overlay{position:absolute;left:24px;right:24px;bottom:24px;background:rgba(8,39,70,.92);color:#fff;border-radius:7px;padding:12px 14px;font-family:Arial,sans-serif;font-size:13px;font-weight:800;text-align:center;box-shadow:0 6px 18px rgba(8,39,70,.18)}
.cv-preview-card:hover .cv-preview-overlay{background:#0d335b}
.cv-info-card{border:1px solid var(--line);border-radius:12px;background:#fff;padding:32px;box-shadow:var(--shadow);display:flex;flex-direction:column;justify-content:center}
.cv-kicker{font-family:Arial,sans-serif;font-size:11px;letter-spacing:.16em;font-weight:800;color:var(--gold)}
.cv-info-card h3{font-size:30px;line-height:1.18;color:var(--navy);margin:12px 0 12px}
.cv-info-card>p{font-family:Arial,sans-serif;color:#587087;font-size:14px;line-height:1.65;margin:0 0 22px;max-width:760px}
.cv-facts{display:grid;gap:0;border-top:1px solid #e8edf1;border-bottom:1px solid #e8edf1;margin-bottom:24px}
.cv-facts span{display:grid;grid-template-columns:90px 1fr;gap:14px;padding:12px 0;border-bottom:1px solid #edf0f3;font-family:Arial,sans-serif;font-size:13px;color:#5c6b7c}
.cv-facts span:last-child{border-bottom:0}.cv-facts strong{color:var(--navy)}
.cv-actions{display:flex;gap:10px;flex-wrap:wrap}
@media(max-width:900px){.cv-showcase{grid-template-columns:1fr}.cv-preview-card{max-width:520px;width:100%;margin:auto;min-height:0}.cv-info-card{padding:24px}.cv-info-card h3{font-size:26px}}
@media(max-width:690px){.cv-preview-card{padding:8px}.cv-preview-overlay{left:16px;right:16px;bottom:16px}.cv-info-card{padding:20px}.cv-info-card h3{font-size:23px}.cv-facts span{grid-template-columns:76px 1fr}.cv-actions .btn{width:100%}}
'''

if '/* Academic CV showcase */' not in css:
    css += css_block

index_path.write_text(html, encoding='utf-8')
css_path.write_text(css, encoding='utf-8')
