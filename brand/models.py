from django.db import models
import string 
import random


def generate_unique_code():
    length = 5

    while True:
        code = ''.join(random.choices(string.ascii_uppercase, k=length))
        if Suggestions.objects.filter(suggestionCode=code).count() == 0:
            break

    return code
# Create your models here.
class Country(models.Model):
    country_name = models.CharField(max_length=100, default="india")

    def __str__(self) -> str:
        return str(self.country_name)

class Suggestions(models.Model):
    suggestionCode=models.CharField(max_length=5,default=generate_unique_code,unique=True)
    drugCode=models.CharField(max_length=5,default="",unique=True)
    Approved=models.BooleanField(default=False)
    createdAt=models.DateTimeField(auto_now_add=True)
    suggestionString=models.CharField(max_length=100,default="")
    names = models.TextField(null=True)
    inputType=models.TextField(default="listOfString",null=False)
    inputTypePreference=models.TextField(default="listOfStringMolecular",null=False)
    country_name = models.CharField(max_length=100, default="india")
    def __str__(self) -> str:
        return str(self.country_name)
    