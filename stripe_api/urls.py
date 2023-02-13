from django.urls import path
from .views import ItemView, ItemsView, get_key, create_checkout_session, test_view, success_view

urlpatterns = [
    path('', ItemsView.as_view()), # убрать
    path('item/<int:pk>', ItemView.as_view()),
    path('get_key', get_key),
    path('buy/<int:pk>', create_checkout_session),
    path('test', test_view), # убрать
    path('successed', success_view),
]
