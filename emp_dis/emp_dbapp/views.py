from django.shortcuts import render
from emp_dbapp.models import *
from django.shortcuts import redirect
import psycopg2

def GetVacancies(request):
    input_text=request.GET.get('serv')
    data={
            'vacancies':Vacancy.objects.filter(status='enabled'),
            'inp':''
        }
    if not input_text:
        return render(request, 'vacancies.html',data)
    else:
        input_text=input_text[0].upper()+input_text[1:].lower()
        new_data=Vacancy.objects.filter(status='enabled',name__icontains=input_text)
        return render(request, 'vacancies.html',{'vacancies':new_data,'inp':input_text})
def GetVacancy(request, idd):
    return render(request, 'vacancy.html',{
            'vacancies':Vacancy.objects.filter(id=idd,status='enabled')[0],
            'inp':''
        })

def delete_vac(request, id):
    conn = psycopg2.connect(database="emp_db", user="emp_user", password="1111", host="localhost", port="5432")
    cur = conn.cursor()

    cur.execute("update vacancy set status='deleted' WHERE id = %s;", (id,))

    conn.commit()
    cur.close()
    conn.close()

    return redirect('all')