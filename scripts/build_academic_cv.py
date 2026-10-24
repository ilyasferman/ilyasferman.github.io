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

# Fonts
font_dir = Path('/usr/share/fonts/truetype/dejavu')
pdfmetrics.registerFont(TTFont('DVSans', str(font_dir/'DejaVuSans.ttf')))
pdfmetrics.registerFont(TTFont('DVSans-Bold', str(font_dir/'DejaVuSans-Bold.ttf')))
pdfmetrics.registerFont(TTFont('DVSerif', str(font_dir/'DejaVuSerif.ttf')))
pdfmetrics.registerFont(TTFont('DVSerif-Bold', str(font_dir/'DejaVuSerif-Bold.ttf')))

W,H=A4
NAVY=HexColor('#0d335b'); GOLD=HexColor('#c79b32'); TEXT=HexColor('#24384d')
MUTED=HexColor('#637487'); LINE=HexColor('#d9e0e7'); PALE=HexColor('#f4f7f9')

THESIS_URL='https://doi.org/10.5281/zenodo.23146579'
CHAPTER_URL='https://doi.org/10.5281/zenodo.23544985'
ZENODO_URL='https://zenodo.org/search?q=%220000-0003-4844-3508%22'

certs=[
 {'key':'istanbul','year':'2026','title':'Temel SPSS ile Nicel Veri Analizi Eğitimi','subtitle':'İstanbul Üniversitesi Sürekli Eğitim Uygulama ve Araştırma Merkezi · 20 saat','pages':1,'kind':'istanbul'},
 {'key':'kasem_tr','year':'2026','title':'SPSS Eğitimi · Türkçe','subtitle':'Karabük Üniversitesi Sürekli Eğitim, Uygulama ve Araştırma Merkezi · 24 saat','pages':3,'kind':'kasem_tr'},
 {'key':'kasem_en','year':'2026','title':'SPSS Training · English','subtitle':'Karabuk University Continuing Education Application and Research Center · 24 hours','pages':3,'kind':'kasem_en'},
 {'key':'yonetim','year':'2026','title':'Yönetim Süreçleri ve İlkeleri','subtitle':'Ankara Üniversitesi Rektörlüğü','pages':1,'kind':'online'},
 {'key':'kamu','year':'2025','title':'Kamu Etiği ve Kamu Görevlileri Etik Davranış İlkeleri','subtitle':'Kamu Görevlileri Etik Kurulu','pages':1,'kind':'online'},
 {'key':'insan','year':'2025','title':'İnsan Hakları Çerçevesinde Etik','subtitle':'Kamu Görevlileri Etik Kurulu','pages':1,'kind':'online'},
 {'key':'stres','year':'2022','title':'İş Yerinde Stres','subtitle':'Türkiye Bilimsel ve Teknolojik Araştırma Kurumu (TÜBİTAK)','pages':1,'kind':'online'},
]

