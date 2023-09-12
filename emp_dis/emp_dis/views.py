from django.shortcuts import render
from datetime import date
from django.shortcuts import redirect

def GetServices(request):
    return render(request, 'services.html', {'data' : {
        'current_date': date.today(),
        'services': [
            {
              'id':1,
              'name':1,
              'pic':1,
              'desc':1,
              'pic':'images/services/p1.png'
            },
            {
                'id':2,
              'name':2,
              'pic':2,
              'desc':2,
              'pic':'images/services/p2.png'
            },
            {
                'id':3,
              'name':3,
              'pic':3,
              'desc':3,
              'pic':'images/services/p1.png'
            },
            {
                'id':4,
              'name':4,
              'pic':4,
              'desc':4,
              'pic':'images/services/p1.png'
            },
            {
                'id':5,
              'name':5,
              'pic':5,
              'desc':5,
              'pic':'images/services/p1.png'
            }
        ],
        'filt':'1'
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