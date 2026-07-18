"""
Şef Kebap — Fixture Export Scripti
===================================
Kullanım:
  python export_fixture.py

Bu script, lokal SQLite veritabanındaki menü verilerini
apps/menu/fixtures/initial_data.json dosyasına aktarır.

Akış:
  1. Lokalde admin panelden ürün ekle/sil/güncelle
  2. Bu scripti çalıştır → fixture güncellenir
  3. git add + commit + push → Vercel canlı siteyi günceller
"""

import os
import sys
import json
import django

# Django ortamını hazırla
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# DATABASE_URL'yi kaldır ki SQLite kullanılsın
if 'DATABASE_URL' in os.environ:
    del os.environ['DATABASE_URL']

# .env'den DATABASE_URL okunmasını engelle — doğrudan SQLite kullan
os.environ['DATABASE_URL'] = ''

sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from apps.menu.models import Category, SubCategory, Product
from django.core.serializers import serialize


def export_fixture():
    """Veritabanındaki tüm menü verilerini fixture olarak kaydet."""
    
    fixture_path = os.path.join('apps', 'menu', 'fixtures', 'initial_data.json')
    
    # Tüm modelleri topla
    categories = Category.objects.all().order_by('order', 'pk')
    subcategories = SubCategory.objects.all().order_by('order', 'pk')
    products = Product.objects.all().order_by('category__order', 'order', 'pk')
    
    print(f"\n📊 Mevcut Veriler:")
    print(f"   Kategoriler  : {categories.count()}")
    print(f"   Alt Kategoriler: {subcategories.count()}")
    print(f"   Ürünler      : {products.count()}")
    
    # JSON serialize et
    data = []
    
    for obj_list in [categories, subcategories, products]:
        serialized = json.loads(serialize('json', obj_list))
        data.extend(serialized)
    
    # Dosyaya yaz
    with open(fixture_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Fixture başarıyla güncellendi!")
    print(f"   📁 {fixture_path}")
    print(f"   📦 Toplam {len(data)} kayıt")
    print(f"\n💡 Sonraki adım:")
    print(f"   git add .")
    print(f"   git commit -m \"Menü güncellendi\"")
    print(f"   git push")


if __name__ == '__main__':
    export_fixture()
