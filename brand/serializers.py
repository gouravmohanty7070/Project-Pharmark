from rest_framework import serializers
from .models import Suggestions


class SuggestionsSerializers(serializers.ModelSerializer):
   class Meta:
       model = Suggestions
       fields = ('drugCode', 'Approved', 'suggestionString' , 'names' , 'country_name', 'createdAt','inputType','inputTypePreference')

class CreateSuggestionsSerializers(serializers.ModelSerializer):
   class Meta:
       model = Suggestions
       fields = ('drugCode', 'suggestionString' , 'country_name','inputType','inputTypePreference')
 
   
    
