"""payments URL Configuration"""
from django.urls import path
from django.conf.urls import url
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from pays.views import PaymentsView, PaymentView


schema_view = get_schema_view(openapi.Info(title="Payments API", default_version='v1'))


urlpatterns = [
    url(r"^swagger(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0)),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0)),
    path('api/v0/payments/', PaymentsView.as_view()),
    path('api/v0/payment/<uuid:pk>/', PaymentView.as_view()),
]
