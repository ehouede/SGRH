from django.db import models
from core_hr.models import Employe

class TypeConge(models.Model):
    libelle = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    nb_jours_max = models.IntegerField(default=30)

    def __str__(self):
        return self.libelle

class DemandeConge(models.Model):
    STATUT_CHOICES = (
        ('BROUILLON', 'Brouillon'),
        ('EN_ATTENTE', 'En attente'),
        ('APPROUVE', 'Approuvé'),
        ('REJETE', 'Rejeté'),
    )
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='demandes_conge')
    type_conge = models.ForeignKey(TypeConge, on_delete=models.PROTECT)
    date_debut = models.DateField()
    date_fin = models.DateField()
    motif = models.TextField(null=True, blank=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='EN_ATTENTE')
    date_demande = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Demande {self.type_conge.libelle} - {self.employe.nom}"

class SoldeConge(models.Model):
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='soldes_conge')
    type_conge = models.ForeignKey(TypeConge, on_delete=models.CASCADE)
    annee = models.IntegerField()
    nb_jours_total = models.DecimalField(max_digits=5, decimal_places=1, default=30.0)
    nb_jours_pris = models.DecimalField(max_digits=5, decimal_places=1, default=0.0)

    @property
    def solde_restant(self):
        return self.nb_jours_total - self.nb_jours_pris

    def __str__(self):
        return f"Solde {self.type_conge.code} - {self.employe.nom} ({self.annee})"
