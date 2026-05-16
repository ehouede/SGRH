from django.db import models
from django.contrib.auth.models import User

class Employe(models.Model):
    ROLE_CHOICES = (
        ('ADMIN', 'Super Administrateur'),
        ('RH', 'Administrateur RH'),
        ('MANAGER', 'Manager / Chef d\'équipe'),
        ('EMPLOYE', 'Employé'),
        ('CANDIDAT', 'Candidat'),
        ('AUDITEUR', 'Auditeur Externe'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='EMPLOYE')
    manager = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subordonnes')
    matricule = models.CharField(max_length=20, unique=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField(null=True, blank=True)
    adresse = models.TextField(null=True, blank=True)
    telephone = models.CharField(max_length=20, null=True, blank=True)
    date_embauche = models.DateField()
    poste = models.CharField(max_length=100)
    service = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)

    def __str__(self):
        return f"{self.prenom} {self.nom} ({self.matricule})"

class Contrat(models.Model):
    TYPE_CONTRAT = (
        ('CDI', 'Contrat à Durée Indéterminée'),
        ('CDD', 'Contrat à Durée Déterminée'),
        ('STAGE', 'Stage'),
        ('PRESTATAIRE', 'Prestataire'),
    )
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='contrats')
    type_contrat = models.CharField(max_length=20, choices=TYPE_CONTRAT)
    date_debut = models.DateField()
    date_fin = models.DateField(null=True, blank=True)
    salaire_de_base = models.DecimalField(max_digits=12, decimal_places=2)
    est_actif = models.BooleanField(default=True)

    def __str__(self):
        return f"Contrat {self.type_contrat} - {self.employe.nom}"

class Evaluation(models.Model):
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='evaluations')
    date_evaluation = models.DateField()
    note = models.IntegerField()  # Sur 20 par exemple
    commentaires = models.TextField()

    def __str__(self):
        return f"Évaluation {self.date_evaluation} - {self.employe.nom}"

class Formation(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField()
    date_debut = models.DateField()
    date_fin = models.DateField()
    employes = models.ManyToManyField(Employe, related_name='formations')

    def __str__(self):
        return self.titre

class DocumentRH(models.Model):
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='documents')
    titre = models.CharField(max_length=100)
    fichier = models.FileField(upload_to='documents/')
    date_upload = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titre} - {self.employe.nom}"

class Notification(models.Model):
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='notifications')
    titre = models.CharField(max_length=200)
    message = models.TextField()
    est_lu = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titre} - {self.employe.nom}"

class NoteDeFrais(models.Model):
    STATUT_CHOICES = (
        ('EN_ATTENTE', 'En attente'),
        ('APPROUVE', 'Approuvé'),
        ('REJETE', 'Rejeté'),
        ('REMBOURSE', 'Remboursé'),
    )
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='notes_frais')
    titre = models.CharField(max_length=200)
    montant = models.DecimalField(max_digits=12, decimal_places=2)
    justificatif = models.FileField(upload_to='frais/', null=True, blank=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='EN_ATTENTE')
    date_creation = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.titre} - {self.employe.nom}"

class Pointage(models.Model):
    STATUT_CHOICES = (
        ('PRESENT', 'Présent'),
        ('RETARD', 'En retard'),
        ('ABSENT', 'Absent'),
    )
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='pointages')
    date = models.DateField(auto_now_add=True)
    heure_arrivee = models.TimeField(null=True, blank=True)
    heure_depart = models.TimeField(null=True, blank=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='PRESENT')

    def __str__(self):
        return f"Pointage {self.date} - {self.employe.nom}"

class Objectif(models.Model):
    STATUT_CHOICES = (
        ('A_FAIRE', 'À faire'),
        ('EN_COURS', 'En cours'),
        ('TERMINE', 'Terminé'),
        ('ANNULE', 'Annulé'),
    )
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='objectifs')
    titre = models.CharField(max_length=200)
    description = models.TextField()
    date_limite = models.DateField()
    progression = models.IntegerField(default=0) # 0 à 100
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='EN_COURS')

    def __str__(self):
        return f"{self.titre} - {self.employe.nom}"
