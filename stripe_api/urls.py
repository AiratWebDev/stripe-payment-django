from django.urls import path
from .views import ItemView, HomePageView, get_key, create_checkout_session, success_view, \
    ItemPaymentIntentView, create_payment_intent, success_intent_view, PaymentIntentView

urlpatterns = [
    path('', HomePageView.as_view()),

    # ------ Session Checkout Urls ------
    path('item/<int:pk>', ItemView.as_view()),
    path('buy/<int:pk>', create_checkout_session),
    path('get_key', get_key),
    path('successed', success_view),
    path('successed-intent', success_intent_view),

    # ------ Payment Intent Urls ------
    path('payment-intent', PaymentIntentView.as_view()),
    path('payment-intent-item', ItemPaymentIntentView.as_view()),
    path('create-payment-intent', create_payment_intent),
]
