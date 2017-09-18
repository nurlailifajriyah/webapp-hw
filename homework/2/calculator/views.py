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
        if checkInteger (request.POST['num1']) == True:
            context['num1'] = int(request.POST['num1'])
        else:
            context['result'] = 'error'
            context['operator'] = ''
            context['num1'] = ''
            context['num2'] = ''
            return render(request, 'calculator.html', context)
    if 'num2' in request.POST and request.POST['num2'] != '':
        if checkInteger (request.POST['num2']) == True:
            context['num2'] = int(request.POST['num2'])
        else:
            context['result'] = 'error'
            context['operator'] = ''
            context['num1'] = ''
            context['num2'] = ''
            return render(request, 'calculator.html', context)
    if 'operatorinput' in request.POST and request.POST['operatorinput'] != '':
        if request.POST['operatorinput'] == '+' or request.POST['operatorinput'] == '-' or request.POST['operatorinput'] == 'x' or request.POST['operatorinput'] == '/' or request.POST['operatorinput'] == '=':
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
                else:
                    context['result'] = 'error'
                if context['result'] == "error":
                    context['num2'] = ''
                    context['operator'] = ''
                    context['num1'] = ''
                    return render(request, 'calculator.html', context)
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
                            context['operator'] = request.POST['operatorinput']
                        else:
                            context['operator'] = request.POST['operatorinput']
        else:
            context['result'] = 'error'
            context['operator'] = ''
            context['num1'] = ''
            context['num2'] = ''
    elif 'numberinput' in request.POST and request.POST['numberinput'] != '':
        if checkInteger(request.POST['numberinput']) == True:
            if context['num2'] != '':
                context['num2'] = int(request.POST['numberinput'])
                context['result'] = context['num2']
            elif context['num1'] != '':
                if context['operator'] != '':
                    if context['operator'] == '=':
                        context['num1'] = request.POST['numberinput']
                        context['result'] = context['num1']
                        context['operator'] = ''
                    else:
                        context['num2'] = request.POST['numberinput']
                        context['result'] = context['num2']
                else:
                    context['num1'] = int(request.POST['numberinput'])
                    context['result'] = context['num1']
            else:
                context['num1'] = int(request.POST['numberinput'])
                context['result'] = context['num1']
        else:
            context['result'] = 'error'
            context['operator'] = ''
            context['num1'] = ''
            context['num2'] = ''
    return render(request, 'calculator.html', context)

def checkInteger(parameter):
    try:
        int(parameter)
        return True
    except ValueError:
        return False

