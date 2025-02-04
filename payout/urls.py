from django.urls import path

from .views import WalletView, WalletTransactionExcelView

urlpatterns = [
    path("wallets/", WalletView.as_view()),
    path("wallet/<int:pk>/deduct/", WalletView.as_view()),
    path("transactions-excel/", WalletTransactionExcelView.as_view()),
]
