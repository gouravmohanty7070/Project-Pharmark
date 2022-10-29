from django.shortcuts import render

# Create your views here.
def homepage(request):
    return render(request, 'home.html')

def predictFormPage(request):
    return render(request, 'predictForm.html')