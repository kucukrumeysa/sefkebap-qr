from django.conf import settings
from datetime import datetime


def restaurant_info(request):
    now = datetime.now()
    current_time = now.strftime('%H:%M')
    open_time = getattr(settings, 'RESTAURANT_OPEN_TIME', '11:00')
    close_time = getattr(settings, 'RESTAURANT_CLOSE_TIME', '23:00')

    if close_time >= open_time:
        is_open = open_time <= current_time <= close_time
    else:
        is_open = current_time >= open_time or current_time <= close_time

    return {
        'RESTAURANT_NAME': getattr(settings, 'RESTAURANT_NAME', 'Şef Kebap'),
        'RESTAURANT_PHONE': getattr(settings, 'RESTAURANT_PHONE', ''),
        'RESTAURANT_ADDRESS': getattr(settings, 'RESTAURANT_ADDRESS', ''),
        'RESTAURANT_WHATSAPP': getattr(settings, 'RESTAURANT_WHATSAPP', ''),
        'RESTAURANT_MAPS_URL': getattr(settings, 'RESTAURANT_MAPS_URL', '#'),
        'RESTAURANT_OPEN_TIME': open_time,
        'RESTAURANT_CLOSE_TIME': close_time,
        'RESTAURANT_IS_OPEN': is_open,
    }
