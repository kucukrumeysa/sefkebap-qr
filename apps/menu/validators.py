import os
from django.core.exceptions import ValidationError

def validate_product_image(image):
    # 1. Dosya Boyutu Kontrolü (Maksimum 5MB)
    max_size = 5 * 1024 * 1024  # 5 Megabayt
    if image.size > max_size:
        raise ValidationError("Yüklenecek görsel boyutu en fazla 5 MB olabilir.")

    # 2. Dosya Uzantısı Kontrolü
    ext = os.path.splitext(image.name)[1].lower()
    valid_extensions = ['.jpg', '.jpeg', '.png', '.webp']
    if ext not in valid_extensions:
        raise ValidationError("Sadece JPG, JPEG, PNG ve WEBP formatları desteklenmektedir.")
