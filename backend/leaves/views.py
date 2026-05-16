from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import TypeConge, DemandeConge, SoldeConge
from .serializers import TypeCongeSerializer, DemandeCongeSerializer
from datetime import datetime

class TypeCongeViewSet(viewsets.ModelViewSet):
    queryset = TypeConge.objects.all()
    serializer_class = TypeCongeSerializer

class DemandeCongeViewSet(viewsets.ModelViewSet):
    queryset = DemandeConge.objects.all()
    serializer_class = DemandeCongeSerializer

    def create(self, request, *args, **kwargs):
        employe_id = request.data.get('employe')
        type_conge_id = request.data.get('type_conge')
        date_debut = datetime.strptime(request.data.get('date_debut'), '%Y-%m-%d').date()
        date_fin = datetime.strptime(request.data.get('date_fin'), '%Y-%m-%d').date()
        
        # Calcul du nombre de jours (simplifié)
        nb_jours = (date_fin - date_debut).days + 1
        
        # Vérification du solde
        try:
            solde = SoldeConge.objects.get(employe_id=employe_id, type_conge_id=type_conge_id, annee=date_debut.year)
            if solde.solde_restant < nb_jours:
                return Response({"error": f"Solde insuffisant. Disponible: {solde.solde_restant} jours."}, status=status.HTTP_400_BAD_REQUEST)
            
            # Décrémenter le solde
            solde.nb_jours_pris += nb_jours
            solde.save()
            
            return super().create(request, *args, **kwargs)
        except SoldeConge.DoesNotExist:
            return Response({"error": "Aucun solde de congés paramétré pour cet employé pour cette année."}, status=status.HTTP_400_BAD_REQUEST)
