from django.urls import path
from . import views

urlpatterns=[
    path('place_order/',views.place_order, name='place_order'),
    path('payments/', views.payments, name='payments'),
    path('payments/<int:order_id>', views.paynow, name='paynow'),
    path('payments_order/', views.paymentorder),
]