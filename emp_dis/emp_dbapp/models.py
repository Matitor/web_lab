from django.db import models


class Service(models.Model):
    name = models.CharField(max_length=30)
    desc = models.CharField(max_length=255)
    price = models.CharField(max_length=30)
    company = models.CharField(max_length=30)
    pic = models.CharField(max_length=30)
    adress = models.CharField(max_length=30)
    total_desc = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'service'