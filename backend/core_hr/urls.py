from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmployeViewSet, ContratViewSet, PointageViewSet, ObjectifViewSet

router = DefaultRouter()
router.register(r'employes', EmployeViewSet)
router.register(r'contrats', ContratViewSet)
router.register(r'pointages', PointageViewSet)
router.register(r'objectifs', ObjectifViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
