from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
import bcrypt

def index(request):
    return render(request, 'index.html')


def register(request):
    errors = User.objects.register_validator(request.POST)
    
    if(len(errors)):
        for tag, error in errors.items():
            messages.error(request, error, extra_tags=tag)
        return redirect('index')
    else:
        firstName = request.POST.get('first_name')
        lastName = request.POST.get('last_name')
        userName = request.POST.get('username')
        email = request.POST.get('email')
        hashed_password = bcrypt.hashpw(request.POST.get('password').encode(),bcrypt.gensalt()).decode()
        birthDate = request.POST.get('birthdate')
        User.objects.create(first_name=firstName, last_name=lastName, email=email, username=userName, password=hashed_password, birthdate=birthDate)
        user = User.objects.last()
        return redirect ('success', id=user.id)

def success(request, id):
    context = {
        'user': User.objects.get(id=id)
    }
    return render(request, "success.html", context)

def login(request):
    if request.method == "POST":

        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/")

        user = User.objects.get(email=request.POST['loginEmail'])
        if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            print("User Password Matches")
            request.session["id"]=user.id
            request.session["first_name"]=user.first_name
            return redirect("/rebase/home")
        else:
            print("User Password Match Fails")
            return redirect("/")

