from django.urls import path

from .views import SkuView, SkuSalesView, SkuSubmissionView, SkuSubmissionExcelView

urlpatterns = [
    path("", SkuView.as_view()),
    path("<int:pk>/", SkuView.as_view()),
    path("sku-sales/", SkuSalesView.as_view()),
    path("sku-submission/", SkuSubmissionView.as_view()),
    path("update-status/<int:pk>/<str:status>/", SkuSubmissionView.as_view()),
    path("sku-submission-excel/", SkuSubmissionExcelView.as_view()),
]
