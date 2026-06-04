from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Kategori Adı')),
                ('slug', models.SlugField(blank=True, max_length=100, unique=True, verbose_name='Slug')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Sıra')),
                ('icon', models.CharField(blank=True, max_length=50, verbose_name='İkon (emoji)')),
                ('description', models.CharField(blank=True, max_length=255, verbose_name='Açıklama')),
            ],
            options={
                'verbose_name': 'Kategori',
                'verbose_name_plural': 'Kategoriler',
                'ordering': ['order', 'name'],
            },
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Alt Kategori Adı')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Sıra')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='menu.category', verbose_name='Kategori')),
            ],
            options={
                'verbose_name': 'Alt Kategori',
                'verbose_name_plural': 'Alt Kategoriler',
                'ordering': ['order', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Ürün Adı')),
                ('description', models.TextField(blank=True, verbose_name='Açıklama')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Fiyat (₺)')),
                ('image', models.ImageField(blank=True, null=True, upload_to='products/', verbose_name='Görsel')),
                ('is_available', models.BooleanField(default=True, verbose_name='Mevcut mu?')),
                ('is_featured', models.BooleanField(default=False, verbose_name='Çok Satan?')),
                ('portion_info', models.CharField(blank=True, max_length=100, verbose_name='Porsiyon Bilgisi')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Sıra')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Eklenme Tarihi')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='menu.category', verbose_name='Kategori')),
                ('subcategory', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='menu.subcategory', verbose_name='Alt Kategori')),
            ],
            options={
                'verbose_name': 'Ürün',
                'verbose_name_plural': 'Ürünler',
                'ordering': ['order', 'name'],
            },
        ),
    ]
