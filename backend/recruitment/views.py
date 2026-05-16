from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import OffreEmploi, Candidat, Candidature
from .serializers import OffreEmploiSerializer, CandidatSerializer, CandidatureSerializer

class OffreEmploiViewSet(viewsets.ModelViewSet):
    queryset = OffreEmploi.objects.all()
    serializer_class = OffreEmploiSerializer

class PublicOffreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OffreEmploi.objects.filter(est_active=True)
    serializer_class = OffreEmploiSerializer
    permission_classes = [AllowAny]

class CandidatViewSet(viewsets.ModelViewSet):
    queryset = Candidat.objects.all()
    serializer_class = CandidatSerializer

class CandidatureViewSet(viewsets.ModelViewSet):
    queryset = Candidature.objects.all()
    serializer_class = CandidatureSerializer
