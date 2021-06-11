from django.db import models
import bcrypt
import datetime
from apps.login_register.models import User
import requests 

class SentenceManager(models.Manager):
    def add_sentence_validator(self, postData, actual):
        user = User.objects.get(id=actual)
        errors={}
        # Validar no frase repetida
        current_sentences =Sentence.objects.filter(user_frase=user)
        list_sentences=[]

        for i in current_sentences:
            list_sentences.append(i.frase)
            print(list_sentences)

        sentence_exists = Sentence.objects.filter(frase=postData['new_sentence'])
        print(postData['new_sentence'])
        if postData['new_sentence'] in list_sentences:
            errors['new_sentence'] = f" La frase '{postData['new_sentence']}' ya ha sido iuncluida"
        return errors

class Text(models.Model):
    content = models.TextField()
    text_name = models.CharField(max_length=250, default="", editable=False)
    user = models.ForeignKey(User, related_name='textos', on_delete=models.CASCADE)
    contador = models.IntegerField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now_add=True)


class Sentence(models.Model):
    frase = models.CharField(max_length=250, default="", editable=False)
    valor_frase = models.IntegerField(default=10)
    user_frase = models.ForeignKey(User, related_name='sentencias', on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now_add=True)
    objects= SentenceManager()
