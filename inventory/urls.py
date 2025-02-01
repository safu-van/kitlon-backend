from django.urls import path

from .views import InventoryView, StockIncreaseView

urlpatterns = [
    path("inventory/", InventoryView.as_view()),
    path("inventory/<int:pk>/", InventoryView.as_view()),
    path("inventory/<int:pk>/increment-stock/", StockIncreaseView.as_view()),
]
