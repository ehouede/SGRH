import os
import django
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from core_hr.models import Employe, NoteDeFrais, Objectif, Pointage, Contrat
from payroll.models import RubriquePaie, BulletinPaie
from recruitment.models import OffreEmploi, Candidature
from leaves.models import TypeConge, SoldeConge, DemandeConge

def seed():
    print("Nettoyage complet de la base de donnees...")
    # Suppression des donnees existantes
    User.objects.all().delete()
    Employe.objects.all().delete()
    Contrat.objects.all().delete()
    DemandeConge.objects.all().delete()
    BulletinPaie.objects.all().delete()
    RubriquePaie.objects.all().delete()
    from recruitment.models import OffreEmploi, Candidature, Candidat
    Candidature.objects.all().delete()
    Candidat.objects.all().delete()
    OffreEmploi.objects.all().delete()
    NoteDeFrais.objects.all().delete()
    Objectif.objects.all().delete()
    Pointage.objects.all().delete()

    print("Creation des rubriques de paie (OHADA)...")
    RubriquePaie.objects.update_or_create(code='BASE', defaults={'libelle': 'Salaire de Base', 'type_rubrique': 'GAIN'})
    RubriquePaie.objects.update_or_create(code='CNSS', defaults={'libelle': 'CNSS', 'type_rubrique': 'RETENUE', 'taux_salarial': 6.3})
    RubriquePaie.objects.update_or_create(code='TRANSP', defaults={'libelle': 'Indemnite Transport', 'type_rubrique': 'GAIN'})

    print("Creation des types de conges...")
    TypeConge.objects.update_or_create(code='ANN', defaults={'libelle': 'Conge Annuel', 'nb_jours_max': 30})
    TypeConge.objects.update_or_create(code='MAL', defaults={'libelle': 'Maladie', 'nb_jours_max': 15})

    print("Creation des utilisateurs et roles...")
    roles = [
        ('admin', 'ADMIN', 'PDG'),
        ('rh', 'RH', 'Directeur RH'),
        ('manager', 'MANAGER', 'Chef de Projet'),
        ('employe', 'EMPLOYE', 'Developpeur'),
        ('auditeur', 'AUDITEUR', 'Auditeur Externe'),
        ('candidat', 'CANDIDAT', 'Candidat Externe'),
    ]

    employes_crees = []
    for username, role, poste in roles:
        user = User.objects.create_user(username=username, password=f"{username}123", email=f"{username}@sgrh.com")
        emp = Employe.objects.create(
            user=user,
            matricule=f"MAT-{username.upper()}",
            nom=username.upper(),
            prenom="Demo",
            role=role,
            poste=poste,
            service="Direction" if role == 'ADMIN' else "IT",
            date_embauche=date.today()
        )
        employes_crees.append(emp)
        print(f"User cree: {username} (Role: {role})")

        # Creation d'un contrat pour les employes internes
        if role != 'CANDIDAT' and role != 'AUDITEUR':
            Contrat.objects.create(
                employe=emp,
                type_contrat='CDI',
                salaire_de_base=500000 if role == 'ADMIN' else 250000,
                date_debut=date.today() - timedelta(days=365)
            )
            
            # Pointages (le champ date est auto_now_add, donc on cree juste pour aujourd'hui)
            Pointage.objects.create(employe=emp, heure_arrivee="08:00", heure_depart="17:00", statut='PRESENT')
            Pointage.objects.create(employe=emp, heure_arrivee="08:30", heure_depart="17:30", statut='RETARD')

            # Objectifs
            Objectif.objects.create(employe=emp, titre="Finaliser module Paie", date_limite=date.today() + timedelta(days=7), progression=80)
            Objectif.objects.create(employe=emp, titre="Optimiser Performance", date_limite=date.today() + timedelta(days=14), progression=30)

    # Simulation de conges
    print("Creation des demandes de conges...")
    type_ann = TypeConge.objects.get(code='ANN')
    DemandeConge.objects.create(
        employe=employes_crees[3], # L'employe
        type_conge=type_ann,
        date_debut=date.today() + timedelta(days=10),
        date_fin=date.today() + timedelta(days=15),
        motif="Vacances annuelles",
        statut='EN_ATTENTE'
    )

    # Recrutement
    print("Creation des offres et candidatures...")
    offre = OffreEmploi.objects.create(
        titre="Developpeur Fullstack React/Django",
        description="Nous recherchons un developpeur talentueux..."
    )
    
    from recruitment.models import Candidat
    cand = Candidat.objects.create(
        nom="SOW",
        prenom="Ibrahima",
        email="ibrahima.sow@email.com",
        telephone="771234567"
    )
    
    Candidature.objects.create(
        offre=offre,
        candidat=cand,
        statut="NOUVEAU"
    )

    print("Base de donnees prete pour la soutenance !")

if __name__ == "__main__":
    seed()
