from django.shortcuts import render
from datetime import date

def GetData(id=0):
    data = {
        'services': [
            {
              'id':1,
              'name':"Удаленный менеджер",
              'desc':"Слух, речь",
              'price':"60'000 - 100'000 ₽",
              'company':"СТМ",
              'pic':'images/services/p1.png'
            },
            {
              'id':2,
              'name':"Водитель такси",
              'desc':"АГа",
              'price':"От 100'000 ₽",
              'company':"неТАкси",
              'pic':'images/services/p2.png'
            },
            {
              'id':3,
              'name':"Упаковщик заказов для ДомашняяКлубника",
              'desc':"ух",
              'price':"До 300'000 ₽",
              'company':"ДомашняяКлубника",
              'pic':'images/services/p1.png'
            },
            {
              'id':4,
              'name':"Оператор колл-центра",
              'desc':"asda",
              'price':"От 40'000 ₽",
              'company':"Пчелайн",
              'pic':'images/services/p1.png'
            }
        ],
        'inp':''
    }
    if id != 0:
        return data['services'][id-1]
    else:
        return data
def GetServices(request):
    input_text=request.GET.get('serv')
    data=GetData(0)
    if not input_text:
        return render(request, 'services.html',data)
    else:
        new_data=[]
        for i in data['services']:
            if input_text.lower() in i.get('name','').lower():
                new_data.append(i)
        return render(request, 'services.html',{'services':new_data,'inp':input_text})
def GetService(request, idd):
    return render(request, 'service.html',GetData(id=idd))
#def sendText(request):
#    input_text = request.GET.get('text')
#    param=GetData(text=input_text)
#    return render(request, 'services.html',param)
