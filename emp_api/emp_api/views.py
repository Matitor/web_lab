from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.db.models import Q
from emp_api.serilizers import *
from emp_api.models import *
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from emp_api.minio import add_pic

user = Users(id=1,name="User", email="a", password=1234, role="user", login="aa")
moderator = Users(id=2, name="mod", email="b", password=12345, role="moderator", login="bb")

class VacanciesAPI(APIView):
    model_class = Vacancy
    serializer_class = VacancySer
    def get(self, request, format=None):
        """
        Возвращает список всех вакансий
        """                                    
        #min_price = request.query_params.get("price_min", '0')
        #max_price = request.query_params.get("price_max", '10000000')
        name_ = request.query_params.get("name", '')

        #filters = Q(status="enabled") 
        ##& Q(price__range=(min_price, max_price))
        #if name_ != '':
        #    filters &= Q(name=name_)

        vacancies = self.model_class.objects.filter(name__icontains=name_).filter(status="enabled")
        #vacancies = self.model_class.objects.filter()
        serializer = self.serializer_class(vacancies, many=True)
        # заказ определенного пользователя
        try: 
            answ=Answer.objects.filter(user=user, status="зарегистрирован").latest('created_at')
            serializerans = AnswerSer(answ)
            return Response({
                'vacancy': serializer.data,
                'answer': serializerans.data
        })
        # заказа-черновика нет
        except:
            return Response({
                'vacancy': serializer.data,
                'answer': []
        })
    def post(self, request, format=None):
        """
        Добавляет новую вакансию
        """                                   
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors)
        new_vacancy = serializer.save()

        # pic
        pic = request.FILES.get("png")
        pic_result = add_pic(new_vacancy, pic)
        if 'error' in pic_result.data:    # Если в результате вызова add_pic результат - ошибка, возвращаем его.
            return pic_result
        # dish = Dishes.objects.filter(status="есть")
        serializer = self.serializer_class(new_vacancy)
        return Response(serializer.data)
class VacancyAPI(APIView):
    model_class = Vacancy
    serializer_class = VacancySer

    def get(self, request, pk, format=None):
        """
        Возвращяет 1 вакансию
        """       
        if not self.model_class.objects.filter(id=pk, status="enabled").exists():
            return Response(f"Такой вакансии нет")

        vac = self.model_class.objects.get(id=pk)
        serializer = self.serializer_class(vac)
        return Response(serializer.data)

    def  delete(self, request, pk, format=None):                              
        """
        Удаление вакансии
        """
        if not self.model_class.objects.filter(id=pk, status="enabled").exists():
            return Response("Такой вакансии нет")
        dish = self.model_class.objects.get(id=pk)
        dish.status = "deleted"
        dish.save()
        return Response({"message": "success"})

    def  put(self, request, pk, format=None):       
        """
        Редактирование вакансии
        """                          
        try:
            vac = self.model_class.objects.get(id=pk, status="enabled")
        except self.model_class.DoesNotExist:
            return Response("Вакансии с таким данными нет")

        serializer = self.serializer_class(vac, data=request.data, partial=True)

        pic_result = add_pic(vac, serializer.initial_data['png'])
        if 'error' in pic_result.data:
            return pic_result
        if serializer.is_valid():
            serializer.save()
            vac = self.model_class.objects.get(id=pk)
            serializer = self.serializer_class(vac)

            return Response(serializer.data)
        else:
            return Response(serializer.errors)
class AnswersAPI(APIView):
    model_class = Answer
    serializer_class = AnswerSer
    def get(self, request, format=None):   
        """
        Возвращяет список всех заявок
        """                              
        date_format = "%Y-%m-%d"
        start_date_str = request.query_params.get("start", '2000-01-01')
        end_date_str = request.query_params.get("end", '3023-12-31')
        start = datetime.strptime(start_date_str, date_format).date()
        end = datetime.strptime(end_date_str, date_format).date()
        status = request.query_params.get("status", '')
        filters = ~Q(status="deleted") & Q(created_at__range=(start, end))
        if status != '':
            filters &= Q(status=status)
            
        answ = self.model_class.objects.filter(filters).order_by('created_at')
        serializer = self.serializer_class(answ, many=True)
        
        return Response(serializer.data)


