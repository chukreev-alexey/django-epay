# -*- coding: utf-8 -*-
from django.conf import settings

# обязательные параметры - реквизиты магазина
SHOP_ID = getattr(settings, 'EPAY_UBRR_SHOP_ID', 0)
LOGIN = getattr(settings, 'EPAY_UBRR_LOGIN', '')
PASSWORD = getattr(settings, 'EPAY_UBRR_PASSWORD', '')

# url, по которому будет идти отправка форм
FORM_TARGET = u'https://gate1.ubrd.ru/estore_listener.php'
URL_RESULT  = u'http://poisk.geograftur.ru/epay_ubrr/result/'
URL_OK      = u'http://poisk.geograftur.ru/epay_ubrr/success/'
URL_NO      = u'http://poisk.geograftur.ru/epay_ubrr/fail/'
