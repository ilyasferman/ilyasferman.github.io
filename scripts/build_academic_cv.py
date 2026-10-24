from pathlib import Path
import re
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import stringWidth

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'cv' / 'ilyas-ferman-akademik-cv.pdf'
OUT.parent.mkdir(parents=True, exist_ok=True)
INDEX = ROOT / 'index.html'

font_dir = Path('/usr/share/fonts/truetype/dejavu')
pdfmetrics.registerFont(TTFont('DVSans', str(font_dir/'DejaVuSans.ttf')))
pdfmetrics.registerFont(TTFont('DVSans-Bold', str(font_dir/'DejaVuSans-Bold.ttf')))
pdfmetrics.registerFont(TTFont('DVSerif-Bold', str(font_dir/'DejaVuSerif-Bold.ttf')))

W,H=A4
NAVY=HexColor('#0d335b'); GOLD=HexColor('#c79b32'); TEXT=HexColor('#24384d')
MUTED=HexColor('#637487'); LINE=HexColor('#d9e0e7'); PALE=HexColor('#f4f7f9')
THESIS_URL='https://zenodo.org/records/23146579'
CHAPTER_URL='https://zenodo.org/records/23544985'
ZENODO_URL=CHAPTER_URL

certs=[
 {'key':'cert-istanbul','year':'2026','title':'Temel SPSS ile Nicel Veri Analizi Eğitimi - 20 saat','subtitle':'İstanbul Üniversitesi Sürekli Eğitim Uygulama ve Araştırma Merkezi','kind':'istanbul'},
 {'key':'cert-kasem-tr','year':'2026','title':'SPSS Eğitimi - 24 saat','subtitle':'Karabük Üniversitesi Sürekli Eğitim, Uygulama ve Araştırma Merkezi','kind':'kasem'},
 {'key':'cert-yonetim','year':'2026','title':'Yönetim Süreçleri ve İlkeleri','subtitle':'Ankara Üniversitesi Rektörlüğü','kind':'online'},
 {'key':'cert-kamu','year':'2025','title':'Kamu Etiği ve Kamu Görevlileri Etik Davranış İlkeleri','subtitle':'Kamu Görevlileri Etik Kurulu','kind':'online'},
 {'key':'cert-insan','year':'2025','title':'İnsan Hakları Çerçevesinde Etik','subtitle':'Kamu Görevlileri Etik Kurulu','kind':'online'},
 {'key':'cert-stres','year':'2022','title':'İş Yerinde Stres','subtitle':'Türkiye Bilimsel ve Teknolojik Araştırma Kurumu (TÜBİTAK)','kind':'online'},
]

def footer(c):
    c.setFillColor(MUTED); c.setFont('DVSans',6.8)
    c.drawCentredString(W/2,17,'İlyas Ferman · Akademik CV · ilyasferman.com')

def section(c,y,title):
    c.setFillColor(NAVY); c.setFont('DVSans-Bold',9.8); c.drawString(34,y,title.upper())
    c.setStrokeColor(GOLD); c.setLineWidth(1.15); c.line(34,y-4,W-34,y-4)
    return y-15

def lines_for(text,font,size,width):
    lines=[]; line=''
    for word in text.split():
        t=(line+' '+word).strip()
        if stringWidth(t,font,size)<=width: line=t
        else:
            if line: lines.append(line)
            line=word
    if line: lines.append(line)
    return lines

def wrapped(c,text,x,y,width,font='DVSans',size=7.4,leading=9,color=TEXT,max_lines=None):
    c.setFillColor(color); c.setFont(font,size)
    lines=lines_for(text,font,size,width)
    if max_lines: lines=lines[:max_lines]
    for ln in lines:
        c.drawString(x,y,ln); y-=leading
    return y

def row(c,year,title,subtitle,y,title_size=7.9):
    c.setFillColor(GOLD); c.setFont('DVSans-Bold',7.0); c.drawString(48,y,year)
    c.setFillColor(NAVY); c.setFont('DVSans-Bold',title_size); c.drawString(127,y,title)
    c.setFillColor(MUTED); c.setFont('DVSans',6.8); c.drawString(127,y-9.5,subtitle)
    c.setStrokeColor(LINE); c.setLineWidth(.45); c.line(48,y-15,W-44,y-15)
    return y-24

def ext_link(c,label,url,x,y,size=6.8):
    c.setFillColor(HexColor('#1f5f99')); c.setFont('DVSans',size); c.drawString(x,y,label)
    tw=stringWidth(label,'DVSans',size)
    c.linkURL(url,(x,y-2,x+tw,y+size+2),relative=0,thickness=0)

