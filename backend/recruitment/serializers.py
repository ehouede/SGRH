from rest_framework import serializers
from .models import OffreEmploi, Candidat, Candidature

class OffreEmploiSerializer(serializers.ModelSerializer):
    class Meta:
        model = OffreEmploi
        fields = '__all__'

class CandidatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidat
        fields = '__all__'

class CandidatureSerializer(serializers.ModelSerializer):
    candidat_nom = serializers.ReadOnlyField(source='candidat.nom')
    candidat_prenom = serializers.ReadOnlyField(source='candidat.prenom')
    offre_titre = serializers.ReadOnlyField(source='offre.titre')

    class Meta:
        model = Candidature
        fields = ['id', 'offre', 'offre_titre', 'candidat', 'candidat_nom', 'candidat_prenom', 'date_postulation', 'statut', 'notes']