tr_topics_1=['Temel İstatistik Bilgileri','Anket Verilerine Bakış','Evren ve Örneklem','Betimsel ve Çıkarımsal İstatistik','Değişken, Sabit Parametre','Bağımlı Bağımsız Değişken','Ölçüm Düzeyleri','Sınıflama (Nominal) Ölçek','Sıralama (Ordinal) Ölçek','Eşit Aralıklı (Interval) Ölçek','Temel İstatistiksel Kavramlar','Ortalama','Mod','Medyan','Standart Sapma','Varyans','Korelasyon','Kovaryans','Normal Dağılım','Hipotez Testleri','Hipotez Testinin Aşamaları','Programın Arayüzünün Tanıtılması','Programdaki Menüler','Çalışma Dosyasının Kaydedilmesi ve Açılması','Programda Değişken Görünümü ve Veri Görünümü','Değişken Oluşturma ve Değişkene Özel Ayarlar','Veri Etiketlerinin Girilmesi','Kategorik Değişkenlere İlişkin Kategori İsimlerinin Atanması','Değişkenin Ölçme Düzeyinin Atanması','Atanan Değişkene İlişkin Veri Girişi','Sürekli Değişkenlerin Kategorik Değişkene Dönüştürülmesi','Görsel Gruplama']
tr_topics_2=['Görsel Gruplama','Gözlem ve Değişken Erişimi','Gözlem ve Frekans İlave Etme','Değişkenleri Artan ve Azalan Olarak Sıralama','Alt Küme Olarak Belirli Koşulla Gözlem Seçme','Gözlemleri Ağırlıklandırma','Kategorik Değişkenleri Yeniden Kodlayarak Birleştirme','Değişkenlerden Yeni Değişken Üretmek','Ölçek Hesaplamaları','Anket Verilerinin Güvenilirliğinin Analizi','Çapraz Tablolar Oluşturmak','Frekans Tabloları Oluşturmak','Betimsel İstatistikler Elde Etmek','Normal Dağılım Testlerine İlişkin Hipotezlerin Kurulması','Normal Dağılım Testi','Grup Ortalamalarının Testi','Tek Örneklem T Testi','Bağımsız Örneklem T Testi','Parametrik Olmayan Bağımsız Örneklem Testi (Mann Whitney U)']
en_topics_1=['Basic Statistical Information','A Look at Survey Data','Population and Sample','Descriptive and Inferential Statistics','Variable, Fixed Parameter','Dependent Independent Variable','Measurement Levels','Classification (Nominal) Scale','Ordinal Scale','Interval Scale','Basic Statistical Concepts','Average','Mode','Median','Standard Deviation','Variance','Correlation','Covariance','Normal Distribution','Hypothesis Tests','Stages of Hypothesis Testing','Introducing the Interface of the Program','Menus in the Program','Saving and Opening the Work File','Variable View and Data View in Program','Creating a Variable and Variable-Specific Settings','Entering Data Effects','Assigning Category Names to Categorical Variables','Assigning the Measurement Level of the Variable','Data Entry for Assigned Variable','Converting Continuous Variables to Categorical Variables','Visual Grouping']
en_topics_2=['Visual Grouping','Observation and Variable Access','Observing and Adding Frequencies','Sorting Variables Ascending and Descending','Selecting Observations as a Subset with Specific Conditions','Weighting Observations','Combining Categorical Variables by Recoding','Creating New Variables from Variables','Scale Calculations','Analysis of Reliability of Survey Data','Creating Crosstabs','Creating Frequency Tables','Obtaining Descriptive Statistics','Establishing Hypotheses Regarding Normal Distribution Tests','Normal Distribution Test','Test of Group Means','One Sample T Test','Independent Sample T Test','Nonparametric Independent Sample Test (Mann Whitney U)']

def footer(c,n):
 c.setFillColor(MUTED); c.setFont('DVSans',7); c.drawCentredString(W/2,18,'İlyas Ferman · Akademik CV · ilyasferman.com'); c.drawRightString(W-28,18,str(n))

def section(c,y,title):
 c.setFillColor(NAVY); c.setFont('DVSans-Bold',11.2); c.drawString(28,y,title); c.setStrokeColor(GOLD); c.setLineWidth(1.3); c.line(28,y-5,W-28,y-5); return y-18

def wrapped(c,text,x,y,width,font='DVSans',size=8,leading=10.5,color=TEXT,max_lines=None):
 c.setFillColor(color); c.setFont(font,size); lines=[]; line=''
 for word in text.split():
  t=(line+' '+word).strip()
  if stringWidth(t,font,size)<=width: line=t
  else:
   if line: lines.append(line)
   line=word
 if line: lines.append(line)
 if max_lines: lines=lines[:max_lines]
 for ln in lines: c.drawString(x,y,ln); y-=leading
 return y

def ext_link(c,label,url,x,y,size=7.6):
 c.setFillColor(HexColor('#1f5f99')); c.setFont('DVSans',size); c.drawString(x,y,label); tw=stringWidth(label,'DVSans',size); c.linkURL(url,(x,y-2,x+tw,y+size+2),relative=0,thickness=0); c.setStrokeColor(HexColor('#1f5f99')); c.setLineWidth(.25); c.line(x,y-1,x+tw,y-1)

def fit_text(c,text,x,y,w,size=8,font='DVSans-Bold',color=NAVY,max_lines=2):
 return wrapped(c,text,x,y,w,font,size,size+2,color,max_lines)

