from django.urls import path, include
from rest_framework import routers

from payment.views import PaymentViewSet

router = routers.DefaultRouter()
router.register("", PaymentViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "payment"
