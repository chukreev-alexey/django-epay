# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from .forms import EpayForm, EpayResultForm, EpayRedirectForm
from .models import EpayState

def epay_form(request, order_id):
    # Нужно во вьюху передать id заказа, чтобы потом можно было бы отслеживать оплату

    order = Order.objects.get(pk=order_id) # Order реальная таблица с заказами, куда уже сохранена заявка
    form = EpayForm(initial={
        'pay_sum': order.pay_sum,
        'order_id': order.id,
    })
    # Создаем объект состяния платежа
    state = EpayState(order_id=order.id, pay_sum=order.pay_sum)
    state.save()
    return render(request, 'epay_form.html', {'form': form})

@csrf_exempt
def result_view(request):
    """ На этот адрес робот УБРиР уведомит о том что пришла оплата. Он может
        уведомить и несколько раз - надо это учесть. Эта вьюха не должна
        требовать авторизации, потому что робот УБРиР понятия никакого о нашей
        авторизации не имеет.
    """
    form = EpayResultForm(request.POST)
    if form.is_valid():
        state = EpayState.objects.get(pk=form.cleaned_data['order_id'])
        if state.state == 'created':
            state.state = 'confirmed'
            state.order_idp = form.cleaned_data['order_idp']
            state.save()
            """Далее здесь добавляем платеж в ФП
            """
        return HttpResponse('OK')
    return HttpResponse('error: bad signature') # Лучше вывести здесь form.errors, чтобы понимать какие ошибки

@login_required
@csrf_exempt
def redirect_view(request, oper):
    """ обработчик для Success и Fail """
    form = EpayRedirectForm(request.GET)
    if form.is_valid():
        state = EpayState.objects.get(pk=form.cleaned_data['order_id'])
        state.order_idp = form.cleaned_data['order_idp']
        state.state = oper
        """Дальше можно достать из state сумму и заявку и отобразить в шаблоне
        любые данные, которые хочется, заполняя пременную context
        """
        context = {}
        template = '%s.html' % oper
        return TemplateResponse(request, template, context)
    return TemplateResponse(request, 'form_error.html', {'form': form})
