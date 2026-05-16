from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.template.loader import render_to_string
from django.http import HttpResponse
from xhtml2pdf import pisa
import io
from datetime import date
from .models import BulletinPaie, DetailBulletin, RubriquePaie
from .serializers import BulletinPaieSerializer, RubriquePaieSerializer
from core_hr.models import Employe, Contrat
from decimal import Decimal

class BulletinPaieViewSet(viewsets.ModelViewSet):
    queryset = BulletinPaie.objects.all()
    serializer_class = BulletinPaieSerializer

    @action(detail=False, methods=['post'])
    def generer(self, request):
        employe_id = request.data.get('employe_id')
        periode = request.data.get('periode') # format 'YYYY-MM-DD'
        
        try:
            employe = Employe.objects.get(id=employe_id)
            contrat = employe.contrats.filter(est_actif=True).first()
            if not contrat:
                return Response({"error": "Aucun contrat actif trouvé pour cet employé."}, status=status.HTTP_400_BAD_REQUEST)
            
            salaire_base = contrat.salaire_de_base
            
            # 1. Calcul de l'ancienneté (en années)
            today = date.today()
            anciennete_ans = (today - employe.date_embauche).days // 365
            prime_anciennete = Decimal(0)
            if anciennete_ans >= 2:
                # 2% par an après 2 ans
                prime_anciennete = (salaire_base * Decimal(anciennete_ans * 0.02))

            # 2. Prime de transport (fixe)
            prime_transport = Decimal(30000)

            # Création du bulletin
            bulletin = BulletinPaie.objects.create(
                employe=employe,
                periode=periode,
                salaire_brut=salaire_base + prime_anciennete + prime_transport,
                salaire_net=0
            )

            # Ajouter les gains détaillés
            if prime_anciennete > 0:
                rub_anc, _ = RubriquePaie.objects.get_or_create(code='ANC', defaults={'libelle': 'Prime d\'ancienneté', 'type_rubrique': 'GAIN'})
                DetailBulletin.objects.create(bulletin=bulletin, rubrique=rub_anc, base=salaire_base, part_salariale=prime_anciennete, part_patronale=0)
            
            rub_trans, _ = RubriquePaie.objects.get_or_create(code='TRANS', defaults={'libelle': 'Indemnité de transport', 'type_rubrique': 'GAIN'})
            DetailBulletin.objects.create(bulletin=bulletin, rubrique=rub_trans, base=prime_transport, part_salariale=prime_transport, part_patronale=0)

            total_retenues = Decimal(0)
            # Retenues basées sur le brut imposable (simplifié)
            brut_imposable = salaire_base + prime_anciennete

            # Simulation de rubriques de cotisations (CNSS / IPRES)
            rubriques = RubriquePaie.objects.all()
            if not rubriques.exists():
                # Créer des rubriques par défaut si elles n'existent pas
                RubriquePaie.objects.create(code='CNSS', libelle='CNSS (Sécurité Sociale)', type_rubrique='RETENUE', taux_salarial=6.3, taux_patronal=12.0)
                RubriquePaie.objects.create(code='IPRES', libelle='IPRES (Retraite)', type_rubrique='RETENUE', taux_salarial=5.6, taux_patronal=8.4)
                rubriques = RubriquePaie.objects.all()

            for rub in rubriques:
                part_sal = (salaire_base * rub.taux_salarial) / 100
                part_pat = (salaire_base * rub.taux_patronal) / 100
                
                DetailBulletin.objects.create(
                    bulletin=bulletin,
                    rubrique=rub,
                    base=salaire_base,
                    part_salariale=part_sal,
                    part_patronale=part_pat
                )
                total_retenues += part_sal

            # Mise à jour du net
            bulletin.salaire_net = salaire_base - total_retenues
            bulletin.save()

            serializer = self.get_serializer(bulletin)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Employe.DoesNotExist:
            return Response({"error": "Employé non trouvé."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['get'])
    def telecharger_pdf(self, request, pk=None):
        bulletin = self.get_object()
        
        # Calculer les totaux pour le template
        details = bulletin.details.all()
        total_retenues = sum(d.part_salariale for d in details)
        total_patronal = sum(d.part_patronale for d in details)

        context = {
            'bulletin': bulletin,
            'total_retenues': total_retenues,
            'total_patronal': total_patronal,
        }
        
        html = render_to_string('payroll/bulletin_pdf.html', context)
        result = io.BytesIO()
        pdf = pisa.pisaDocument(io.BytesIO(html.encode("UTF-8")), result)
        
        if not pdf.err:
            response = HttpResponse(result.getvalue(), content_type='application/pdf')
            filename = f"Bulletin_{bulletin.employe.nom}_{bulletin.periode.strftime('%m_%Y')}.pdf"
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
        
        return Response({"error": "Erreur lors de la génération du PDF"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RubriquePaieViewSet(viewsets.ModelViewSet):
    queryset = RubriquePaie.objects.all()
    serializer_class = RubriquePaieSerializer
