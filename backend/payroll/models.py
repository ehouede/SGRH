from django.db import models
from core_hr.models import Employe

class RubriquePaie(models.Model):
    TYPE_RUBRIQUE = (
        ('GAIN', 'Gain / Prime'),
        ('RETENUE', 'Retenue / Cotisation'),
    )
    code = models.CharField(max_length=20, unique=True)
    libelle = models.CharField(max_length=100)
    type_rubrique = models.CharField(max_length=10, choices=TYPE_RUBRIQUE)
    taux_salarial = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    taux_patronal = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    est_fixe = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.code} - {self.libelle}"

class BulletinPaie(models.Model):
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE)
    periode = models.DateField()  # Premier jour du mois
    date_generation = models.DateTimeField(auto_now_add=True)
    salaire_brut = models.DecimalField(max_digits=12, decimal_places=2)
    salaire_net = models.DecimalField(max_digits=12, decimal_places=2)
    pdf_file = models.FileField(upload_to='bulletins/', null=True, blank=True)

    def __str__(self):
        return f"Bulletin {self.periode.strftime('%m/%Y')} - {self.employe.nom}"

class DetailBulletin(models.Model):
    bulletin = models.ForeignKey(BulletinPaie, on_delete=models.CASCADE, related_name='details')
    rubrique = models.ForeignKey(RubriquePaie, on_delete=models.SET_NULL, null=True)
    base = models.DecimalField(max_digits=12, decimal_places=2)
    part_salariale = models.DecimalField(max_digits=12, decimal_places=2)
    part_patronale = models.DecimalField(max_digits=12, decimal_places=2)
