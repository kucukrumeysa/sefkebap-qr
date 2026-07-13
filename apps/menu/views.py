from django.shortcuts import render, redirect
from django.conf import settings
from .models import Category, Product
import io
import os
import base64
import qrcode
from PIL import Image

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

    img = qr.make_image(fill_color='#2C2C2C', back_color='#FAF7F2').convert('RGB')

    # Logoyu ortaya yerleştir
    logo_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'logo.webp')
    if os.path.exists(logo_path):
        logo = Image.open(logo_path).convert('RGBA')

        qr_width, qr_height = img.size
        # Logo, QR kodun ~%22'sini kaplasın (okunabilirlik için güvenli oran)
        logo_max_size = int(qr_width * 0.22)
        logo.thumbnail((logo_max_size, logo_max_size), Image.LANCZOS)

        # Logonun etrafına QR arka plan renginde bir kutu ekle (kontrast için),
        # kutu boyutu logonun GERÇEK en/boy oranına göre hesaplanır
        padding = int(logo_max_size * 0.12)
        box_w = logo.size[0] + padding * 2
        box_h = logo.size[1] + padding * 2
        box = Image.new('RGBA', (box_w, box_h), '#FAF7F2')
        # Logo, kutunun tam ortasına yapıştırılır
        logo_pos = ((box_w - logo.size[0]) // 2, (box_h - logo.size[1]) // 2)
        box.paste(logo, logo_pos, logo)

        pos = ((qr_width - box_w) // 2, (qr_height - box_h) // 2)
        img.paste(box, pos, box)

    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    qr_b64 = base64.b64encode(buffer.getvalue()).decode()

    context = {
        'qr_image': qr_b64,
        'menu_url': menu_url,
    }
    return render(request, 'menu/qr.html', context)