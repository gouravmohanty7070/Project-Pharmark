from django.db import models

# Create your models here.
class Country(models.Model):
    country_name = models.CharField(max_length=100, default="india")

    def __str__(self) -> str:
        return str(self.country_name)