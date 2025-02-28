from django.db import models

class Login(models.Model):
    username=models.CharField(max_length=50)
    password=models.CharField(max_length=50)
    type=models.CharField(max_length=50)

class User(models.Model):
    LOGIN = models.ForeignKey(Login,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone = models.BigIntegerField()
    image = models.FileField()

class Complaint(models.Model):
    USER = models.ForeignKey(User,on_delete=models.CASCADE)
    complaint = models.CharField(max_length=500)
    date = models.DateField()
    reply = models.CharField(max_length=500)

class Review(models.Model):
    USER = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.FloatField()
    review = models.CharField(max_length=500)
    date = models.DateField()

class Chatbot(models.Model):
    USER = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.CharField(max_length=1000)
    reply = models.TextField()
    date = models.DateField()
    type = models.CharField(max_length=50)

class Payment(models.Model):
    USER = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20)
