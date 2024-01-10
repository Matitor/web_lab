import requests
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.db.models import Q
from emp_api.serilizers import *
from emp_api.models import *
from rest_framework.views import APIView
from rest_framework.decorators import api_view, parser_classes, authentication_classes, permission_classes, action
from emp_api.minio import add_pic
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.contrib.auth import authenticate, login
from emp_api.permissions import *
from django.http import HttpResponse
import uuid
import redis
from django.conf import settings
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly

session_storage = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
user = CustomUser(id=1,email="a", password=123)
moderator = CustomUser(id=2, email="b", password=12345, is_staff=True)

@swagger_auto_schema(method='post', request_body=UserSerializer)
@api_view(['Post'])
@permission_classes([AllowAny])
def create(request):
        print('req is', request.data)
        if CustomUser.objects.filter(email=request.data['email']).exists():
            return Response({'status': 'Exist'}, status=400)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = CustomUser.objects.create_user(email=serializer.data['email'],
                                     password=serializer.data['password'],
                                     is_superuser=serializer.data['is_superuser'],
                                     )
            user.save()
            random_key = str(uuid.uuid4())
            session_storage.set(random_key, serializer.data['email'])
            user_data = {
                "email": request.data['email'],
                "is_superuser": False
            }
            print('user data is ', user_data)
            response = Response(user_data, status=status.HTTP_201_CREATED)
            # response = HttpResponse("{'status': 'ok'}")
            response.set_cookie("session_id", random_key)
            return response
            # return Response({'status': 'Success'}, status=200)
        return Response({'status': 'Error', 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='post', request_body=UserSerializer)
@api_view(['Post'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(request, email=username, password=password)
    
    if user is not None:
        random_key = str(uuid.uuid4())
        user_data = {
            "user_id": user.id,
            "email": user.email,
            "is_superuser": user.is_superuser,
        }
        session_storage.set(random_key, username)
        response = Response(user_data, status=status.HTTP_201_CREATED)
        response.set_cookie("session_id", random_key)

        return response
    else:
        return Response({'status': 'Error'}, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='post', request_body=UserSerializer)
@api_view(['Post'])
@permission_classes([IsAuth])
def logout_view(request):
    ssid = request.COOKIES["session_id"]
    if session_storage.exists(ssid):
        session_storage.delete(ssid)
        response_data = {'status': 'Success'}
    else:
        response_data = {'status': 'Error', 'message': 'Session does not exist'}
    return Response(response_data)


@api_view(['GET'])
# @permission_classes([IsAuth])
def user_info(request):
    try:
        ssid = request.COOKIES["session_id"]
        if session_storage.exists(ssid):
            email = session_storage.get(ssid).decode('utf-8')
            user = CustomUser.objects.get(email=email)
            user_data = {
                "user_id": user.id,
                "email": user.email,
                "is_superuser": user.is_superuser
            }
            return Response(user_data, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'Error', 'message': 'Session does not exist'})
    except:
        return Response({'status': 'Error', 'message': 'Cookies are not transmitted'})
    

class VacanciesAPI(APIView):
    model_class = Vacancy
    serializer_class = VacancySer
    @permission_classes([IsAuth])
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
            ssid = request.COOKIES["session_id"]
            try:
                email = session_storage.get(ssid).decode('utf-8')
                cur_user = CustomUser.objects.get(email=email)
            except:
                return Response('Сессия не найдена')
            answ=Answer.objects.filter(user=cur_user, status="registered").latest('created_at')
            serializerans = AnswerSer(answ)
            return Response({
                'vacancy': serializer.data,
                'answer': serializerans.data['id']
        })
        # заказа-черновика нет
        except:
              return Response({
                  'vacancy': serializer.data,
                  'answer': -1
        })
    @swagger_auto_schema(request_body=VacancySer)
    @permission_classes([IsManager])
    def post(self, request, format=None):
        """
        Добавляет новую вакансию
        """ 
        print(request.data['png'])                                  
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            print(serializer.errors)
            return Response(serializer.errors,status=status.HTTP_403_FORBIDDEN)
        new_vacancy = serializer.save()

        # pic
        pic = request.FILES.get("png")
        pic_result = add_pic(new_vacancy, pic)
        if 'error' in pic_result.data:
            print(pic_result)    # Если в результате вызова add_pic результат - ошибка, возвращаем его.
            return Response("нет фотографии",status=status.HTTP_403_FORBIDDEN)
        # dish = Dishes.objects.filter(status="есть")
        vacanies=Vacancy.objects.filter(status="enabled")
        serializer = self.serializer_class(vacanies,many=True)
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
    @permission_classes([IsManager])
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
    @permission_classes([IsManager])
    def  put(self, request, pk, format=None):       
        """
        Редактирование вакансии
        """                          
        try:
            vac = self.model_class.objects.get(id=pk, status="enabled")
        except self.model_class.DoesNotExist:
            return Response("Вакансии с таким данными нет")

        serializer = self.serializer_class(vac, data=request.data, partial=True)
        if request.FILES.get("png"):
          pic_result = add_pic(vac, request.FILES.get("png"))
          if 'error' in pic_result.data:
              return pic_result
        if serializer.is_valid():
            serializer.save()
            #vac = self.model_class.objects.get(id=pk)
            #serializer = self.serializer_class(vac)
            vacanies=Vacancy.objects.filter(status="enabled")
            serializer = self.serializer_class(vacanies,many=True)
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
        try:
          ssid = request.COOKIES["session_id"]
        except:
          return Response('Сессия не найдена', status=403)    
        try:
          email = session_storage.get(ssid).decode('utf-8')
          current_user = CustomUser.objects.get(email=email)
        except:
          return Response('Сессия не найдена')
        date_format = "%Y-%m-%d"
        start_date_str = request.query_params.get('start', '2023-01-01')
        end_date_str = request.query_params.get('end', '2025-12-31')
        status = request.query_params.get('status')  # Получаем параметр "status" из запроса

        start = datetime.strptime(start_date_str, date_format).date()
        end = datetime.strptime(end_date_str, date_format).date()
        print(status)
        # Формируем фильтр по дате и статусу
        filter_kwargs = {
            'created_at__range': (start, end),
        }
        if status:
            status=[status]
          #if status != 'deleted':
          #        # Используем Q-объект для исключения заявок со статусом "deleted"
          #    filter_kwargs['status'] = ~Q(status='deleted')
          #else:
          #    # Если параметр статуса не указан, исключаем заявки со статусом "deleted"
          #    filter_kwargs['status'] = ~Q(status='deleted')
        else:
            status =['approved','confirmed','denied']

        if current_user.is_superuser: # Модератор может смотреть заявки всех пользователей
            #answ = Answer.objects.filter(**filter_kwargs).order_by('created_at')
            answ = Answer.objects.filter(created_at__range=(start,end)).filter(status__in = status).order_by('created_at')
            serializer = AnswerSer(answ, many=True)

            return Response(serializer.data)
        else: # Авторизованный пользователь может смотреть только свои заявки
            answ = Answer.objects.filter(status__in = ['approved','confirmed','denied']).filter(user = current_user).order_by('created_at')
            serializer = AnswerSer(answ, many=True)

            return Response(serializer.data)
    @permission_classes([IsAuth])  
    def delete(self, request, pk, format=None):
        """
        Удаление заявки(пользователем)
        """
        ssid = request.COOKIES["session_id"]
        try:
            email = session_storage.get(ssid).decode('utf-8')
            current_user = CustomUser.objects.get(email=email)
        except:
            return Response('Сессия не найдена')

        try: 
            resp = Answer.objects.get(user=current_user, status="registered")
            resp.status = "canceled"
            resp.save()
            return Response({'status': 'Success'})
        except:
            return Response("У данного пользователя нет заявки", status=400)


class AnswerAPI(APIView):
    model_class = Answer
    serializer_class = AnswerSer

    def get(self, request, pk, format=None):
      """
      Возвращает 1 заявку
      """
      ssid = request.COOKIES["session_id"]
      try:
        email = session_storage.get(ssid).decode('utf-8')
        current_user = CustomUser.objects.get(email=email)
        print(current_user)
      except:
        return Response('Сессия не найдена')
    
      try:
        answ = Answer.objects.get(pk=pk)
        if answ.status == "deleted" or not answ:
            return Response("Отклика с таким id нет")
        answ_s = AnswerSer(answ)
        if (current_user.is_superuser):
            vac_answ = AnswVac.objects.filter(answ=answ)
            vacancy_ids = [rv.vac.id for rv in vac_answ]
            vacancies = Vacancy.objects.filter(id__in=vacancy_ids)
            vac_s=VacancySer(vacancies,many=True)
            
            answ_data = {
                'answ': answ_s.data,
                'vacancies':  vac_s.data
            }
            return Response(answ_data)
        else:
            try:
                answ = Answer.objects.get(user=current_user, pk=pk)
                print("not superuser")
                vac_answ = AnswVac.objects.filter(answ=answ)
                vacancy_ids = [rv.vac.id for rv in vac_answ]
                vacancies = Vacancy.objects.filter(id__in=vacancy_ids)
                vac_s=VacancySer(vacancies,many=True)
                answ_data = {
                    'answ': answ_s.data,
                    'vacancies':  vac_s.data
            }
                return Response(answ_data)
            except Answer.DoesNotExist:
                return Response("Отклика с таким  id  у данного пользователя нет")
      except Answer.DoesNotExist:
        return Response("Отклика с таким id нет")
    @permission_classes([IsManager])
    def put(request, pk):
        try:
            answ = Answer.objects.get(id=pk)
        except Answer.DoesNotExist:
            return Response("Отклика с таким id нет")
        serializer = AnswerSer(answ, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors)
        serializer.save()

        answ = Answer.objects.all()
        serializer = AnswerSer(answ, many=True)
        return Response(serializer.data)
class VacAnsAPI(APIView):
    model_class = AnswVac
    serializer_class = AnsVacSer
    def delete(self, request, pk, format=None):                              # удаление м-м, передаем id блюда
      ssid = request.COOKIES["session_id"]
      try:
        email = session_storage.get(ssid).decode('utf-8')
        current_user = CustomUser.objects.get(email=email)
      except:
        return Response('Сессия не найдена')
      resp = get_object_or_404(Answer, user=current_user, status="registered")
      try:
        vacancy = Vacancy.objects.get(pk=pk, status='enabled')
        try:
            rv = get_object_or_404(AnswVac, answ=resp, vac=vacancy)
            rv.delete()
            return Response("Вакансия удалена из отклика", status=200)
        except AnswVac.DoesNotExist:
            return Response("Заявка не найдена", status=404)
      except Vacancy.DoesNotExist:
        return Response("Такая вакансия не была добавлена в отклик", status=400)
#@permission_classes([IsAuth])
@api_view(['POST'])
def PAnswToVac(request, pk):
    ssid = request.COOKIES["session_id"]
    try:
        email = session_storage.get(ssid).decode('utf-8')
        current_user = CustomUser.objects.get(email=email)
    except:
        return Response('Сессия не найдена')
    try: 
        answ = Answer.objects.filter(user=current_user, status="registered").latest('created_at') 
    except Answer.DoesNotExist:
        answ = Answer(                             
            status='registered',
            created_at=datetime.now(),
            user=current_user,
        )
        answ.save()
    id_answ = answ.id
    try:
        vacancies = Vacancy.objects.get(pk=pk, status='enabled')
    except Vacancy.DoesNotExist:
        return Response("Такой вакансии нет", status=400)
    try:
        id_vacancies = AnswVac.objects.get(answ=answ, vac=vacancies)
        print(id_vacancies) # проверка есть ли такая м-м
        return Response(f"Такой отклик на эту вакансию уже есть",status=406)
    except AnswVac.DoesNotExist:
        av = AnswVac(                            # если нет, создаем м-м
            answ=answ, vac=vacancies
        )
        av.save()
    answ = Answer.objects.filter(user=current_user, status='registered')
    serializer = AnswerSer(answ, many = True)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsManager])                                  # статусы модератора
