from django.urls import path
from .views import SubmitDataView
from rest_framework.routers import DefaultRouter
from .views import PerevalViewSet, SubmitDataDetailView

router = DefaultRouter()
router.register(r'pereval_list', PerevalViewSet, basename='pereval_list')


urlpatterns = [
    path("submitData/", SubmitDataView.as_view(), name="submit_data"),
    path("pereval_list/<int:id>/", SubmitDataDetailView.as_view(), name="submit_data_detail"),
]

urlpatterns += router.urls