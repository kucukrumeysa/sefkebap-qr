# 🔥 Şef Kebab — QR Menü Sistemi

Premium Django tabanlı dijital restoran menü sistemi. QR kod okutulunca doğrudan menüye yönlendirir. Admin panelinden tam yönetim.

---

## ✨ Özellikler

| Özellik | Detay |
|---|---|
| 📱 Mobil Uyumlu | Bootstrap 5, responsive tasarım |
| 🎨 Premium Tema | Cormorant Garamond + Inter + Montserrat fontları |
| 🔧 Admin Paneli | Kategori, ürün, görsel, aktif/pasif yönetimi |
| 📸 Görsel Yönetimi | Pillow ile resim yükleme ve önizleme |
| 🔗 QR Kod | Statik QR, her zaman aynı URL'e yönlendirir |
| 🏷️ Badge Sistemi | "Çok Satan", "Mevcut Değil" etiketleri |
| 🧭 Sticky Navbar | Kategori bazlı smooth scroll navigasyon |
| 🌙 Açık/Kapalı | Çalışma saatine göre otomatik durum |
| 📍 Konum & WhatsApp | Entegre iletişim butonları |

---

## 🚀 Hızlı Kurulum

```bash
git clone <repo-url>
cd sef_kebab
bash setup.sh
```

Script şunları otomatik yapar:
- Sanal ortam oluşturur
- Bağımlılıkları yükler
- `.env` dosyasını hazırlar
- Veritabanını oluşturur
- Örnek verileri yükler
- Admin kullanıcısı oluşturur

---

## 🛠️ Manuel Kurulum

```bash
# 1. Sanal ortam
python3 -m venv venv
source venv/bin/activate        # Linux/Mac
# venv\Scripts\activate         # Windows

# 2. Bağımlılıklar
pip install -r requirements.txt

# 3. Ortam değişkenleri
cp .env.example .env
# .env dosyasını düzenleyin

# 4. Veritabanı
python manage.py migrate

# 5. Örnek veriler
python manage.py loaddata apps/menu/fixtures/initial_data.json

# 6. Statik dosyalar
python manage.py collectstatic

# 7. Admin kullanıcısı
python manage.py createsuperuser

# 8. Sunucu
python manage.py runserver
```

---

## 📁 Proje Yapısı

```
sef_kebab/
├── apps/
│   └── menu/
│       ├── fixtures/
│       │   └── initial_data.json   # Örnek veriler
│       ├── migrations/
│       ├── admin.py                # Admin özelleştirmeleri
│       ├── context_processors.py   # Global restoran bilgileri
│       ├── models.py               # Category, SubCategory, Product
│       ├── urls.py
│       └── views.py
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── static/
│   ├── css/main.css
│   ├── js/main.js
│   └── images/
│       └── logo.png               # ← Logonuzu buraya koyun
├── templates/
│   ├── base.html
│   └── menu/
│       ├── home.html
│       ├── menu.html
│       ├── qr.html
│       └── partials/
│           └── product_card.html
├── media/                          # Yüklenen görseller
├── .env.example
├── manage.py
├── requirements.txt
└── setup.sh
```

---

## 🎨 Logo Ekleme

`static/images/logo.png` dosyasına logonuzu koyun.

- Önerilen boyut: **200×200 px** veya daha büyük kare görsel
- Desteklenen formatlar: PNG, JPG, SVG (PNG önerilir, transparan arka planlı)
- Logo navbar sol üstte ve footer'da otomatik görünür
- Dosya yoksa emoji fallback (🔥) gösterilir

---

## ⚙️ .env Ayarları

```env
SECRET_KEY=güvenli-bir-anahtar
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

RESTAURANT_NAME=Şef Kebab
RESTAURANT_PHONE=+90 (555) 123 45 67
RESTAURANT_ADDRESS=Örnek Mah. No:1, İstanbul
RESTAURANT_WHATSAPP=905551234567         # Ülke kodu dahil, + ve boşluk olmadan
RESTAURANT_MAPS_URL=https://maps.google.com/?q=...
RESTAURANT_OPEN_TIME=11:00
RESTAURANT_CLOSE_TIME=23:00
MENU_URL=https://siteniz.com/menu/       # QR kod bu URL'i kullanır
```

---

## 🔗 Sayfalar

| URL | Açıklama |
|---|---|
| `/` | Ana sayfa — hero, öne çıkanlar, bilgi |
| `/menu/` | Dijital menü — QR ile açılan sayfa |
| `/qr/` | QR kod görüntüleme ve indirme |
| `/admin/` | Yönetim paneli |

---

## 📦 Teknolojiler

- **Django 4.2** — Web framework
- **SQLite** — Veritabanı
- **Bootstrap 5** — UI
- **Pillow** — Görsel işleme
- **qrcode** — QR kod üretimi
- **whitenoise** — Statik dosya servisi
- **python-decouple** — Ortam değişkenleri

---

## 🖼️ QR Kod Sistemi

QR kod `/qr/` sayfasında üretilir ve `MENU_URL` değişkenine yönlendirir. Bu değişkeni sabit tuttuğunuz sürece QR baskılı materyallerinizi değiştirmenize gerek kalmaz; içerik tamamen admin panelinden güncellenir.

---

## 📝 Admin Panel Kullanımı

1. `/admin/` adresine gidin
2. **Kategoriler** → Yeni kategori ekle, sırasını ve ikonunu belirle
3. **Ürünler** → Kategori seçin, fiyat ve açıklama girin, görsel yükleyin
4. **Aktif/Pasif** → `is_available` kutusunu işaretleyin/kaldırın
5. **Çok Satan** → `is_featured` kutusunu işaretleyin
6. Liste görünümünde sıra ve durum alanları doğrudan düzenlenebilir

---

*Lezzetle kodlandı 🔥*
