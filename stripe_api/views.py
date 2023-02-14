from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView
from .models import Item, Order, Discount, Tax
import stripe
import json


class ItemView(DetailView):
    """View class for every single item"""
    template_name = 'item_page.html'
    model = Item
    context_object_name = 'item_info'


# ------ Session Checkout Views ------
class HomePageView(ListView):
    """View class for main page with list of items"""
    template_name = 'home_page.html'
    model = Item
    context_object_name = 'item_info'


@csrf_exempt
def get_key(request):
    """View for publish key requesting"""
    if request.method == 'GET':
        stripe_publish_key = {'stripePublishableKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_publish_key, safe=False)


@csrf_exempt
def create_checkout_session(request, pk):
    """View for creating new checkout session"""
    if request.method == 'POST':
        main_url = f'http://{request.get_host()}/'

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
                    'unit_amount': round(item.price) * 100,
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
    """View for success page and creating new order"""
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


# ------ Payment Intent Views ------
class ItemPaymentIntentView(ListView):
    """Class view for item with payment intent"""
    template_name = 'payment_intent_item.html'
    model = Item
    context_object_name = 'item_info'


class PaymentIntentView(ListView):
    """Class view for payment intent feature"""
    template_name = 'payment_intent.html'
    model = Item
    context_object_name = 'item_info'


def get_currency_and_price(quantity: str) -> list:
    """Function to get price and currency for payment intent item"""
    item = Item.objects.get(pk=3)
    currency = item.currency
    price = round(item.price)
    total_price = price * int(quantity)
    info = [total_price, currency]
    return info


@csrf_exempt
def create_payment_intent(request):
    """View for creating payment intent"""
    if request.method == 'POST':

        try:
            stripe.api_key = settings.STRIPE_SECRET_KEY
            data: dict = json.loads(request.body)

            quantity: str = data['quantity']
            info: list = get_currency_and_price(quantity)

            intent: dict = stripe.PaymentIntent.create(
                amount=info[0],
                currency=info[1],
            )

            return JsonResponse({
                'clientSecret': intent['client_secret']
            })
        except Exception:
            return JsonResponse({'error': str(Exception)})


def success_intent_view(request):
    """View for success page for payment intent feature"""
    quantity = request.GET.get('quantity')
    item = Item.objects.get(pk=3)
    Order.objects.create(order=item, quantity=quantity, price=item.price, currency=item.currency)
    data = {
        'name': item.name,
        'price': item.price,
        'quantity': quantity,
        'currency': item.currency,
    }
    return render(request, 'success_page.html', context=data)
