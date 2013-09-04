# -*- coding: utf-8 -*-
import datetime

from django.db import models

class EpayState(models.Model):
    STATE_CHOICES = (
        ('created', u'Создано'),
        ('confirmed', u'Подтверждено'),
        ('success', u'Подтверждено и пользователь перешел на SuccessUrl'),
        ('fail', u'Ошибка от платежной системы'),
    )
    order_id = models.IntegerField(u'Номер заказа в ФП', db_index=True)
    order_idp = models.IntegerField(u'ИД в платежной системе', blank=True,
        null=True)
    state = models.CharField(u'Состояние', choices=STATE_CHOICES,
        default=STATE_CHOICES[0][0])
    pay_sum = models.DecimalField(u'Платеж', max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(u'Время создания уведомления',
        auto_now_add=True)
    confirmed_at = models.DateTimeField(u'Время получения успешного уведомления',
        blank=True, null=True)

    def save(self, *args, **kwargs):
        # Проставляем время подтверждения платежа
        if self.state =='confirmed':
            old_state = self.__class__.objects.get(id=self.id)
            if old_state.state == 'created':
                self.confirmed_at = datetime.datetime.now()
        super(EpayState, self).save(*args, **kwargs)


    def __unicode__(self):
        return u'#%d: %s' % (self.order_id, self.pay_sum)

    class Meta:
        verbose_name = u'Уведомление о платеже УБРиР'
        verbose_name_plural = u'Уведомления о платежах УБРиР'
