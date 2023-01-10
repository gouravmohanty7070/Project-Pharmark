from rest_framework import serializers
from .models import Suggestions


class SuggestionsSerializers(serializers.ModelSerializer):
   class Meta:
       model = Suggestions
       fields = ('drugCode', 'Approved', 'suggestionString' , 'names' , 'country_name', 'createdAt')

class CreateSuggestionsSerializers(serializers.ModelSerializer):
   class Meta:
       model = Suggestions
       fields = ('drugCode', 'suggestionString' , 'country_name')
 
   
    