class AnswerAPI(APIView):
    model_class = Answer
    serializer_class = AnswerSer

    def get(self, request, pk, format=None):
        """
        Возвращает 1 заявку
        """
        try:
            answ = self.model_class.objects.get(id=pk)
        except self.model_class.DoesNotExist:
            return Response("Заявки с такими данными нет")

        serializer = self.serializer_class(answ)
        return Response(serializer.data)
    
    def delete(self, request, pk, format=None):
        """
        Удаление заявки(модератором)
        """
        if not self.model_class.objects.filter(id=pk).exists():
            return Response(f"Заявки с такими данными нет")
        answ = self.model_class.objects.get(id=pk)
        answ.status = "denied"
        answ.save()
        return Response({"status": "success"})
class VacAnsAPI(APIView):
    model_class = AnswVac
    serializer_class = AnsVacSer
    def put(self, request, pk, format=None):   
        '''
        изменение м-м(кол-во), передаем id заявки
        '''                            
        try: 
            ans=Answer.objects.get(user=user, status="registered", id=pk) # заказ определенного пользователя
        except:
            return Response("нет такой заявки")
        if not AnswVac.objects.filter(answ=ans.id).exists():
            return Response("нет такой вакансии")
        VA = AnswVac.objects.get(id=pk)
        VA.quantity = request.data["quantity"]
        VA.save()

        VA = AnswVac.objects.all()
        serializer = self.serializer_class(VA, many=True)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):          
        '''
        удаление м-м, передаем id заказа
        '''                    
        try: 
            answ=Answer.objects.get(user=user, status="registered", id=pk) # заказ определенного пользователя
        except:
            return Response("нет такого заявки")
        if not AnswVac.objects.filter(answ=answ.id).exists():
            return Response("нет такой вакансии")

        VA = get_object_or_404(AnswVac, id=pk)
        VA.delete()

        VA = AnswVac.objects.all()
        serializer = self.serializer_class(VA, many=True)
        return Response(serializer.data)
@api_view(['Delete'])
def delete(self, request, pk, format=None):
        """
        Удаление заявки(пользователем)
        """
        if not self.model_class.objects.filter(id=pk).exists():
            return Response("Заявки с такими данными нет")
        answ = self.model_class.objects.get(id=pk)
        answ.status = "canceled"
        answ.save()
        return Response({"status": "success"})

@api_view(['PUT'])
def PAnswToVac(request, pk):
    try: 
        answ=Answer.objects.filter(user=user, status="registered").latest('created_at') # заказ определенного пользователя
    except:
        answ = Answer(                              # если нет, создаем новый заказ
            status='registered',
            created_at=datetime.now(),
            user=user,
        )
        answ.save()

    if not Vacancy.objects.filter(id=pk, status="enabled").exists():
        return Response("Такой вакансии нет")

    answ_id=answ.id
    vac_id=pk
    try:
        VA=AnswVac.objects.get(answ_id=answ_id, vac_id=vac_id) #проверка есть ли такая м-м
        VA.quantity+=1    # если да, не создаем новую а меняем существующую
        VA.save()
    except:
        VA = AnswVac(    
            vac_id=vac_id,               # если нет, создаем м-м
            answ_id=answ_id,
            quantity=1
        )
        VA.save()
    answ = Answer.objects.get(id=answ_id)  
    serializer = AnsVacUserSer(answ)
    return Response(serializer.data)

@api_view(['PUT'])                                  # статусы модератора
def ConfirmAnsw(request, pk):
    if not Answer.objects.filter(id=pk).exists():
        return Response(f"Заявки с таким id нет")

    answ = Answer.objects.get(id=pk)

    if answ.status != "confirmed":
        return Response("Такая заявка не сформирована")
    if request.data["status"] not in ["denied", "approved"]:
        return Response("Ошибка")
    answ.status = request.data["status"]
    answ.completed_at=datetime.now()
    answ.save()

    serializer = AnswerSer(answ)
    return Response(serializer.data)

@api_view(['PUT'])                                  # статусы пользователя
def ToAnsw(request, pk):
    if not Answer.objects.filter(id=pk).exists():
        return Response(f"Заявки с таким id нет")

    answ = Answer.objects.get(id=pk)

    if answ.status != "registered":
        return Response(serializer.errors)
    if request.data["status"] not in ["confirmed", "canceled"]:
        return Response(serializer.errors)

    answ.status = request.data["status"]
    answ.processed_at=datetime.now()           #.strftime("%d.%m.%Y %H:%M:%S")
    answ.moderator=moderator                   # назначаем модератора
    answ.save()

    serializer = AnsVacSer(answ)
    return Response(serializer.data)