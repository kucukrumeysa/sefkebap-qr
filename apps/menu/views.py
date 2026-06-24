from django.shortcuts import render, redirect
from django.conf import settings
from .models import Category, Product
import io
import base64
import qrcode

# Unsplash kaynaklı ücretsiz yemek görselleri (ürün adı → URL)
PRODUCT_IMAGE_MAP = {
    # Izgaralar
    "Ali Nazik":               "https://images.unsplash.com/photo-1599487488170-d11ec9c172f0?w=600&q=80",
    "Külbastı":                "https://images.unsplash.com/photo-1529042410759-befb1204b468?w=600&q=80",
    "Lokum Kebap":             "https://images.unsplash.com/photo-1544025162-d76694265947?w=600&q=80",
    "Ciğer":                   "https://images.unsplash.com/photo-1603360946369-dc9bb6258143?w=600&q=80",
    "Tavuk Kelebek":           "https://images.unsplash.com/photo-1598515214211-89d3c73ae83b?w=600&q=80",
    "Tavuk Kanat":             "https://images.unsplash.com/photo-1527477396000-e27163b481c2?w=600&q=80",
    "İkiyüzlü Adana Kebap":   "https://images.unsplash.com/photo-1633237308525-cd587cf71926?w=600&q=80",
    "Sıcak Ezme Üstü Kebap":  "https://images.unsplash.com/photo-1599487488170-d11ec9c172f0?w=600&q=80",
    "Kuzu Kaburga":            "https://images.unsplash.com/photo-1558030006-450675393462?w=600&q=80",
    "Kazbaşı":                 "https://images.unsplash.com/photo-1544025162-d76694265947?w=600&q=80",
    "Kuşbaşı":                 "https://images.unsplash.com/photo-1603360946369-dc9bb6258143?w=600&q=80",
    "Patlıcan Kebap":          "https://images.unsplash.com/photo-1529042410759-befb1204b468?w=600&q=80",
    "Beyti":                   "https://images.unsplash.com/photo-1633237308525-cd587cf71926?w=600&q=80",
    "Tavuk Şiş":               "https://images.unsplash.com/photo-1598515214211-89d3c73ae83b?w=600&q=80",
    "Kemikli Tavuk Şiş":      "https://images.unsplash.com/photo-1527477396000-e27163b481c2?w=600&q=80",
    "Adana Kebap":             "https://images.unsplash.com/photo-1599487488170-d11ec9c172f0?w=600&q=80",
    "Karışık Kebap":           "https://images.unsplash.com/photo-1544025162-d76694265947?w=600&q=80",
    # Dürümler
    "Adana Dürüm":             "https://images.unsplash.com/photo-1626700051175-6818013e1d4f?w=600&q=80",
    "Tavuk Şiş Dürüm":        "https://images.unsplash.com/photo-1626700051175-6818013e1d4f?w=600&q=80",
    # İkramlar
    "Salata":                  "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=600&q=80",
    "Soğan Salatası":          "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=600&q=80",
    "Acılı Ezme":              "https://images.unsplash.com/photo-1608897013039-887f21d8c804?w=600&q=80",
    "Haydari":                 "https://images.unsplash.com/photo-1488477181946-6428a0291777?w=600&q=80",
    "Humus":                   "https://images.unsplash.com/photo-1637949385162-e416fb15b2ce?w=600&q=80",
    "Patlıcan Ezmesi":         "https://images.unsplash.com/photo-1541518763669-27fef04b14ea?w=600&q=80",
    "Közlenmiş Mantar":        "https://images.unsplash.com/photo-1504545102780-26774c1bb073?w=600&q=80",
    "Közlenmiş Biber":         "https://images.unsplash.com/photo-1506806732259-39c2d0268443?w=600&q=80",
    "Yeşillik Tabağı":         "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=600&q=80",
    # İçecekler
    "Coca-Cola":               "https://images.unsplash.com/photo-1554866585-cd94860890b7?w=600&q=80",
    "Coca-Cola Zero":          "https://images.unsplash.com/photo-1554866585-cd94860890b7?w=600&q=80",
    "Coca-Cola Şişe":          "https://images.unsplash.com/photo-1554866585-cd94860890b7?w=600&q=80",
    "Fanta":                   "https://images.unsplash.com/photo-1603048719539-9ecb4aa395e3?w=600&q=80",
    "Sprite":                  "https://images.unsplash.com/photo-1625772299848-391b6a87d7b3?w=600&q=80",
    "Soda":                    "https://images.unsplash.com/photo-1625772299848-391b6a87d7b3?w=600&q=80",
    "Fusetea Şeftali":         "https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=600&q=80",
    "Fusetea Limonlu":         "https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=600&q=80",
    "Cappy Kayısı":            "https://images.unsplash.com/photo-1600271886742-f049cd451bba?w=600&q=80",
    "Cappy Vişne":             "https://images.unsplash.com/photo-1600271886742-f049cd451bba?w=600&q=80",
    "Cappy Şeftali":           "https://images.unsplash.com/photo-1600271886742-f049cd451bba?w=600&q=80",
    "Su":                      "https://images.unsplash.com/photo-1548839140-29a749e1cf4d?w=600&q=80",
    "Kapalı Ayran":            "https://images.unsplash.com/photo-1488477181946-6428a0291777?w=600&q=80",
    "Açık Ayran":              "https://images.unsplash.com/photo-1488477181946-6428a0291777?w=600&q=80",
    "Şalgam":                  "https://images.unsplash.com/photo-1603048719539-9ecb4aa395e3?w=600&q=80",
}


def home(request):
    return redirect('menu')


def menu(request):
    categories = Category.objects.prefetch_related(
        'subcategories',
        'products__subcategory',
        'subcategories__products',
    ).all()

    # Popüler ürünler — sadece bu 8 ürün, bu sırayla
    popular_names = [
        'Adana Kebap', 'Kuşbaşı', 'Ciğer', 'Tavuk Kanat',
        'Tavuk Şiş', 'Kuzu Kaburga', 'Adana Dürüm', 'Tavuk Şiş Dürüm'
    ]
    all_featured = Product.objects.filter(
        name__in=popular_names, is_available=True
    ).select_related('category')
    # İsim listesinin sırasını koru
    featured_map = {p.name: p for p in all_featured}
    featured_products = [featured_map[name] for name in popular_names if name in featured_map]

    context = {
        'categories': categories,
        'featured_products': featured_products,
        'product_images': PRODUCT_IMAGE_MAP,
    }
    return render(request, 'menu/menu.html', context)


def qr_view(request):
    menu_url = getattr(settings, 'MENU_URL', request.build_absolute_uri('/menu/'))

    qr = qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(menu_url)
    qr.make(fit=True)

    img = qr.make_image(fill_color='#2C2C2C', back_color='#FAF7F2')

    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    qr_b64 = base64.b64encode(buffer.getvalue()).decode()

    context = {
        'qr_image': qr_b64,
        'menu_url': menu_url,
    }
    return render(request, 'menu/qr.html', context)