def cert_frame(c,x,y,w,h,kind,page_no=1,mini=False,title=''):
 # Shared stylized public certificate representation; intentionally omits ID/QR/signature data.
 if kind in ('kasem_tr','kasem_en'):
  c.setFillColor(white); c.setStrokeColor(NAVY); c.setLineWidth(max(.8,w/250)); c.roundRect(x,y,w,h,4,fill=1,stroke=1)
  if page_no==1:
   head='EĞİTİM SERTİFİKASI' if kind=='kasem_tr' else 'TRAINING CERTIFICATE'
   course='SPSS Eğitimi' if kind=='kasem_tr' else 'SPSS Training'
   issuer='Karabük Üniversitesi' if kind=='kasem_tr' else 'Karabuk University'
   c.setFillColor(NAVY); c.setFont('DVSerif-Bold',max(5,w/30)); c.drawCentredString(x+w/2,y+h*.78,head)
   c.setFont('DVSans-Bold',max(4,w/40)); c.drawCentredString(x+w/2,y+h*.61,'İLYAS FERMAN')
   c.setFont('DVSans',max(3.5,w/48)); c.drawCentredString(x+w/2,y+h*.48,issuer)
   c.setFont('DVSans-Bold',max(4,w/42)); c.drawCentredString(x+w/2,y+h*.36,course)
  else:
   head='TRANSKRİPT ve İÇERİK BELGESİ' if kind=='kasem_tr' else 'TRANSCRIPT and CONTENT DOCUMENT'
   c.setFillColor(NAVY); c.setFont('DVSerif-Bold',max(4.2,w/34)); c.drawCentredString(x+w/2,y+h*.83,head)
   topics=(tr_topics_1 if page_no==2 else tr_topics_2) if kind=='kasem_tr' else (en_topics_1 if page_no==2 else en_topics_2)
   c.setFillColor(TEXT); c.setFont('DVSans',max(2.6,w/72));
   cols=2; per=(len(topics)+1)//2
   for j,t in enumerate(topics[:min(len(topics),22 if mini else len(topics))]):
    col=j//per; row=j%per
    xx=x+w*(.08+.48*col); yy=y+h*(.70-row*(.045 if not mini else .07))
    if yy>y+h*.10: c.drawString(xx,yy,t[:42])
 else:
  bg=HexColor('#f3fbfc') if kind=='online' else white
  c.setFillColor(bg); c.setStrokeColor(HexColor('#d7e5ea') if kind=='online' else NAVY); c.setLineWidth(max(.6,w/300)); c.rect(x,y,w,h,fill=1,stroke=1)
  if kind=='istanbul':
   c.setStrokeColor(HexColor('#1c6144')); c.setLineWidth(max(1,w/180)); c.rect(x+w*.02,y+h*.02,w*.96,h*.96,fill=0,stroke=1)
   c.setFillColor(NAVY); c.setFont('DVSerif-Bold',max(5,w/28)); c.drawCentredString(x+w/2,y+h*.76,'SERTİFİKA')
   c.setFont('DVSans-Bold',max(4,w/38)); c.drawCentredString(x+w/2,y+h*.60,'İLYAS FERMAN')
   c.setFont('DVSans-Bold',max(3.5,w/48)); c.drawCentredString(x+w/2,y+h*.42,'TEMEL SPSS İLE NİCEL VERİ ANALİZİ EĞİTİMİ')
  else:
   c.setFillColor(NAVY); c.setFont('DVSans-Bold',max(5,w/26)); c.drawCentredString(x+w/2,y+h*.76,'KATILIM SERTİFİKASI')
   c.setFont('DVSans-Bold',max(4.2,w/36)); c.drawCentredString(x+w/2,y+h*.55,'İLYAS FERMAN')
   c.setFont('DVSans-Bold',max(3.5,w/48)); c.drawCentredString(x+w/2,y+h*.36,title[:54])
 # Safety/public-copy note area
 c.setFillColor(HexColor('#f7f8fa')); c.rect(x+w*.08,y+h*.05,w*.84,h*.11,fill=1,stroke=0)
 c.setFillColor(MUTED); c.setFont('DVSans',max(2.5,w/80)); c.drawCentredString(x+w/2,y+h*.09,'Kimlik, doğrulama ve imza alanları kamuya açık kopyada gizlenmiştir.')

