from rest_framework import serializers
from .models import BulletinPaie, DetailBulletin, RubriquePaie

class RubriquePaieSerializer(serializers.ModelSerializer):
    class Meta:
        model = RubriquePaie
        fields = '__all__'

class DetailBulletinSerializer(serializers.ModelSerializer):
    rubrique_libelle = serializers.ReadOnlyField(source='rubrique.libelle')
    
    class Meta:
        model = DetailBulletin
        fields = ['rubrique', 'rubrique_libelle', 'base', 'part_salariale', 'part_patronale']

class BulletinPaieSerializer(serializers.ModelSerializer):
    details = DetailBulletinSerializer(many=True, read_only=True)
    employe_nom = serializers.ReadOnlyField(source='employe.nom')
    employe_prenom = serializers.ReadOnlyField(source='employe.prenom')

    class Meta:
        model = BulletinPaie
        fields = ['id', 'employe', 'employe_nom', 'employe_prenom', 'periode', 'salaire_brut', 'salaire_net', 'details']
