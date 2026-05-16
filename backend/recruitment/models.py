from django.db import models

class OffreEmploi(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField()
    date_publication = models.DateField(auto_now_add=True)
    est_active = models.BooleanField(default=True)

    def __str__(self):
        return self.titre

class Candidat(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(max_length=250, unique=True)
    telephone = models.CharField(max_length=20, null=True, blank=True)
    cv = models.FileField(upload_to='cvs/', null=True, blank=True)

    def __str__(self):
        return f"{self.prenom} {self.nom}"

class Candidature(models.Model):
    STATUT_CHOICES = (
        ('NOUVEAU', 'Nouveau'),
        ('ENTRETIEN', 'Entretien'),
        ('OFFRE', 'Offre'),
        ('REJETE', 'Rejeté'),
        ('EMBAUCHE', 'Embauché'),
    )
    offre = models.ForeignKey(OffreEmploi, on_delete=models.CASCADE, related_name='candidatures')
    candidat = models.ForeignKey(Candidat, on_delete=models.CASCADE, related_name='candidatures')
    date_postulation = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='NOUVEAU')
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Candidature de {self.candidat.nom} pour {self.offre.titre}"