def draw_cert_full(c,ci,pno):
 c.setFillColor(GOLD); c.setFont('DVSans-Bold',7); c.drawString(28,H-28,f"{ci['year']} · {ci['title']}")
 c.setFillColor(MUTED); c.setFont('DVSans',6.6); c.drawString(28,H-40,f"Sayfa {pno}/{ci['pages']} · Kamuya açık kopya")
 x,y=38,68; w,h=W-76,H-135
 cert_frame(c,x,y,w,h,ci['kind'],pno,mini=False,title=ci['title'])
 c.setFillColor(HexColor('#1f5f99')); c.setFont('DVSans-Bold',7); c.drawString(28,31,'← Sertifika listesine dön'); c.linkRect('', 'cert-gallery',(25,25,150,42),relative=0,thickness=0)

c=canvas.Canvas(str(OUT),pagesize=A4); c.setTitle('İlyas Ferman - Akademik CV'); c.setAuthor('İlyas Ferman')
# Page 1
c.setFillColor(NAVY); c.rect(24,H-132,W-48,106,fill=1,stroke=0)
c.setFillColor(white); c.setFont('DVSerif-Bold',25); c.drawString(35,H-68,'İlyas Ferman')
c.setFont('DVSans-Bold',10); c.drawString(35,H-86,'Acil Tıp Teknisyeni')
c.setFont('DVSans',7.5); c.drawString(35,H-101,'Yönetim ve Organizasyon  ·  Sağlık Hizmetleri Yönetimi  ·  Yönetim Bilişim Sistemleri')
c.drawString(35,H-116,'Yalova, Türkiye   |   info@ilyasferman.com')
photo=ROOT/'assets'/'profile.png'
if photo.exists(): c.drawImage(str(photo),W-112,H-124,76,90,preserveAspectRatio=True,mask='auto')
y=H-153; y=section(c,y,'PROFESYONEL / AKADEMİK PROFİL')
profile='2011 yılından bu yana kamu sağlık hizmetlerinde Acil Tıp Teknisyeni olarak görev yapıyorum. Saha deneyimimi yönetim, sağlık hizmetleri ve işletme alanındaki akademik eğitimle birlikte sürdürüyorum. Sağlık kurumları işletmeciliği, kamu yönetimi ve sağlık yönetimi alanlarında yükseköğrenim gördüm; Giresun Üniversitesi İşletme yüksek lisans programını tamamladım. Hâlen Anadolu Üniversitesi Yönetim Bilişim Sistemleri lisans programında öğrenimime devam ediyorum. Çalışmalarımda yönetim ve organizasyon, sağlık hizmetlerinin yönetimi, kamu yönetimi, örgütsel davranış, stratejik yönetim ve yönetim bilişim sistemlerine odaklanıyorum.'
y=wrapped(c,profile,28,y,W-56,size=8.1,leading=11); y-=10; y=section(c,y,'EĞİTİM')
for yr,school,degree in [('2026-Devam','Anadolu Üniversitesi - Yönetim Bilişim Sistemleri','Lisans'),('2018-2022','Giresun Üniversitesi - İşletme','Tezli Yüksek Lisans'),('2016-2018','İstanbul Üniversitesi - Sağlık Yönetimi','Lisans'),('2014-2016','Anadolu Üniversitesi - Kamu Yönetimi','Lisans'),('2012-2014','Anadolu Üniversitesi - Sağlık Kurumları İşletmeciliği','Önlisans'),('2007-2011','Fatsa Sağlık Meslek Lisesi - Acil Tıp Teknisyenliği','Ortaöğretim')]:
 c.setFillColor(GOLD); c.setFont('DVSans-Bold',7.5); c.drawString(42,y,yr); c.setFillColor(NAVY); c.setFont('DVSans-Bold',8.5); c.drawString(118,y,school); c.setFillColor(MUTED); c.setFont('DVSans',7.5); c.drawString(118,y-11,degree); c.setStrokeColor(LINE); c.line(42,y-16,W-42,y-16); y-=31
