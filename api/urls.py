from django.urls import path
from .views import (payments)

urlpatterns = [
    path('pay',payments.processPayment),
]