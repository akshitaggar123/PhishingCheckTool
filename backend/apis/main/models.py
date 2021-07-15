from django.db import models

# Create your models here.

class Url(models.Model):
    main=models.CharField(max_length=250)
    similar=models.CharField(max_length=250)
    score=models.IntegerField()
    updated=models.CharField(max_length=20)

    def __str__(self):
        return self.main + '-' +  self.similar

class Verify(models.Model):
    url=models.CharField(max_length=250)
    identity=models.CharField(max_length=10,default='0000000000')

    def __str__(self):
        return self.url + '-' +  self.identity

class Report(models.Model):
    url=models.CharField(max_length=250)
    #identity=models.CharField(max_length=10,default='0000000000')
    updated=models.CharField(max_length=20)
    count=models.IntegerField()

    def __str__(self):
        return self.url + '-' +  self.updated

class Fraud(models.Model):
    url=models.CharField(max_length=250)

    def __str__(self):
        return self.url

class Person(models.Model):
    identity=models.CharField(max_length=10)
    updated=models.CharField(max_length=20)
    count=models.IntegerField()
    category=models.CharField(max_length=10,default='branding')

    def __str__(self):
        return self.id

