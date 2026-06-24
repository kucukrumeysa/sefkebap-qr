import os
import sys
import django

# Add project path to sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.menu.models import Product

updates = {
    # Izgaralar
    "Ali Nazik": (700.00, "1,5 Porsiyon"),
    "Külbastı": (700.00, "1,5 Porsiyon"),
    "Lokum Kebap": (700.00, "180 gr"),
    "Ciğer": (450.00, "Standart"),
    "Tavuk Kelebek": (350.00, "Standart"),
    "Tavuk Kanat": (350.00, "Standart"),
    "İkiyüzlü Adana Kebap": (700.00, "1,5 Porsiyon"),
    "Sıcak Ezme Üstü Kebap": (700.00, "1,5 Porsiyon"),
    "Kuzu Kaburga": (450.00, "Standart"),
    "Kazbaşı": (700.00, "1,5 Porsiyon"),
    "Kuşbaşı": (700.00, "1,5 Porsiyon"),
    "Patlıcan Kebap": (700.00, "1,5 Porsiyon"),
    "Beyti": (700.00, "1,5 Porsiyon"),
    "Tavuk Şiş": (350.00, "Standart"),
    "Kemikli Tavuk Şiş": (350.00, "Standart"),
    "Adana Kebap": (350.00, "Standart"),
    "Karışık Kebap": (3500.00, "8 Porsiyon"),
    # İçecekler
    "Coca-Cola": (70.00, "Kutu"),
    "Coca-Cola Zero": (70.00, "Kutu"),
    "Coca-Cola Şişe": (70.00, "Şişe"),
    "Fanta": (70.00, "Kutu"),
    "Sprite": (70.00, "Kutu"),
    "Soda": (40.00, "Şişe"),
    "Fusetea Şeftali": (70.00, "Kutu"),
    "Fusetea Limonlu": (70.00, "Kutu"),
    "Cappy Kayısı": (70.00, "Kutu"),
    "Cappy Vişne": (70.00, "Kutu"),
    "Cappy Şeftali": (70.00, "Kutu"),
    "Su": (20.00, "Küçük Şişe"),
    "Kapalı Ayran": (50.00, "Kutu"),
    "Açık Ayran": (50.00, "Bardak"),
    "Şalgam": (50.00, "Şişe"),
}

print("Starting database price updates on Supabase...")
for name, (price, portion) in updates.items():
    products = Product.objects.filter(name__iexact=name)
    if products.exists():
        for product in products:
            product.price = price
            product.portion_info = portion
            product.save()
            print(f"Updated: {product.name} -> {price} TL, {portion}")
    else:
        print(f"WARNING: Product not found: {name}")
print("Database updates finished successfully!")
