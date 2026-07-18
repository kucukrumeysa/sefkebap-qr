"""
Sef Kebap - Mevcut Gorselleri Cloudinary'ye Yukle (media/ prefix ile)
"""

import os
import sys
import codecs

if sys.platform == 'win32':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, errors='replace')

import cloudinary
import cloudinary.uploader
from decouple import config

cloudinary.config(
    cloud_name=config('CLOUDINARY_CLOUD_NAME'),
    api_key=config('CLOUDINARY_API_KEY'),
    api_secret=config('CLOUDINARY_API_SECRET'),
    secure=True
)

MEDIA_DIR = os.path.join(os.path.dirname(__file__), 'media', 'products')
VALID_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp'}


def upload_all_images():
    if not os.path.exists(MEDIA_DIR):
        print("HATA: media/products/ klasoru bulunamadi!")
        return

    files = [f for f in os.listdir(MEDIA_DIR)
             if os.path.splitext(f)[1].lower() in VALID_EXTENSIONS]

    print(f"\n{len(files)} gorsel bulundu: media/products/")
    print("=" * 50)

    success = 0
    errors = 0

    for i, filename in enumerate(sorted(files), 1):
        filepath = os.path.join(MEDIA_DIR, filename)
        name_without_ext = os.path.splitext(filename)[0]
        # django-cloudinary-storage "media/" prefix ekliyor
        # bu yuzden public_id'yi media/products/... olarak ayarliyoruz
        public_id = f"media/products/{name_without_ext}"

        try:
            result = cloudinary.uploader.upload(
                filepath,
                public_id=public_id,
                overwrite=True,
                resource_type="image"
            )
            url = result.get('secure_url', '')
            print(f"  OK [{i}/{len(files)}] {filename}")
            print(f"     -> {url}")
            success += 1
        except Exception as e:
            print(f"  HATA [{i}/{len(files)}] {filename} - {e}")
            errors += 1

    print("\n" + "=" * 50)
    print(f"Sonuc: {success} basarili, {errors} hatali")

    if errors == 0:
        print("Tum gorseller basariyla yuklendi!")
    else:
        print("Bazi gorseller yuklenemedi, yukardaki hatalari kontrol et.")


if __name__ == '__main__':
    upload_all_images()