def cert_thumb(c,x,y,w,h,kind,title):
    c.setFillColor(white); c.setStrokeColor(HexColor('#cbd7e2')); c.setLineWidth(.7)
    c.roundRect(x,y,w,h,3,fill=1,stroke=1)
    if kind=='istanbul':
        c.setStrokeColor(HexColor('#1c6144')); c.setLineWidth(1.2); c.rect(x+5,y+5,w-10,h-10,fill=0,stroke=1)
        c.setFillColor(NAVY); c.setFont('DVSerif-Bold',8); c.drawCentredString(x+w/2,y+h*.69,'SERTİFİKA')
        c.setFont('DVSans-Bold',5.7); c.drawCentredString(x+w/2,y+h*.50,'İLYAS FERMAN')
        c.setFont('DVSans-Bold',4.5); c.drawCentredString(x+w/2,y+h*.30,'TEMEL SPSS İLE NİCEL VERİ ANALİZİ')
    elif kind=='kasem':
        c.setStrokeColor(NAVY); c.setLineWidth(1.0); c.rect(x+5,y+5,w-10,h-10,fill=0,stroke=1)
        c.setFillColor(NAVY); c.setFont('DVSerif-Bold',7.5); c.drawCentredString(x+w/2,y+h*.69,'EĞİTİM SERTİFİKASI')
        c.setFont('DVSans-Bold',5.7); c.drawCentredString(x+w/2,y+h*.50,'İLYAS FERMAN')
        c.setFont('DVSans-Bold',5); c.drawCentredString(x+w/2,y+h*.30,'SPSS Eğitimi')
    else:
        c.setFillColor(HexColor('#f0fafa')); c.rect(x+1,y+1,w-2,h-2,fill=1,stroke=0)
        c.setFillColor(HexColor('#5790aa')); c.setFont('DVSans-Bold',5.3); c.drawCentredString(x+w/2,y+h*.78,'eğitimkapısı')
        c.setFillColor(NAVY); c.setFont('DVSerif-Bold',7); c.drawCentredString(x+w/2,y+h*.60,'KATILIM SERTİFİKASI')
        c.setFont('DVSans-Bold',5.8); c.drawCentredString(x+w/2,y+h*.40,'İLYAS FERMAN')
        short=title if len(title)<36 else title[:33]+'...'
        c.setFont('DVSans',4.2); c.drawCentredString(x+w/2,y+h*.20,short)
    c.setFillColor(PALE); c.rect(x+w*.12,y+h*.04,w*.76,h*.10,fill=1,stroke=0)

c=canvas.Canvas(str(OUT),pagesize=A4)
c.setTitle('İlyas Ferman - Akademik CV'); c.setAuthor('İlyas Ferman')

c.setFillColor(NAVY); c.rect(30,H-126,W-60,96,fill=1,stroke=0)
c.setFillColor(white); c.setFont('DVSerif-Bold',23); c.drawString(44,H-68,'İlyas Ferman')
c.setFont('DVSans-Bold',9.5); c.drawString(44,H-85,'Acil Tıp Teknisyeni')
c.setFillColor(HexColor('#dbc980')); c.setFont('DVSans',7.1)
c.drawString(44,H-99,'Yönetim ve Organizasyon  ·  Sağlık Hizmetleri Yönetimi  ·  Yönetim Bilişim Sistemleri')
c.setFillColor(white); c.drawString(44,H-114,'Yalova, Türkiye   |   info@ilyasferman.com')
photo=ROOT/'assets'/'profile.png'
if photo.exists(): c.drawImage(str(photo),W-111,H-121,65,82,preserveAspectRatio=True,mask='auto')

y=H-145
y=section(c,y,'Profesyonel / Akademik Profil')
profile=('2011 yılından bu yana kamu sağlık hizmetlerinde Acil Tıp Teknisyeni olarak görev yapıyorum. '
'Saha deneyimimi yönetim, sağlık hizmetleri ve işletme alanındaki akademik eğitimle birlikte sürdürüyorum. '
'Sağlık kurumları işletmeciliği, kamu yönetimi ve sağlık yönetimi alanlarında yükseköğrenim gördüm; '
'Giresun Üniversitesi İşletme yüksek lisans programını tamamladım. Hâlen Anadolu Üniversitesi Yönetim '
'Bilişim Sistemleri lisans programında öğrenimime devam ediyorum. Çalışmalarımda yönetim ve organizasyon, '
'sağlık hizmetlerinin yönetimi, kamu yönetimi, örgütsel davranış, stratejik yönetim ve yönetim bilişim sistemlerine odaklanıyorum.')
y=wrapped(c,profile,34,y,W-68,size=7.1,leading=8.3); y-=3

