from django.db import models

# Create your models here.
# 나중에 캐시 데이터 베이스로 사용할 수도 있으니 냅두기
class Etf(models.Model):
    item = models.CharField(max_length=100)
    close = models.CharField(max_length=20)
    date = models.CharField(max_length=20)

class Interest(models.Model):
    submitpn = models.CharField(max_length=6)
    banknm = models.CharField(max_length=20)
    goodnm = models.CharField(max_length=50)
    wayre = models.CharField(max_length=100)
    materityinterest = models.TextField()
    priority = models.TextField()
    limit_rate = models.IntegerField()
    retarget = models.TextField()
    atmost = models.BigIntegerField()
    interestnm = models.CharField(max_length=10)
    typesave = models.CharField(max_length=10)
    period = models.CharField(max_length=30)
    interestrate = models.IntegerField()
    maxinterest = models.IntegerField()

class KoreaBond(models.Model):
    item_name = models.CharField(max_length=20)
    close = models.DecimalField(decimal_places=2, max_digits=5)
    change = models.CharField(max_length=20)
    one_month = models.CharField(max_length=20)
    six_month = models.CharField(max_length=20) 
    one_year = models.CharField(max_length=20)

class P2p(models.Model):
    information = models.TextField()

class UsBond(models.Model):
    item_name = models.CharField(max_length=20)
    close = models.DecimalField(decimal_places=2, max_digits=5)
    change = models.CharField(max_length=20)
    one_month = models.CharField(max_length=20)
    six_month = models.CharField(max_length=20)
    one_year = models.CharField(max_length=20)