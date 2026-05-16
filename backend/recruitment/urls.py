from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OffreEmploiViewSet, CandidatViewSet, CandidatureViewSet, PublicOffreViewSet

router = DefaultRouter()
router.register(r'offres', OffreEmploiViewSet)
router.register(r'public-offres', PublicOffreViewSet, basename='public-offres')
router.register(r'candidats', CandidatViewSet)
router.register(r'candidatures', CandidatureViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
