# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('epay_ubrr.views',
    url(r'^result/$', 'result_view', name='epay_ubrr_result'),
    url(r'^(?P<oper>success|fail)/$', 'redirect_view', name='epay_ubrr_redirect'),
)
