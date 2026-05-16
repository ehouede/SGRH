from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TypeCongeViewSet, DemandeCongeViewSet

router = DefaultRouter()
router.register(r'types', TypeCongeViewSet)
router.register(r'demandes', DemandeCongeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
