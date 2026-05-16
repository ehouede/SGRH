from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BulletinPaieViewSet, RubriquePaieViewSet

router = DefaultRouter()
router.register(r'bulletins', BulletinPaieViewSet)
router.register(r'rubriques', RubriquePaieViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
