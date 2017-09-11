from django.http import HttpResponse
from django.shortcuts import render

def calculate(request):
    # Creates a Python dictionary that will be used to make name-value pairs available to the view
    context = {}
    context['number_value'] = ''

    # Retrieves then name from the request if the 'username' HTTP GET parameter is present.
    if 'number' in request.GET:
        context['number_value'] = request.GET['number']

    return render(request, 'calculator.html', context)