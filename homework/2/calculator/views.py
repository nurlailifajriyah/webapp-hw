from django.shortcuts import render

def calculate(request):
    # Creates a Python dictionary that will be used to make name-value pairs available to the view
    context = {}
    context['result'] = 0
    context['operator'] = ''
    context['num1'] = 0
    context['num2'] = 0
    # Retrieves then name from the request if the 'username' HTTP GET parameter is present.
    if 'operator' in request.GET and request.GET['operator'] != '':
        context['operator'] = request.GET['operator']
    if 'num1' in request.GET and request.GET['num1'] != '':
        context['num1'] = int(request.GET['num1'])
    if 'num2' in request.GET and request.GET['num2'] != '':
        context['num2'] = int(request.GET['num2'])
    if 'operatorinput' in request.GET and request.GET['operatorinput'] != '':
        if context['num2'] != 0:
            if context['operator'] == '+':
                context['result'] = context['num1'] + context['num2']
            elif context['operator'] == '-':
                context['result'] = context['num1'] - context['num2']
            elif context['operator'] == 'x':
                context['result'] = context['num1'] * context['num2']
            elif context['operator'] == '/':
                context['result'] = context['num1'] / context['num2']
            if request.GET['operatorinput'] == "=":
                context['num1'] = 0
                context['num2'] = 0
                context['operator'] = ''
            else:
                context['num1'] = context['result']
                context['num2'] = 0
                context['operator'] = request.GET['operatorinput']
        else:
            context['result'] = context['num1']
            context['num2'] = 0
            if request.GET['operatorinput'] == "=":
                context['num1'] = 0
                context['operator'] = ''
            else:
                context['operator'] = request.GET['operatorinput']
    elif 'numberinput' in request.GET:
        if context['num2']:
            context['num2'] = int(request.GET['numberinput'])
            context['result'] = context['num2']
        elif context['num1']:
            if context['operator'] != '':
                context['num2'] = request.GET['numberinput']
                context['result'] = context['num2']
            else:
                context['num1'] = int(request.GET['numberinput'])
                context['result'] = context['num1']
        else:
            context['num1'] = int(request.GET['numberinput'])
            context['result'] = context['num1']
    return render(request, 'calculator.html', context)