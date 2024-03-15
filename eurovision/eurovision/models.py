from django.db import models

class Country(models.Model):
    code = models.CharField(max_length=2, primary_key=True)
    country_name = models.CharField(max_length=100)

    def __str__ (self):
        return self.country_name
    
    class Meta:
        verbose_name_plural = "Countries"