y=section(c,y,'Eğitim')
for d in [
('2026-Devam','Anadolu Üniversitesi - Yönetim Bilişim Sistemleri','Lisans'),
('2018-2022','Giresun Üniversitesi - İşletme','Tezli Yüksek Lisans'),
('2016-2018','İstanbul Üniversitesi - Sağlık Yönetimi','Lisans'),
('2014-2016','Anadolu Üniversitesi - Kamu Yönetimi','Lisans'),
('2012-2014','Anadolu Üniversitesi - Sağlık Kurumları İşletmeciliği','Önlisans'),
('2007-2011','Fatsa Sağlık Meslek Lisesi - Acil Tıp Teknisyenliği','Ortaöğretim')]: y=row(c,*d,y)

y+=2; y=section(c,y,'Mesleki Deneyim')
for d in [
('2024-Devam','Yalova İl Sağlık Müdürlüğü - Merkez 7 No’lu Acil Sağlık Hizmetleri İstasyonu','Acil Tıp Teknisyeni'),
('2014-2024','Ordu Fatsa 2 No’lu Acil Sağlık Hizmetleri İstasyonu','Acil Tıp Teknisyeni'),
('2011-2014','Ordu Fatsa Devlet Hastanesi','Acil Tıp Teknisyeni · Kamu görevine Eylül 2011’de başlama')]: y=row(c,*d,y,title_size=7.4)

y+=2; y=section(c,y,'Akademik Çalışmalar')
c.setFillColor(NAVY); c.setFont('DVSans-Bold',7.5); c.drawString(34,y,'Yüksek Lisans Tezi')
y-=10
y=wrapped(c,'112 Acil Servis Çalışanlarının İş Güçlüğü ve İş Riski Sorunları; Ordu İli 112 Acil Servis Çalışanları Üzerinde Bir Araştırma',34,y,W-68,font='DVSans-Bold',size=6.8,leading=8.0,color=NAVY,max_lines=2)
c.setFillColor(MUTED); c.setFont('DVSans',6.2); c.drawString(34,y,'Giresun Üniversitesi · İşletme · 2022 · Danışman: Doç. Dr. İhsan Cora · YÖK Tez No: 747495'); y-=10
ext_link(c,'Zenodo: https://zenodo.org/records/23146579',THESIS_URL,34,y,6.1); y-=13
c.setFillColor(NAVY); c.setFont('DVSans-Bold',7.5); c.drawString(34,y,'Kitap Bölümü · Endüstri 3.0 ve Endüstri 4.0'); y-=10
c.setFillColor(MUTED); c.setFont('DVSans',6.1); c.drawString(34,y,'Platanus Publishing · Sosyal Bilimlerde Güncel Gelişmeler ve Tematik İncelemeler · Bölüm 34 · ss. 756-767 · 2026'); y-=10
ext_link(c,'DOI: https://doi.org/10.5281/zenodo.23544985',CHAPTER_URL,34,y,6.1); y-=14

y=section(c,y,'Araştırma Alanları')
y=wrapped(c,'Yönetim ve Organizasyon · Sağlık Hizmetleri Yönetimi · Yönetim Bilişim Sistemleri · Stratejik Yönetim · Örgütsel Davranış · Kamu Yönetimi ve Politika · Dijitalleşme ve kurumsal teknoloji uyumu',34,y,W-68,size=6.5,leading=7.8); y-=2

y=section(c,y,'Yabancı Dil')
c.setFillColor(TEXT); c.setFont('DVSans',6.5); c.drawString(34,y,'İngilizce: Akademik okuma ileri düzey (öz değerlendirme); konuşma becerisi gelişmekte. Yabancı dil sınav puanı: 55.')
footer(c); c.showPage()

