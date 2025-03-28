from django.urls import path
from market_app.api.views import first_view

urlpatterns = [
    path("", first_view, name="home"),
]
