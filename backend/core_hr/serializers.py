from rest_framework import serializers
from .models import Employe, Contrat, Pointage, Objectif

class ContratSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contrat
        fields = '__all__'

class PointageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pointage
        fields = '__all__'

class ObjectifSerializer(serializers.ModelSerializer):
    class Meta:
        model = Objectif
        fields = '__all__'

class EmployeSerializer(serializers.ModelSerializer):
    contrats = ContratSerializer(many=True, read_only=True)
    
    class Meta:
        model = Employe
        fields = ['id', 'user', 'matricule', 'nom', 'prenom', 'date_naissance', 'adresse', 'telephone', 'date_embauche', 'poste', 'service', 'role', 'photo', 'contrats']
