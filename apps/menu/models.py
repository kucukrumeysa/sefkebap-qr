from django.db import models
from django.utils.text import slugify
from .validators import validate_product_image


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Kategori Adı')
    slug = models.SlugField(max_length=100, unique=True, blank=True, verbose_name='Slug')
    order = models.PositiveIntegerField(default=0, verbose_name='Sıra')
    icon = models.CharField(max_length=50, blank=True, verbose_name='İkon (emoji)')
    description = models.CharField(max_length=255, blank=True, verbose_name='Açıklama')

    class Meta:
        verbose_name = 'Kategori'
        verbose_name_plural = 'Kategoriler'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def active_products(self):
        return self.products.filter(is_available=True)


class SubCategory(models.Model):
    """Alt başlık — özellikle İçecekler gibi kategoriler için"""
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories', verbose_name='Kategori')
    name = models.CharField(max_length=100, verbose_name='Alt Kategori Adı')
    order = models.PositiveIntegerField(default=0, verbose_name='Sıra')

    class Meta:
        verbose_name = 'Alt Kategori'
        verbose_name_plural = 'Alt Kategoriler'
        ordering = ['order', 'name']

    def __str__(self):
        return f'{self.category.name} → {self.name}'

    def active_products(self):
        return self.products.filter(is_available=True)


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='Kategori')
    subcategory = models.ForeignKey(
        SubCategory, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='products', verbose_name='Alt Kategori'
    )
    name = models.CharField(max_length=200, verbose_name='Ürün Adı')
    description = models.TextField(blank=True, verbose_name='Açıklama')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Fiyat (₺)')
    image = models.ImageField(
        upload_to='products/', blank=True, null=True,
        verbose_name='Görsel', validators=[validate_product_image]
    )
    is_available = models.BooleanField(default=True, verbose_name='Mevcut mu?')
    is_featured = models.BooleanField(default=False, verbose_name='Çok Satan?')
    portion_info = models.CharField(max_length=100, blank=True, verbose_name='Porsiyon Bilgisi')
    order = models.PositiveIntegerField(default=0, verbose_name='Sıra')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Eklenme Tarihi')

    class Meta:
        verbose_name = 'Ürün'
        verbose_name_plural = 'Ürünler'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    @property
    def formatted_price(self):
        return f'₺{self.price:.0f}'