def ConfirmAnsw(request, pk):
    if not Answer.objects.filter(id=pk).exists():
        return Response(f"Заказа с таким id нет")

    answ = Answer.objects.get(id=pk)
    ssid = request.COOKIES["session_id"]
    email = session_storage.get(ssid).decode('utf-8')
    cur_user = CustomUser.objects.get(email=email)

    if bool(cur_user.is_staff == False and cur_user.is_superuser == False):
        return Response("Нет прав", status=status.HTTP_403_FORBIDDEN)
    else:
        answ.moderator=cur_user                  # назначаем модератора

        if answ.status != "confirmed":
            return Response("Такой ответ не сформирован", status=status.HTTP_400_BAD_REQUEST)
        if request.data["status"] not in ["approved", "denied"]:
            return Response("Ошибка", status=status.HTTP_400_BAD_REQUEST)
        answ.status = request.data["status"]
        answ.completed_at=datetime.now()
        answ.save()

        serializer = AnswerSer(answ)
        return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuth])
def ToAnsw(request):
    ssid = request.COOKIES["session_id"]
    try:
        email = session_storage.get(ssid).decode('utf-8')
        current_user = CustomUser.objects.get(email=email)
    except:
        return Response('Сессия не найдена')

    try: 
        resp = Answer.objects.get(user=current_user, status="registered")
        resp.status = "confirmed"
        resp.processed_at=datetime.now()
        resp.save()
        serializer = AnswerSer(resp)
        return Response(serializer.data)
    except:
        return Response("У данного пользователя нет зарегистрированного отклика", status=400)

