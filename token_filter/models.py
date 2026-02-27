from django.db import models

class SolanaToken(models.Model):
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=50)
    address = models.CharField(max_length=255, unique=True)
    
    # Core Parameters
    market_cap = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    liquidity = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    twitter = models.URLField(max_length=500, null=True, blank=True)
    website = models.URLField(max_length=500, null=True, blank=True)
    volume_24h = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    age_seconds = models.PositiveIntegerField(default=0)
    holders_count = models.PositiveIntegerField(default=0)
    
    # Optional Parameters
    dev_hold_percent = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    top_10_percent = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    bundle_percent = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    sniper_percent = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    pro_holders_count = models.PositiveIntegerField(default=0)
    
    is_passing_filter = models.BooleanField(default=False)
    is_notified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.symbol}) - {self.address}"
