from django.urls import path
from . import views

urlpatterns = [
    path("markets/", views.MarketView.as_view(), name="home"),
    path("markets/<int:pk>/", views.MarketDetailView.as_view(), name="market_detail"),
    path("sellers/", views.SellerView.as_view(), name="sellers"),
    path("sellers/<int:pk>/", views.SellerDetailView.as_view(), name="seller_detail"),
    path("products/", views.ProductView.as_view(), name="products"),
    path("products/<int:pk>/", views.ProductDetailView.as_view(), name="product_detail"),
]
