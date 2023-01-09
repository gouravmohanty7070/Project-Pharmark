from rest_framework import serializers
from .models import Suggestions


class SuggestionsSerializers(serializers.ModelSerializer):
   class Meta:
       model = Suggestions
       fields = ('drugCode', 'Approved', 'names', 'listOfString' , 'country_name')
 
   
    
