# -*- coding: utf-8 -*-

from hashlib import md5
from urllib import urlencode

from django import forms

from .conf import SHOP_ID, LOGIN, PASSWORD, FORM_TARGET, URL_OK, URL_NO
from .models import SuccessNotification

class BaseEpayForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.target = FORM_TARGET # Используется только дял формы переадресации на сервис оплаты
        super(EpayForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget = forms.HiddenInput()
        self.fields['sign'].initial = self.get_sign()

class EpayForm(BaseEpayForm):
    """Форма для переправки посетителя на страницу сервиса оплаты
    """
    shop_id = forms.IntegerField(initial=SHOP_ID)
    login = forms.CharField(max_length=30, initial=LOGIN)
    pswd = forms.CharField(max_length=30, initial=PASSWORD)
    order_id = forms.CharField(max_length=128)
    pay_sum = forms.FloatField(min_value=0.01)
    url_ok = forms.CharField(max_length=255, initial=URL_OK)
    url_no = forms.CharField(max_length=255, initial=URL_NO)
    sign = forms.CharField(max_length=255)

    def __init__(self, *args, **kwargs):
        self.target = FORM_TARGET
        super(EpayForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget = forms.HiddenInput()
        self.fields['sign'].initial = self.get_sign()

    def get_sign(self):
        """ uppercase(md5(
                md5(SHOP_ID) + & + md5(LOGIN) + & + md5(PSWD) + & + md5(ORDER_ID) + & + md5(PAY_SUM)
            ))
        """
        _val = lambda val: md5(val).hexdigest()
        value = '&'.join([
            _val(str(SHOP_ID)), _val(LOGIN), _val(PASSWORD),
            _val(str(self.fields['order_id'].initial)),
            _val(str(round(self.fields['pay_sum'].initial, 2)))
        ])
        return _val(value).upper()

class EpayResultForm(BaseEpayForm):
    """Форма для приема результатов и проверки контрольной суммы"""
    STATE_CHOICES = (
        ('authorized', u'средства успешно заблокированы'),
        ('paid', u'оплачен'),
        ('canceled', u'отменен')
    )
    shop_id = forms.IntegerField(initial=SHOP_ID)
    order_id = forms.CharField(max_length=128)
    order_idp = forms.CharField(max_length=255)
    state = forms.ChoiceField(max_length=20, choices=STATE_CHOICES)
    sign = forms.CharField(max_length=255)

    def get_sign(self):
        """ uppercase(md5(md5(SHOP_ID) + & + md5(ORDER_ID) + & + md5(STATE)))
        """
        _val = lambda val: md5(val).hexdigest()
        value = '&'.join([
            _val(str(SHOP_ID)),
            _val(str(self.cleaned_data['order_id'].initial)),
            _val(self.cleaned_data['state'].initial)
        ])
        return _val(value).upper()

    def clean(self):
        sign = self.cleaned_data['sign'].upper()
        if sign != self.get_sign():
            raise forms.ValidationError(u'Ошибка в контрольной сумме')
        return self.cleaned_data

class EpayRedirectForm(forms.Form):
    """Форма обработки возвращения посетителя на страницу магазина после
    успешной или неуспешной оплаты
    """
    order_id = forms.CharField(max_length=128)
    order_idp = forms.CharField(max_length=255)