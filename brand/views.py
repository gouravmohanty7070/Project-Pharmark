from django.shortcuts import render
from .models import Country , Suggestions
from .serializers import SuggestionsSerializers , CreateSuggestionsSerializers
from rest_framework import viewsets
from rest_framework import generics , status
from rest_framework.views import APIView
from rest_framework.response import Response
from .utils import generate_new_names, med_count , check_phonetically_sound

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
        if serializer.is_valid():
            country_name=serializer.data.get('country_name')
            drugCode=serializer.data.get('drugCode')
            suggestionString=serializer.data.get('suggestionString')
            listOfString = suggestionString.split(",")
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
                final_list = med_count(temp_list)
                temp_final_list_as_a_str = ",".join(final_list)
                final_list_as_a_str.append(temp_final_list_as_a_str)
            final_list_as_a_str = " . ".join(final_list_as_a_str)

            
            
            suggestion=Suggestions(country_name=country_name,names=temp_final_list_as_a_str,drugCode=drugCode,suggestionString=suggestionString)
            try:
                suggestion.save()
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
                final_list = med_count(temp_list)
                names_dict[p] = final_list
            print(names_dict)
        elif request.POST['input_type'] == 'Therapeutic Name':
            params = request.POST['text_input']
            list_params = []
            for x in range(len(params)):
                if x+3 > len(params):
                    break
                list_params.append(params[x:x+3])
            if len(list_params[-1]) < 3:
                list_params = list_params[ : -1]
            for p in list_params:
                temp_list = generate_new_names(p)
                final_list = med_count(temp_list)
                names_dict[p] = final_list
            print(names_dict)
        elif request.POST['input_type'] == 'Molecular Name':
            params = request.POST['text_input']
            list_params = []
            for x in range(len(params)):
                if x+3 > len(params):
                    break
                list_params.append(params[x:x+3])
            if len(list_params[-1]) < 3:
                list_params = list_params[ : -1]
            for p in list_params:
                temp_list = generate_new_names(p)
                final_list = med_count(temp_list)
                names_dict[p] = final_list
            print(names_dict)
        context = {
            'names': names_dict,
        }
        return render(request, 'predictPage.html', context=context)
    else:
        context = {
            'countries': Country.objects.all(),
        }
        return render(request, 'predictForm.html', context=context)