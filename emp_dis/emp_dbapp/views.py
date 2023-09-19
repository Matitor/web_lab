from django.shortcuts import render
from datetime import date
from emp_dbapp.models import *

def GetServices(request):
    input_text=request.GET.get('serv')
    data={
            'services':Service.objects.all(),
            'inp':''
        }
    if not input_text:
        return render(request, 'services.html',data)
    else:
        new_data=[]
        for i in data['services']:
            if input_text.lower() in i.get('name','').lower():
                new_data.append(i)
        return render(request, 'services.html',{'services':new_data,'inp':input_text})
def GetService(request, idd):
    return render(request, 'service.html',data={
            'services':Service.objects.filter(id=idd)[0],
            'inp':''
        })
#def sendText(request):
#    input_text = request.GET.get('text')
#    param=GetData(text=input_text)
#    return render(request, 'services.html',param)
