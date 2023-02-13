from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView
from .models import Item, Order, Discount, Tax
import stripe
import json


class ItemView(DetailView):
    template_name = 'item_page.html'
    model = Item
    context_object_name = 'item_info'


class ItemsView(ListView):
    template_name = 'items_page.html'
    model = Item
    context_object_name = 'item_info'


@csrf_exempt
def get_key(request):
    if request.method == 'GET':
        stripe_publish_key = {'stripePublishableKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_publish_key, safe=False)


@csrf_exempt
def create_checkout_session(request, pk):
    if request.method == 'POST':
        main_url = 'http://127.0.0.1:8000/'

        stripe.api_key = settings.STRIPE_SECRET_KEY

        item = Item.objects.get(pk=pk)
        quantity: str = json.loads(request.body)['quantity']

        tax_info: dict = stripe.TaxRate.create(
            display_name="NDS",
            inclusive=False,
            percentage=item.tax.tax_size,
        )

        if item.discount.size != 0:
            discount_info: dict = stripe.Coupon.create(percent_off=item.discount.size, duration="once")
        else:
            discount_info: dict = stripe.Coupon.create(percent_off=0.01, duration="once")

        session = stripe.checkout.Session.create(
            line_items=[{
                'price_data': {
                    'currency': item.currency,
                    'product_data': {
                        'name': item.name,
                    },
                    'unit_amount': round(item.price)*100,
                },
                'quantity': quantity if quantity != '0' else '1',
                'tax_rates': [tax_info['id']],
            }],
            discounts=[{
                'coupon': discount_info['id'],
            }],
            mode='payment',
            success_url=main_url + 'successed?session_id={CHECKOUT_SESSION_ID}' + f'&pk={pk}' + f'&quantity={quantity}',
            cancel_url=main_url + f'item/{pk}',
        )
        return JsonResponse({'sessionId': session['id']})


def success_view(request):
    session_id = request.GET.get('session_id')
    pk = request.GET.get('pk')
    quantity = request.GET.get('quantity')
    if session_id and pk:
        item = Item.objects.get(pk=pk)
        Order.objects.create(order=item, quantity=quantity, price=item.price)
        data = {
            'name': item.name,
            'price': item.price,
            'quantity': quantity,
            'currency': item.currency,
        }
        return render(request, 'success_page.html', context=data)
    else:
        raise Exception('Нет параметров')


def test_view(request):
    obj = Item.objects.get(pk=2)
    return JsonResponse({'name': obj.name, 'price': str(obj.price)[:-3]})