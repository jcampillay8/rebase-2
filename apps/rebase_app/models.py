from django.db import models
import bcrypt
import datetime
from apps.login_register.models import User

class Text(models.Model):
    content = models.TextField()
    text_name = models.CharField(max_length=250, default="", editable=False)
    user = models.ForeignKey(User, related_name='textos', on_delete=models.CASCADE)
    contador = models.IntegerField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now_add=True)
