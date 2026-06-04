from django.contrib import admin
from django.utils.html import format_html
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
        'image_preview', 'name', 'category', 'subcategory',
        'formatted_price_display', 'portion_info',
        'is_available', 'is_featured', 'order', 'created_at'
    ]
    list_display_links = ['image_preview', 'name']
    list_editable = ['is_available', 'is_featured', 'order']
    list_filter = ['category', 'subcategory', 'is_available', 'is_featured']
    search_fields = ['name', 'description', 'category__name']
    readonly_fields = ['image_preview_large', 'created_at']
    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('category', 'subcategory', 'name', 'description', 'price', 'portion_info')
        }),
        ('Görsel', {
            'fields': ('image', 'image_preview_large')
        }),
        ('Durum', {
            'fields': ('is_available', 'is_featured', 'order')
        }),
        ('Sistem', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:50px;height:50px;object-fit:cover;border-radius:6px;" />',
                obj.image.url
            )
        return format_html('<span style="color:#aaa;">{}</span>', '—')
    image_preview.short_description = 'Görsel'

    def image_preview_large(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width:300px;max-height:200px;object-fit:cover;border-radius:8px;" />',
                obj.image.url
            )
        return '—'
    image_preview_large.short_description = 'Görsel Önizleme'

    def formatted_price_display(self, obj):
        return format_html('<strong>₺{}</strong>', f'{obj.price:.0f}')
    formatted_price_display.short_description = 'Fiyat'
    formatted_price_display.admin_order_field = 'price'
