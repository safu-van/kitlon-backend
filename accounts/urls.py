from django.urls import path

from .views import LoginView, LabourView, LabourBlockUnblockView

urlpatterns = [
    path("login/", LoginView.as_view()),
    path("labour/", LabourView.as_view()),
    path("labour/<int:pk>/", LabourView.as_view()),
    path("labour/<int:pk>/block-unblock/", LabourBlockUnblockView.as_view()),
]
