from .views import CatalogView, ProductDetailView, home, artists
from django.urls import path

app_name = "main"

urlpatterns = [
    path('', home, name='home'),
    path('artists/', artists, name='artists'),
    path('services/', CatalogView.as_view(), name='catalog'),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
]
