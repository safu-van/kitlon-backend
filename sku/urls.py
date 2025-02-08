from django.urls import path

from .views import SkuView, SkuSubmissionView, SkuSubmissionExcelView

urlpatterns = [
    path("", SkuView.as_view()),
    path("<int:pk>/", SkuView.as_view()),
    path("sku-submission/", SkuSubmissionView.as_view()),
    path("update-status/<int:pk>/<str:status>/", SkuSubmissionView.as_view()),
    path("sku-submission-excel/", SkuSubmissionExcelView.as_view()),
]