y-=4; y=section(c,y,'MESLEKİ DENEYİM')
for yr,place,role in [('2024-Devam','Yalova İl Sağlık Müdürlüğü - Merkez 7 No’lu Acil Sağlık Hizmetleri İstasyonu','Acil Tıp Teknisyeni'),('2014-2024','Ordu Fatsa 2 No’lu Acil Sağlık Hizmetleri İstasyonu','Acil Tıp Teknisyeni'),('2011-2014','Ordu Fatsa Devlet Hastanesi','Acil Tıp Teknisyeni · Kamu görevine Eylül 2011’de başlama')]:
 c.setFillColor(GOLD); c.setFont('DVSans-Bold',7.5); c.drawString(42,y,yr); c.setFillColor(NAVY); c.setFont('DVSans-Bold',8.5); c.drawString(118,y,place); c.setFillColor(MUTED); c.setFont('DVSans',7.4); c.drawString(118,y-11,role); c.setStrokeColor(LINE); c.line(42,y-16,W-42,y-16); y-=34
footer(c,1); c.showPage()
# Page 2
c.bookmarkPage('academic-works'); y=H-42; y=section(c,y,'AKADEMİK ÇALIŞMALAR')
c.setFillColor(GOLD); c.setFont('DVSans-Bold',9); c.drawString(32,y,'1'); c.setFillColor(NAVY); c.setFont('DVSans-Bold',10.3); c.drawString(55,y,'Yüksek Lisans Tezi'); y-=17
y=wrapped(c,'112 Acil Servis Çalışanlarının İş Güçlüğü ve İş Riski Sorunları; Ordu İli 112 Acil Servis Çalışanları Üzerinde Bir Araştırma',55,y,W-85,font='DVSerif-Bold',size=9.6,leading=12.5)
c.setFillColor(MUTED); c.setFont('DVSans',7.4); c.drawString(55,y-1,'Giresun Üniversitesi · Sosyal Bilimler Enstitüsü · İşletme · 2022 · Danışman: Doç. Dr. İhsan Cora · YÖK Tez No: 747495'); y-=16; ext_link(c,'Zenodo DOI: 10.5281/zenodo.23146579',THESIS_URL,55,y); y-=26
c.setFillColor(GOLD); c.setFont('DVSans-Bold',9); c.drawString(32,y,'2'); c.setFillColor(NAVY); c.setFont('DVSans-Bold',10.3); c.drawString(55,y,'Kitap Bölümü'); y-=17
c.setFillColor(TEXT); c.setFont('DVSerif-Bold',10); c.drawString(55,y,'Endüstri 3.0 ve Endüstri 4.0'); y-=14
y=wrapped(c,'Platanus Publishing · Sosyal Bilimlerde Güncel Gelişmeler ve Tematik İncelemeler · Bölüm 34 · ss. 756-767 · 2026',55,y,W-85,size=7.5,leading=10,color=MUTED); ext_link(c,'DOI: 10.5281/zenodo.23544985',CHAPTER_URL,55,y); y-=30
y=section(c,y,'ARAŞTIRMA ALANLARI'); y=wrapped(c,'Yönetim ve Organizasyon · Sağlık Hizmetleri Yönetimi · Yönetim Bilişim Sistemleri · Stratejik Yönetim · Örgütsel Davranış · Kamu Yönetimi ve Politika · Dijitalleşme ve kurumsal teknoloji uyumu',32,y,W-64,size=8,leading=10.5); y-=18
y=section(c,y,'AKADEMİK PROFİLLER VE İLETİŞİM')
for label,url in [('ORCID','https://orcid.org/0000-0003-4844-3508'),('Google Scholar','https://scholar.google.com/citations?user=lYZXEKEAAAAJ&hl=tr'),('ResearchGate','https://www.researchgate.net/profile/Ilyas-Ferman-2'),('Zenodo',ZENODO_URL),('Kişisel web sitesi','https://ilyasferman.com'),('E-posta','mailto:info@ilyasferman.com')]:
 c.setFillColor(NAVY); c.setFont('DVSans-Bold',8); c.drawString(32,y,label+':'); ext_link(c,url,url,125,y,size=7.4); y-=17
