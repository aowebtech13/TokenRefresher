from django.db import models

class TokenRefreshLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField()
    message = models.TextField(blank=True)
    status_code = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.timestamp} - {'Success' if self.success else 'Failure'}"
