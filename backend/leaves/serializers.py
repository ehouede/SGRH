from rest_framework import serializers
from .models import TypeConge, DemandeConge

class TypeCongeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeConge
        fields = '__all__'

class DemandeCongeSerializer(serializers.ModelSerializer):
    employe_nom = serializers.ReadOnlyField(source='employe.nom')
    type_conge_libelle = serializers.ReadOnlyField(source='type_conge.libelle')

    class Meta:
        model = DemandeConge
        fields = ['id', 'employe', 'employe_nom', 'type_conge', 'type_conge_libelle', 'date_debut', 'date_fin', 'motif', 'statut', 'date_demande']
