from django.shortcuts import render

def calculate(request):
    # Creates a Python dictionary that will be used to make name-value pairs available to the view
    context = {}
    context['result'] = ''
    context['operator'] = ''
    context['num1'] = ''
    context['num2'] = ''
    # Retrieves then name from the request if the 'username' HTTP GET parameter is present.
    if 'operator' in request.POST and request.POST['operator'] != '':
        context['operator'] = request.POST['operator']
    if 'num1' in request.POST and request.POST['num1'] != '':
        context['num1'] = int(request.POST['num1'])
    if 'num2' in request.POST and request.POST['num2'] != '':
        context['num2'] = int(request.POST['num2'])
    if 'operatorinput' in request.POST and request.POST['operatorinput'] != '':
        if context['num2'] != '':
            if context['operator'] == '+':
                context['result'] = context['num1'] + context['num2']
            elif context['operator'] == '-':
                context['result'] = context['num1'] - context['num2']
            elif context['operator'] == 'x':
                context['result'] = context['num1'] * context['num2']
            elif context['operator'] == '/':
                if context['num2'] == 0:
                    context['result'] = "error"
                else:
                    context['result'] = context['num1'] / context['num2']
            if context['result'] == "error":
                context['num2'] = ''
            elif request.POST['operatorinput'] == "=":
                context['num1'] = context['result']
                context['num2'] = ''
                context['operator'] = ''
            else:
                context['num1'] = context['result']
                context['num2'] = ''
                context['operator'] = request.POST['operatorinput']
        else:
            context['result'] = context['num1']
            context['num2'] = ''
            if context['num1'] == '':
                context['result'] = 0;
                context['num1'] = context['result']
                context['num2'] = ''
                context['operator'] = request.POST['operatorinput']
            else:
                if context['operator'] != '':
                    context['operator'] = request.POST['operatorinput']
                else:
                    if request.POST['operatorinput'] == "=":
                        context['num1'] = context['result']
                        context['num2'] = ''
                        context['operator'] = ''
                    else:
                        context['operator'] = request.POST['operatorinput']
    elif 'numberinput' in request.POST:
        if context['num2'] != '':
            context['num2'] = int(request.POST['numberinput'])
            context['result'] = context['num2']
        elif context['num1'] != '':
            if context['operator'] != '':
                context['num2'] = request.POST['numberinput']
                context['result'] = context['num2']
            else:
                context['num1'] = int(request.POST['numberinput'])
                context['result'] = context['num1']
        else:
            context['num1'] = int(request.POST['numberinput'])
            context['result'] = context['num1']
    return render(request, 'calculator.html', context)