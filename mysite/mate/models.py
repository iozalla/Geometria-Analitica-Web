from django.db import models

###Aqui estan las tablas de la base de datos.


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)


class User(models.Model):
    name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    age = models.IntegerField(default=10)
    mail= models.CharField(max_length=200, primary_key=True )
    def __str__(self):
        return self.name
