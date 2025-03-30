from django.urls import path
from . import views

urlpatterns = [
    path("markets/", views.markets_view, name="home"),
    path("markets/<int:pk>/", views.market_detail_view, name="market_detail"),
    path("sellers/", views.sellers_view, name="sellers"),
    path("sellers/<int:pk>/", views.seller_detail_view, name="seller_detail"),
    path("products/", views.products_view, name="products"),
    path("products/<int:pk>/", views.product_detail_view, name="product_detail"),
]
