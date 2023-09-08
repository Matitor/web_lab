from django.shortcuts import render
from datetime import date
from django.shortcuts import redirect

def GetServices(request):
    return render(request, 'services.html', {'data' : {
        'current_date': date.today(),
        'services': [
            {'title': 'Книга с картинками', 'id': 1},
            {'title': 'Бутылка с водой', 'id': 2},
            {'title': 'Коврик для мышки', 'id': 3},
        ]
    }})
def GetService(request, id):
    return render(request, 'service.html', {'data' : {
        'current_date': date.today(),
        'id': id
    }})
def sendText(request):
    input_text = request.POST['text']
    return redirect('sendText', 'sendtext.html',{'data':{
        'text':input_text
        }})