ystart=H-44; y=section(c,ystart,'Sertifikalar')
col_gap=14; card_w=(W-68-col_gap)/2; card_h=151; xs=[34,34+card_w+col_gap]
for i,ci in enumerate(certs):
    col=i%2; r=i//2; x=xs[col]; top=y-r*card_h
    c.setStrokeColor(LINE); c.setLineWidth(.55); c.roundRect(x,top-card_h+8,card_w,card_h-8,5,stroke=1,fill=0)
    thumb_w=card_w-30; thumb_h=86; tx=x+15; ty=top-94
    cert_thumb(c,tx,ty,thumb_w,thumb_h,ci['kind'],ci['title'])
    url='https://ilyasferman.com/?cert='+ci['key']+'#sertifikalar'
    c.linkURL(url,(tx,ty,tx+thumb_w,ty+thumb_h),relative=0,thickness=0)
    by=top-107
    c.setFillColor(GOLD); c.setFont('DVSans-Bold',6.7); c.drawString(x+8,by,ci['year'])
    c.setFillColor(NAVY); c.setFont('DVSans-Bold',6.8)
    title_lines=lines_for(ci['title'],'DVSans-Bold',6.8,card_w-56)[:2]
    for j,ln in enumerate(title_lines): c.drawString(x+43,by-j*7.8,ln)
    sy=by-max(1,len(title_lines))*7.8-2
    c.setFillColor(MUTED); c.setFont('DVSans',5.8)
    sublines=lines_for(ci['subtitle'],'DVSans',5.8,card_w-16)[:2]
    for j,ln in enumerate(sublines): c.drawString(x+8,sy-j*6.8,ln)

py=y-3*card_h-2; py=section(c,py,'Akademik Profiller ve İletişim')
profiles=[
('ORCID','https://orcid.org/0000-0003-4844-3508'),
('Google Scholar','https://scholar.google.com/citations?user=lYZXEKEAAAAJ&hl=tr'),
('ResearchGate','https://www.researchgate.net/profile/Ilyas-Ferman-2'),
('Zenodo - Kitap Bölümü',ZENODO_URL),
('Kişisel web sitesi','https://ilyasferman.com'),
('E-posta','mailto:info@ilyasferman.com')]
for label,url in profiles:
    c.setFillColor(NAVY); c.setFont('DVSans-Bold',6.6); c.drawString(34,py,label+':')
    lx=34+stringWidth(label+': ','DVSans-Bold',6.6)
    display=url.replace('mailto:',''); c.setFillColor(TEXT); c.setFont('DVSans',6.5); c.drawString(lx,py,display)
    c.linkURL(url,(lx,py-2,min(W-34,lx+stringWidth(display,'DVSans',6.5)),py+7),relative=0,thickness=0)
    py-=11
footer(c); c.save()

if INDEX.exists():
    html=INDEX.read_text(encoding='utf-8')
    html=html.replace('https://zenodo.org/search?q=%220000-0003-4844-3508%22', ZENODO_URL)
    html=html.replace('<div class="card-head"><div class="head-left"><span class="gold-icon">▮▮</span><h2>Araştırma Alanları</h2></div><a href="#research-detail">Daha fazla <span>→</span></a></div>',
                      '<div class="card-head"><div class="head-left"><span class="gold-icon">▮▮</span><h2>Araştırma Alanları</h2></div></div>')
    html=re.sub(r'\n\s*<section class="detail-section soft" id="research-detail">.*?</section>\s*\n', '\n', html, count=1, flags=re.S)
    html=html.replace('<div class="section-title"><p>SEÇİLMİŞ EĞİTİMLER</p><h2>Sertifikalar ve mesleki gelişim</h2></div>',
                      '<div class="section-title"><h2>Sertifikalar</h2></div>')
    html=re.sub(r'\n\s*<section class="thesis-feature">.*?</section>\s*\n', '\n', html, count=1, flags=re.S)
    marker="""    document.querySelectorAll('.certificate-trigger').forEach(button => button.addEventListener('click', () => {
      const template = document.getElementById(button.dataset.template);
      htmlViewer.replaceChildren(template.content.cloneNode(true));
      htmlViewer.hidden = false;
      frame.hidden = true;
      newTab.hidden = true;
      openModal(button.dataset.title);
    }));"""
    if marker in html and "new URLSearchParams(window.location.search).get('cert')" not in html:
        addition=marker+"""
    const requestedCertificate = new URLSearchParams(window.location.search).get('cert');
    if(requestedCertificate){
      const certificateButton = document.querySelector('.certificate-trigger[data-template="' + requestedCertificate + '"]');
      if(certificateButton) setTimeout(() => certificateButton.click(), 0);
    }"""
        html=html.replace(marker,addition)
    INDEX.write_text(html,encoding='utf-8')

print(OUT)
