from django.shortcuts import render, redirect
from django.conf import settings
from .models import Category, Product
import io
import base64
import qrcode

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
