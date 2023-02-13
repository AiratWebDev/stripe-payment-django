from django.urls import path
from .views import ItemView, ItemsView, get_key, create_checkout_session, success_view

urlpatterns = [
    path('', ItemsView.as_view()),
    path('item/<int:pk>', ItemView.as_view()),
    path('get_key', get_key),
    path('buy/<int:pk>', create_checkout_session),
    path('successed', success_view),
]
