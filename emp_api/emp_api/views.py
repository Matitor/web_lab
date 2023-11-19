from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.db.models import Q
from emp_api.serilizers import *
from emp_api.models import *
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from emp_api.minio import add_pic

user = Users(id=1, name="User", email="a", password=1234, role="user", login="aa")
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

        filters = Q(status="активна") 
        #& Q(price__range=(min_price, max_price))
        if name_ != '':
            filters &= Q(name=name_)

        #vacancies = self.model_class.objects.filter(filters)
        vacancies = self.model_class.objects.filter()
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
        pic_result = add_pic(new_vacancy, pic, 0)
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
            return Response(f"Такого блюда нет")
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
class AnswerAPI(APIView):
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
            return Response(f"Заявки с такими данными нет")

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
class VacAnswAPI(APIView):
    model_class = AnswVac
    serializer_class = AnsVacSer

    def put(self, request, pk, format=None):   
        """
        Изменение м-м по id заявки
        """                            
        try: 
            answ=Answer.objects.get(user=user, status="registered", id=pk)
        except:
            return Response("нет такой заявки")
        if not AnswVac.objects.filter(answer=answ.id).exists():
            return Response(f"нет такой заявки на вакансию")
        AV = AnswVac.objects.get(id=pk)
        AV.quantity = request.data["quantity"]
        AV.save()

        AV = AnswVac.objects.all()
        serializer = self.serializer_class(AV, many=True)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):              
        """
        удаление м-м по id заявки
        """                # удаление м-м, передаем id заказа
        try: 
            order=Orders.objects.get(user=user, status="зарегистрирован", id=pk) # заказ определенного пользователя
        except:
            return Response("нет такого заказа")
        if not DishesOrders.objects.filter(order=order.id).exists():
            return Response(f"в заказе нет блюд")

        dishes_orders = get_object_or_404(DishesOrders, id=pk)
        dishes_orders.delete()

        dishes_orders = DishesOrders.objects.all()
        serializer = self.serializer_class(dishes_orders, many=True)
        return Response(serializer.data)    

@api_view(['Delete'])
def delete(self, request, pk, format=None):
        """
        Удаление заявки(пользователем)
        """
        if not self.model_class.objects.filter(id=pk).exists():
            return Response(f"Заявки с такими данными нет")
        answ = self.model_class.objects.get(id=pk)
        answ.status = "canceled"
        answ.save()
        return Response({"status": "success"})
