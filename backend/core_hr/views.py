from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Sum
from django.template.loader import render_to_string
from django.http import HttpResponse
from xhtml2pdf import pisa
import io
from .models import Employe, Contrat, Pointage, Objectif
from .serializers import EmployeSerializer, ContratSerializer, PointageSerializer, ObjectifSerializer

class EmployeViewSet(viewsets.ModelViewSet):
    queryset = Employe.objects.all()
    serializer_class = EmployeSerializer

    @action(detail=False, methods=['get'])
    def stats(self, request):
        total_employes = Employe.objects.count()
        par_service = Employe.objects.values('service').annotate(count=Count('id'))
        
        # Masse salariale (basée sur les contrats actifs)
        masse_salariale = Contrat.objects.filter(est_actif=True).aggregate(total=Sum('salaire_de_base'))['total'] or 0
        
        return Response({
            'total_employes': total_employes,
            'par_service': par_service,
            'masse_salariale': masse_salariale
        })

    @action(detail=True, methods=['get'])
    def generer_contrat(self, request, pk=None):
        employe = self.get_object()
        contrat = employe.contrats.filter(est_actif=True).first()
        
        if not contrat:
            return Response({"error": "Aucun contrat actif trouvé."}, status=status.HTTP_400_BAD_REQUEST)
        
        context = {
            'employe': employe,
            'contrat': contrat,
        }
        
        html = render_to_string('core_hr/contrat_pdf.html', context)
        result = io.BytesIO()
        pisa.pisaDocument(io.BytesIO(html.encode("UTF-8")), result)
        
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        filename = f"Contrat_{employe.nom}.pdf"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response

    @action(detail=False, methods=['get'])
    def me(self, request):
        try:
            employe = request.user.profile
            serializer = self.get_serializer(employe)
            return Response(serializer.data)
        except AttributeError:
            return Response({"error": "Profil non trouvé"}, status=404)

class ContratViewSet(viewsets.ModelViewSet):
    queryset = Contrat.objects.all()
    serializer_class = ContratSerializer

class PointageViewSet(viewsets.ModelViewSet):
    queryset = Pointage.objects.all()
    serializer_class = PointageSerializer

class ObjectifViewSet(viewsets.ModelViewSet):
    queryset = Objectif.objects.all()
    serializer_class = ObjectifSerializer
