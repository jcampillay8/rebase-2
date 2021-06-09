from django.db import models
import re
import datetime
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'\d.*[A-Z]|[A-Z].*\d')
DATE_REGEX = re.compile(r'^([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))')

# Create your models here.
class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}

        # Validate first name
        if(len(postData['first_name'])) < 2:
            errors['first_name'] = "Nombre debe tener a lo menos 3 caracteres"
        elif postData['first_name'].isalpha() == False:
            errors['first_name'] = "Nombre solo acepta letras"
        
        # Validate last name
        if(len(postData['last_name'])) < 2:
            errors['last_name'] = "Apellido debe tener a lo menos 3 caracteres"
        elif postData['last_name'].isalpha() == False:
            errors['last_name'] = "Apellido solo acepta letras"

        # Validate username
        username_exists = User.objects.filter(username=postData['username'])
        if len(username_exists) != 0:
            errors['username'] = " Nombre usuario ya existe"
        
        # Validate Birthdate
        if len(postData['birthdate']) < 1:
            errors['birthdate'] = "Fecha nacimiento es obligatorio"
        elif not DATE_REGEX.match(postData['birthdate']):
            errors['birthdate'] = "Fecha invalida, usa dd-mm-aaaa formato"
        else:
            current_time = datetime.datetime.now()
            temp_time = datetime.datetime.strptime(postData['birthdate'], "%Y-%m-%d")
            if temp_time >= current_time:
                errors['birthdate'] = "Fecha ingresada no puede estar en el futuro"

        # Validate Email
        email_exists = User.objects.filter(email=postData['email'])
        if len(email_exists) != 0:
            errors['email'] = " Correo Electrónico ya existe "        
        if len(postData['email']) < 1:
            errors['email'] = "Correo Electrónico es obligatorio"
        elif not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Correo Electrónico debe llevar arroba y dominio"

        # Validate Confirm Email
        if len(postData['confirm_email']) < 1:
            errors['confirm_email'] = "Confirmación Correo Electrónico es obligatorio"
        elif postData['email'] != postData['confirm_email']:
            errors['confirm_email'] = "Correos Electrónicos no son iguales"

        # Validate Password
        if len(postData['password']) < 8:
            errors['password'] = "Contraseña debe tener un largo de a lo menos 8 caracteres"
        elif not PASSWORD_REGEX.match(postData['password']):
            errors['password'] = "Contraseña invalida, debe tener a lo menos una mayúscula y un número"

        # Validate Confrim Password
        if len(postData['confirm_password']) < 1:
            errors['confirm'] = "Confirmar contraseña es obligatorio"
        elif postData['password'] != postData['confirm_password']:
            errors['confirm'] = "Contraseñas no son iguales"      
            
        return errors
    
    def login_validator(self, user_data):
            errors = {}

            try:
                user = User.objects.get(email = user_data["loginEmail"])
            
            except:
                errors["loginEmail"] = f"No existe el correo {user_data['loginEmail']} o una cuenta asociada con este correo"
                return errors
            
            if not bcrypt.checkpw(user_data["password"].encode(), user.password.encode()):
                errors["password"] = "Contraseña incorrecta, por favor intentelo de nuevo"
            
            return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    birthdate = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects= UserManager()
