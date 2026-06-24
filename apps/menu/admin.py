from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import Category, SubCategory, Product


class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 0
    fields = ['name', 'order']


class ProductInline(admin.TabularInline):
    model = Product
    extra = 0
    fields = ['name', 'price', 'portion_info', 'is_available', 'is_featured', 'order']
    show_change_link = True


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'order', 'product_count', 'slug']
    list_editable = ['order', 'icon']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [SubCategoryInline, ProductInline]
    search_fields = ['name']

    def product_count(self, obj):
        count = obj.products.count()
        active = obj.products.filter(is_available=True).count()
        return format_html('<span style="color:green">{}</span> / {}', active, count)
    product_count.short_description = 'Aktif / Toplam Ürün'


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'order']
    list_editable = ['order']
    list_filter = ['category']
    search_fields = ['name', 'category__name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'image_thumbnail', 'name', 'category', 'subcategory',
        'formatted_price_display', 'portion_info',
        'is_available', 'is_featured', 'order',
    ]
    list_display_links = ['image_thumbnail', 'name']
    list_editable = ['is_available', 'is_featured', 'order']
    list_filter = ['category', 'subcategory', 'is_available', 'is_featured']
    search_fields = ['name', 'description', 'category__name']
    readonly_fields = ['image_preview_panel', 'created_at']
    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('category', 'subcategory', 'name', 'description', 'price', 'portion_info')
        }),
        ('Görsel Yönetimi', {
            'fields': ('image_preview_panel', 'image'),
            'description': 'Görsel yüklemek için "Görsel" alanını kullanın. Mevcut görseli silmek için "Temizle" kutucuğunu işaretleyin.'
        }),
        ('Durum & Sıralama', {
            'fields': ('is_available', 'is_featured', 'order')
        }),
        ('Sistem Bilgisi', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    # ── Liste görünümü küçük thumbnail ──
    def image_thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:54px;height:54px;object-fit:cover;'
                'border-radius:8px;box-shadow:0 1px 4px rgba(0,0,0,0.15);" />',
                obj.image.url
            )
        return format_html(
            '<div style="width:54px;height:54px;border-radius:8px;background:#f5f0e8;'
            'display:flex;align-items:center;justify-content:center;'
            'font-size:22px;color:#ccc;">📷</div>'
        )
    image_thumbnail.short_description = '📷'

    # ── Detay sayfası büyük önizleme + işlem butonları ──
    def image_preview_panel(self, obj):
        if obj.image:
            return format_html(
                '''
                <div style="margin-bottom:12px;">
                    <img src="{url}"
                         style="max-width:320px;max-height:220px;object-fit:cover;
                                border-radius:10px;box-shadow:0 2px 12px rgba(0,0,0,0.15);
                                display:block;margin-bottom:10px;" />
                    <p style="font-size:12px;color:#888;margin:0;">
                        ✅ Görsel yüklü. Değiştirmek için aşağıdan yeni görsel seçin.
                        Silmek için <strong>"Temizle"</strong> kutucuğunu işaretleyip kaydedin.
                    </p>
                </div>
                ''',
                url=obj.image.url
            )
        return format_html(
            '<div style="padding:16px;background:#fafafa;border:2px dashed #ddd;'
            'border-radius:10px;text-align:center;color:#999;font-size:13px;">'
            '📷 Henüz görsel yüklenmedi.<br>'
            '<span style="font-size:12px;">Aşağıdaki "Görsel" alanından yükleyebilirsiniz.</span>'
            '</div>'
        )
    image_preview_panel.short_description = 'Mevcut Görsel'

    def formatted_price_display(self, obj):
        if obj.price == 0:
            return format_html('<span style="color:#aaa;font-size:11px;">İkram</span>')
        return format_html('<strong style="color:#C5A880;">₺{}</strong>', f'{obj.price:.0f}')
    formatted_price_display.short_description = 'Fiyat'
    formatted_price_display.admin_order_field = 'price'
