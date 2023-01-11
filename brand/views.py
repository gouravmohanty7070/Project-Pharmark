from django.shortcuts import render
from .models import Country , Suggestions
from .serializers import SuggestionsSerializers , CreateSuggestionsSerializers
from rest_framework import viewsets
from rest_framework import generics , status
from rest_framework.views import APIView
from rest_framework.response import Response
from .utils import generate_new_names, med_count , check_phonetically_sound , check_phonetically_sound , check_fuzzy_wuzzy , check_sound_similarity
from lstm_model import return_model
# Create your views here.

class SuggestionViewSet(viewsets.ModelViewSet):
   queryset = Suggestions.objects.all()
   serializer_class = SuggestionsSerializers

class SuggestionView(generics.ListAPIView):
    queryset= Suggestions.objects.all()
    serializer_class = SuggestionsSerializers


class CreateSuggestionView(APIView):
    
    serializer_class = CreateSuggestionsSerializers

    def post(self,request,format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        
        serializer =  self.serializer_class(data=request.data)
        print(request.data)
        if serializer.is_valid():
            country_name=serializer.data.get('country_name')
            drugCode=serializer.data.get('drugCode')
            suggestionString=serializer.data.get('suggestionString')
            inputType=serializer.data.get('inputType')
            inputTypePreference=serializer.data.get('inputTypePreference')
            listOfString = suggestionString.split(",")
            # return_model(inputTypePreference,country=country_name)
            print(listOfString)
            final_list_as_a_str = []
            for prefix in listOfString:
                print(prefix)
                temp_list = generate_new_names(prefix=prefix)
                temp_list=check_phonetically_sound(temp_list)

                print(temp_list)
                for word in temp_list:
                    if len(word)<3:
                        temp_list.remove(word)
                temp_list = check_fuzzy_wuzzy(temp_list)
                temp_list = check_phonetically_sound(temp_list)
                temp_list = check_sound_similarity(temp_list)
                # temp_list = med_count(temp_list)
                final_list = temp_list
                temp_final_list_as_a_str = ",".join(final_list)
                final_list_as_a_str.append(temp_final_list_as_a_str)
            final_list_as_a_str = ",".join(final_list_as_a_str)

            
            
            suggestion=Suggestions(country_name=country_name,names=temp_final_list_as_a_str,drugCode=drugCode,suggestionString=suggestionString,inputType=inputType,inputTypePreference=inputTypePreference)
            try:
                suggestion.save()
                print(SuggestionsSerializers(suggestion).data)
                return Response(SuggestionsSerializers(suggestion).data,status=status.HTTP_200_OK)
            except:
                print("Error occured")
                raise Exception
        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)



def homepage(request):
    return render(request, 'home.html')

def predictFormPage(request):
    context = {
        'countries': Country.objects.all(),
    }
    return render(request, 'predictForm.html', context=context)

def predict(request):
    if request.method == 'POST':
        print(request.POST)
        country_name = request.POST['countries']
        names_dict = {}
        if request.POST['input_type'] == 'List of Strings':
            params = request.POST['text_input'].split(',')
            for p in params:
                temp_list = generate_new_names(p)
            # final_list = med_count(temp_list)
                names_dict[p] = temp_list
            print(names_dict)
        elif request.POST['input_type'] == 'Therapeutic Name':
            pass
        elif request.POST['input_type'] == 'Molecular Name':
            pass
        context = {
            'names': names_dict,
        }
        return render(request, 'predictPage.html', context=context)
    else:
        context = {
            'countries': Country.objects.all(),
        }
        return render(request, 'predictForm.html', context=context)