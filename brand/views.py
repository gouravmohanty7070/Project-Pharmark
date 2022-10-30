from django.shortcuts import render
from .models import Country
from .utils import generate_new_names, med_count

# Create your views here.
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