@api_view(['PUT'])
def handle_async_task(request,pk):
    print("HHHHHHHHh")
    answ_id = pk
    token = 4321
    print(answ_id)
    second_service_url = "http://localhost:8088/async_task"
    data = {
        'answ_id': answ_id,
        'token': token
    }

    headers = {
        'Content-Type': 'application/json'
    }

    answ = requests.post(second_service_url, data=data)
    exp = Answer.objects.get(id=answ_id)
    
    # Обработка ответа от второго сервиса
    if answ.status_code == 200:
        exp.suite = "Отправлено на ревью"
        exp.save()
        serializer = AnswerSer(exp)
        return Response(serializer.data)
    else:
        return Response(data={'error': 'Запрос завершился с кодом: {}'.format(answ.status_code)},
                        status=answ.status_code)

@api_view(['POST'])
@permission_classes([AllowAny])
def put_async(request, format=None):
    """
    Обновляет данные 
    """
    print("вызвалось")
    # Проверка метода запроса (должен быть PUT)
    if request.method != 'POST':
        return Response({'error': 'Метод не разрешен'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    exp_id = request.data.get('answ_id')
    result = request.data.get('suite')
    tokken = request.data.get('token')
    # Проверка наличия всех необходимых параметров
    print(tokken)    
    if tokken == '4321':
      if not exp_id or not result or tokken != '4321':
          return Response({'error': 'Отсутствуют необходимые данные'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Неверный токен'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        exp = Answer.objects.get(id=exp_id)
    except Answer.DoesNotExist:
        return Response({'error': 'Отклик не найден'}, status=status.HTTP_404_NOT_FOUND)

    exp.suite = str(result) + " %"
    exp.save()
    serializer = AnswerSer(exp)
    print(serializer.data)
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAuth])  
def delete(request,  format=None):
        """
        Удаление заявки(пользователем)
        """
        ssid = request.COOKIES["session_id"]
        try:
            email = session_storage.get(ssid).decode('utf-8')
            current_user = CustomUser.objects.get(email=email)
        except:
            return Response('Сессия не найдена')

        try: 
            resp = Answer.objects.get(user=current_user, status="registered")
            resp.status = "canceled"
            resp.save()
            return Response({'status': 'Success'})
        except:
            return Response("У данного пользователя нет заявки", status=400)