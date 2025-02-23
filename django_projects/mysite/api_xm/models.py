# api_xm/models.py

from django.db import models
from django.utils import timezone

class XMRequest(models.Model):
    endpoint = models.CharField(max_length=50)
    metric_id = models.CharField(max_length=50)
    entity = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    filters = models.JSONField(null=True, blank=True)  # En caso de tener múltiples filtros
    created_at = models.DateTimeField(auto_now_add=True)

    # Si quieres guardar la respuesta:
    response_data = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.metric_id} - {self.entity} | {self.endpoint} ({self.start_date} to {self.end_date})"