y-=8; y=section(c,y,'SERTİFİKALAR VE SEÇİLMİŞ MESLEKİ EĞİTİMLER'); c.setFillColor(MUTED); c.setFont('DVSans',8); c.drawString(32,y,'Belge önizlemeleri ve büyütülebilir sertifika sayfaları sonraki sayfadadır.')
footer(c,2); c.showPage()
# Page 3 gallery
c.bookmarkPage('cert-gallery'); c.setFillColor(GOLD); c.setFont('DVSans-Bold',8); c.drawString(28,H-38,'BELGE GALERİSİ'); c.setFillColor(NAVY); c.setFont('DVSerif-Bold',21); c.drawString(28,H-62,'Sertifikalar ve Mesleki Eğitimler'); c.setFillColor(MUTED); c.setFont('DVSans',7.4); c.drawString(28,H-78,'Küçük belge görseline tıklayın; ilgili sertifikanın büyük kopyasına geçin.')
margin=28; gap=14; top=H-95; card_w=(W-2*margin-gap)/2; card_h=164
for i,ci in enumerate(certs):
 col=i%2; row=i//2; x=margin+col*(card_w+gap); y0=top-(row+1)*card_h-row*10
 c.setFillColor(white); c.setStrokeColor(LINE); c.roundRect(x,y0,card_w,card_h,7,fill=1,stroke=1); c.setFillColor(GOLD); c.setFont('DVSans-Bold',7); c.drawString(x+10,y0+card_h-16,ci['year']); fit_text(c,ci['title'],x+10,y0+card_h-30,card_w-20,8.1)
 tx=x+18; ty=y0+27; tw=card_w-36; th=72; cert_frame(c,tx,ty,tw,th,ci['kind'],1,mini=True,title=ci['title']); c.linkRect('',f"cert_{ci['key']}",(tx,ty,tx+tw,ty+th),relative=0,thickness=0)
 c.setFillColor(MUTED); c.setFont('DVSans',6.1); sub=ci['subtitle'];
 if stringWidth(sub,'DVSans',6.1)>card_w-20: sub=sub[:66]+'…'
 c.drawCentredString(x+card_w/2,y0+12,sub)
footer(c,3); c.showPage()
# Appendix
pnum=4
for ci in certs:
 for p in range(1,ci['pages']+1):
  if p==1: c.bookmarkPage(f"cert_{ci['key']}")
  draw_cert_full(c,ci,p); footer(c,pnum); pnum+=1; c.showPage()
c.save()

# Patch website: keep CV only in top menu, add Zenodo beside academic profile buttons.
if INDEX.exists():
 html=INDEX.read_text(encoding='utf-8')
 # Remove any hero CV viewer button if an older copy reappears.
 html=re.sub(r'\s*<button class="btn btn-primary document-trigger"[^>]*>.*?CV Görüntüle.*?</button>\s*','\n',html,count=1,flags=re.S)
 # Ensure menu CV opens the existing modal viewer.
 html=html.replace('<a href="#cv">CV</a>','<a class="document-trigger" href="cv/ilyas-ferman-akademik-cv.pdf" data-document="cv/ilyas-ferman-akademik-cv.pdf" data-document-title="İlyas Ferman · Akademik CV">CV</a>')
 # Remove obsolete dedicated CV section if present.
 html=re.sub(r'\n\s*<section class="detail-section soft cv-section" id="cv">.*?</section>\s*\n','\n',html,count=1,flags=re.S)
 rg='<a class="btn btn-light" href="https://www.researchgate.net/profile/Ilyas-Ferman-2" target="_blank" rel="noopener"><span class="logo-dot rg">RG</span> ResearchGate</a>'
 zen='<a class="btn btn-light" href="'+ZENODO_URL+'" target="_blank" rel="noopener"><span class="logo-dot scholar">Z</span> Zenodo</a>'
 hero=html.split('<div class="hero-actions" aria-label="Akademik bağlantılar">',1)
 if len(hero)==2:
  before,rest=hero; block,after=rest.split('</div>',1)
  if '> Zenodo</a>' not in block and rg in block:
   block=block.replace(rg,rg+'\n            '+zen)
  html=before+'<div class="hero-actions" aria-label="Akademik bağlantılar">'+block+'</div>'+after
 INDEX.write_text(html,encoding='utf-8')
print(OUT)
