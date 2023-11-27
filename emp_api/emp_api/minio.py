'''
sudo MINIO_ROOT_USER=admin MINIO_ROOT_PASSWORD=password ./minio server /mnt/data --console-address ":9001"
'''
from minio import Minio
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework.response import *

def process_file_upload(file_object: InMemoryUploadedFile, client, image_name):
    try:
        client.put_object('vacancies', image_name, file_object, file_object.size)
        return f"http://localhost:9000/vacancies/{image_name}"
    except Exception as e:
        return {"error": str(e)}
def add_pic(new_vacancy, pic):
    client = Minio(endpoint="localhost:9000",
                   access_key='admin',
                   secret_key='password',
                   secure=False)
    i = new_vacancy.id-1
    img_obj_name = f"{i}.png"

    if not pic:
        return Response({"error": "Нет файла для изображения вакансии."})
    result = process_file_upload(pic, client, img_obj_name)
    if 'error' in result:
        return Response(result)

    
    new_vacancy.pic = result

    new_vacancy.save()
    return Response({"message": "success"})