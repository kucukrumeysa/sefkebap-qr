#!/bin/bash
# ============================================================
# Şef Kebab — Otomatik Kurulum Scripti
# Kullanım: bash setup.sh
# ============================================================

set -e

GREEN='\033[0;32m'
GOLD='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GOLD}"
echo "  ╔══════════════════════════════════╗"
echo "  ║   ŞEF KEBAB — Kurulum Başlıyor  ║"
echo "  ╚══════════════════════════════════╝"
echo -e "${NC}"

# 1. Virtual environment
echo -e "${GREEN}[1/7] Sanal ortam oluşturuluyor...${NC}"
python3 -m venv venv
source venv/bin/activate

# 2. Dependencies
echo -e "${GREEN}[2/7] Bağımlılıklar yükleniyor...${NC}"
pip install --upgrade pip -q
pip install -r requirements.txt -q

# 3. .env dosyası
echo -e "${GREEN}[3/7] .env dosyası oluşturuluyor...${NC}"
if [ ! -f .env ]; then
    cp .env.example .env
    # Rastgele SECRET_KEY üret
    SECRET=$(python3 -c "import secrets; print(secrets.token_urlsafe(50))")
    sed -i "s/your-secret-key-here/$SECRET/" .env
    echo "  → .env oluşturuldu (SECRET_KEY otomatik üretildi)"
else
    echo "  → .env zaten mevcut, atlanıyor"
fi

# 4. Migrate
echo -e "${GREEN}[4/7] Veritabanı oluşturuluyor...${NC}"
python manage.py migrate --run-syncdb -v 0

# 5. Fixture
echo -e "${GREEN}[5/7] Örnek veriler yükleniyor...${NC}"
python manage.py loaddata apps/menu/fixtures/initial_data.json

# 6. Static files
echo -e "${GREEN}[6/7] Statik dosyalar toplanıyor...${NC}"
python manage.py collectstatic --noinput -v 0

# 7. Superuser
echo -e "${GREEN}[7/7] Admin kullanıcısı oluşturuluyor...${NC}"
echo -e "${GOLD}Kullanıcı adı ve şifre belirleyin:${NC}"
python manage.py createsuperuser --username admin --email admin@sefkebab.com || true

echo ""
echo -e "${GOLD}╔══════════════════════════════════════════════╗${NC}"
echo -e "${GOLD}║        KURULUM TAMAMLANDI! 🎉                ║${NC}"
echo -e "${GOLD}╠══════════════════════════════════════════════╣${NC}"
echo -e "${GOLD}║  Sunucuyu başlatmak için:                    ║${NC}"
echo -e "${GOLD}║    source venv/bin/activate                  ║${NC}"
echo -e "${GOLD}║    python manage.py runserver                ║${NC}"
echo -e "${GOLD}╠══════════════════════════════════════════════╣${NC}"
echo -e "${GOLD}║  Sayfalar:                                   ║${NC}"
echo -e "${GOLD}║    Ana Sayfa  →  http://127.0.0.1:8000/      ║${NC}"
echo -e "${GOLD}║    Menü       →  http://127.0.0.1:8000/menu/ ║${NC}"
echo -e "${GOLD}║    QR Kod     →  http://127.0.0.1:8000/qr/   ║${NC}"
echo -e "${GOLD}║    Admin      →  http://127.0.0.1:8000/admin/║${NC}"
echo -e "${GOLD}╚══════════════════════════════════════════════╝${NC}"
echo ""
echo -e "  💡 Logo eklemek için: ${GREEN}static/images/logo.png${NC} konumuna koyun"
echo ""
