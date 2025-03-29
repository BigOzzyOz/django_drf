from django.urls import path
from . import views

urlpatterns = [
    path("", views.markets_view, name="home"),
    path("<int:pk>/", views.market_detail_view, name="market_detail"),
]
