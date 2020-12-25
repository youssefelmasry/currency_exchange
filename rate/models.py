from django.db import models

class Rate(models.Model):
    """A model represinting Currency Exchange Rates on a specific day"""

    from_currency = models.CharField(max_length=3)
    to_currency = models.CharField(max_length=3)
    date = models.DateField()
    rate = models.FloatField()

    def __str__(self):
        """A unicode representation of Rate model"""
        return f"{self.pk}"
