from django.shortcuts import render
from .models import Country

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
        if request.POST['input_type'] == 'List of Strings':
            params = request.POST['text_input'].split(',')
            print(params)
            pass
        elif request.POST['input_type'] == 'Therapeutic Name':
            pass
        elif request.POST['input_type'] == 'Molecular Name':
            pass
        return render(request, 'predictPage.html')
    else:
        context = {
            'countries': Country.objects.all(),
        }
        return render(request, 'predictForm.html', context=context)