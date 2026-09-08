from django.db import models
from django.utils import timezone
import uuid

# Create your models here.

from account.models import Customer

class Project(models.Model):
    """Réprésente un projet ou le site web tracké (lié au data-site-id)"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='projects')

    site_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Session(models.Model):
    """Regroupe l'historique d'un visiteur unique"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    session_id = models.UUIDField(default=uuid.uuid4)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)

    # Django pourra calculer la durée de session en comparant
    # le premier et le dernier événement associé à cette session.
    started_at = models.DateTimeField(auto_now_add=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Event(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # --- Données issues du payload TypeScript ---
    site_id = models.CharField(max_length=100, db_index=True)
    session_id = models.CharField(max_length=100, db_index=True)
    event_type = models.CharField(max_length=50)
    url = models.URLField(max_length=1000)

    # On stocke le timestamp exact généré par le navigateur (le new Date().toISOString())
    client_timestamp = models.DateTimeField()

    # --- Données dynamiques ([key: string]: unknown) ---
    # Le JSONField est parfait pour stocker les variables aléatoires comme
    # 'tag', 'id', 'className' ou 'formId' sans devoir modifier la base de données à chaque fois.
    properties = models.JSONField(default=dict, blank=True)

    # --- Données capturées par le backend (Django) ---
    # Comme discuté, l'IP est récupérée par le serveur, pas par le front-end
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    # Optionnel : L'heure exacte à laquelle ton serveur a reçu la requête
    server_timestamp = models.DateTimeField(auto_now_add=True)

    # Optionnel : Le User-Agent pour savoir si l'utilisateur est sur Mobile/Desktop, Chrome/Safari...
    user_agent = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.event_type} - {self.session_id} à {self.client_timestamp}"

    class Meta:
        ordering = ['-client_timestamp'] # Les plus récents en premier
