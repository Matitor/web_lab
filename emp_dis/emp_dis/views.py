from django.shortcuts import render
from datetime import date

def GetData(id=0):
    data = {
        'vacancies': [
            {
              'id':1,
              'name':"Удаленный менеджер",
              'desc':"I и II группа инвалидности",
              'price':"60'000 - 100'000 ₽",
              'company':"СТМ",
              'pic':'images/vacancy/p11.png',
              'adress':"Москва, дом пушкина",
              'total_desc':"подробное описание вакансии"
            },
            {
              'id':2,
              'name':"Водитель такси",
              'desc':"Только I группа инвалидности",
              'price':"От 100'000 ₽",
              'company':"неТАкси",
              'pic':'images/vacancy/p22.png',
              'adress':"Москва, улица колотушкина",
              'total_desc':"подробное описание вакансии"
            },
            {
              'id':3,
              'name':"Упаковщик заказов для ДомашняяКлубника",
              'desc':"Только I группа инвалидности",
              'price':"До 300'000 ₽",
              'company':"ДомашняяКлубника",
              'pic':'images/vacancy/p3.png',
              'adress':"Москва, проспект чайной церемонии",
              'total_desc':"подробное описание вакансии"
            },
            {
              'id':4,
              'name':"Оператор колл-центра",
              'desc':"I,II и III группа инвалидности",
              'price':"От 40'000 ₽",
              'company':"Пчелайн",
              'pic':'images/vacancy/p4.png',
              'adress':"Москва, улица приколов",
              'total_desc':"подробное описание вакансии"
            }
        ],
        'inp':''
    }
    if id != 0:
        return data['vacancies'][id-1]
    else:
        return data
def GetServices(request):
    input_text=request.GET.get('serv')
    data=GetData(0)
    if not input_text:
        return render(request, 'vacancies.html',data)
    else:
        new_data=[]
        for i in data['vacancies']:
            if input_text.lower() in i.get('name','').lower():
                new_data.append(i)
        return render(request, 'vacancies.html',{'vacancies':new_data,'inp':input_text})
def GetService(request, idd):
    return render(request, 'vacancy.html',GetData(id=idd))
#def sendText(request):
#    input_text = request.GET.get('text')
#    param=GetData(text=input_text)
#    return render(request, 'vacancies.html',param)
