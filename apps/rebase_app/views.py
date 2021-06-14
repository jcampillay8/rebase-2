from django.shortcuts import render, redirect
from apps.login_register.models import User
from apps.rebase_app.models import Text, Sentence
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from google_trans_new import google_translator
from django.contrib import messages
from apps.rebase_app.forms import ContactForm
from django.core.mail import EmailMessage, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
import random
import pyttsx3

# Home
def home(request):
    return render(request, 'rebase/home.html')

def users(request):
    text_list = Text.objects.all()
    page = request.GET.get('page',1)
    paginator = Paginator(text_list,5)
    try:
        textos = paginator.page(page)
    except PageNotAnInteger:
        textos = paginator.page(1)
    except EmptyPage:
        textos = paginator.page(paginator.num_pages)
    context = {
        'user': User.objects.get(id=request.session['id']),
        'textos': textos
    }
    return render(request, "rebase/users.html", context)

def logout(request):
    if request.method == 'POST':
        request.session.clear()
        return redirect('/')
    else:
        return redirect('/')


def add_text(request):
    
    return render(request, 'rebase/add_text.html')

def add_text2(request):
    errors = Text.objects.add_text_validator(request.POST)

    if(len(errors)):
        for tag, error in errors.items():
            messages.error(request, error, extra_tags=tag)
        return redirect('add_text')

    if request.method == 'POST':
        thisUser = User.objects.get(id=request.session['id'])
        print(request.session['id'])
        recoger_texto = request.POST['add_text']
        
        recoger_texto1=recoger_texto.replace(' “ ',' " ')
        recoger_texto2=recoger_texto1.replace('”','"')
        recoger_texto3=recoger_texto2.replace("’","'")
        recoger_texto4=recoger_texto3.replace("•","*")
        recoger_texto5=recoger_texto4.replace("—","--")
        recoger_texto6=recoger_texto5.replace(":",".")
        
        print(recoger_texto6.strip('\n'))
        # print("####")
        print(recoger_texto6.lstrip())
        # print("####")
        print(recoger_texto6.rstrip())

        newText = Text.objects.create(
            content = recoger_texto6,
            text_name = request.POST['text_name'],
            user = thisUser,
            contador = 0,
        )
        newText.save()
    
    
    return redirect('/rebase/success2')

def delete(request, textId):
    Text.objects.get(id=textId).delete()

    return redirect('/rebase/users')

def success2(request):
    context = {
        'user': User.objects.get(id=request.session['id']),
    }
    return render(request, "rebase/success2.html", context)



def read(request):
    text_list = Text.objects.all()
    page = request.GET.get('page',1)
    paginator = Paginator(text_list,5)
    try:
        textos = paginator.page(page)
    except PageNotAnInteger:
        textos = paginator.page(1)
    except EmptyPage:
        textos = paginator.page(paginator.num_pages)

    context = {
        'user': User.objects.get(id=request.session['id']),
        'textos': textos
    }
    return render(request, 'rebase/read.html', context)

def read2(request, text_id):
    book = Text.objects.get(id=text_id).content
    line=book.split(".")
    contador=Text.objects.get(id=text_id).contador
    context ={
        'book': Text.objects.get(id=text_id),
        'text_name': Text.objects.get(id=text_id).text_name,
        'content':  line[contador],
        'contador': contador,
        'contenido':'',
    }

    return render(request, 'rebase/read2.html', context)

def add_new_sentence(request, text_id):
    errors = Sentence.objects.add_sentence_validator(request.POST, request.session["id"])

    if(len(errors)):
        for tag, error in errors.items():
            messages.error(request, error, extra_tags=tag)
        return redirect('read2', text_id)
    
    else:
        thisUser = User.objects.get(id=request.session['id'])
        
        newSentence = Sentence.objects.create(
            frase = request.POST.get('new_sentence'),
            valor_frase = 10,
            user_frase = thisUser,
        )
        newSentence.save()

        book = Text.objects.get(id=text_id).content    
        line=book.split(".")    
        cont = Text.objects.get(id=text_id)
        cont.contador=int(request.POST['contador'])
        cont.save()
        contador=Text.objects.get(id=text_id).contador
        frase = request.POST['new_sentence']

        linea_Eng = line[contador]
        context ={
            'book': Text.objects.get(id=text_id),
            'text_name': Text.objects.get(id=text_id).text_name,
            'content':  line[contador],
            'contador': contador,
            'contenido': '',
            'frase': frase,
        }
        return render(request, 'rebase/read_add.html', context)    

def next(request, text_id):
    print('hello there')
    book = Text.objects.get(id=text_id).content
    
    line=book.split(".")
    
    cont = Text.objects.get(id=text_id)
    cont.contador=int(request.POST['contador'])+1
    cont.save()
    contador=Text.objects.get(id=text_id).contador
    if (len(line)-contador) >=1:
        context ={
            'book': Text.objects.get(id=text_id),
            'text_name': Text.objects.get(id=text_id).text_name,
            'content':  line[contador],
            'contador': contador,
            'contenido': '',
        }
        # print(Text.objects.get(id=text_id).content)
        return render(request, 'rebase/read2.html', context)
    else:
        context ={
            'book': Text.objects.get(id=text_id),
            'text_name': Text.objects.get(id=text_id).text_name,
            'content':  "END OF TEXT, CONGRATULATION",
            'contador': contador,
            'contenido': '',
        }
        # print(Text.objects.get(id=text_id).content)
        return render(request, 'rebase/read2.html', context)

def next_line(request):
    # user = User.objects.get(id=request.session["id"])
    # current_sentences =Sentence.objects.filter(user_frase=user)
    # text_id = 1

    return redirect ('/next',text_id=1)

def previous(request, text_id):
    
    book = Text.objects.get(id=text_id).content
    
    line=book.split(".")
    
    cont = Text.objects.get(id=text_id)
    cont.contador=int(request.POST['contador'])-1
    cont.save()
    contador=Text.objects.get(id=text_id).contador
    if (len(line)-contador) >=1:
        context ={
            'book': Text.objects.get(id=text_id),
            'text_name': Text.objects.get(id=text_id).text_name,
            'content':  line[contador],
            'contador': contador,
            'contenido': '',
        }
        # print(Text.objects.get(id=text_id).content)
        return render(request, 'rebase/read2.html', context)
    else:
        context ={
            'book': Text.objects.get(id=text_id),
            'text_name': Text.objects.get(id=text_id).text_name,
            'content':  "END OF TEXT, CONGRATULATION",
            'contador': contador,
            'contenido': '',
        }
        # print(Text.objects.get(id=text_id).content)
        return render(request, 'rebase/read2.html', context)

def translate(request, text_id):
    
    book = Text.objects.get(id=text_id).content
    
    line=book.split(".")
    
    cont = Text.objects.get(id=text_id)
    cont.contador=int(request.POST['contador'])
    cont.save()
    contador=Text.objects.get(id=text_id).contador
    linea_Eng = line[contador]
    translator=google_translator()
    translation=translator.translate(linea_Eng,lang_src="en", lang_tgt="es")
    context ={
        'book': Text.objects.get(id=text_id),
        'text_name': Text.objects.get(id=text_id).text_name,
        'content':  line[contador],
        'contador': contador,
        'contenido': translation,
    }
    # print(Text.objects.get(id=text_id).content)
    return render(request, 'rebase/read2.html', context)


#--------------------- Frase -------------------------------


def phrase(request):
    user = User.objects.get(id=request.session["id"])
    current_sentences =Sentence.objects.filter(user_frase=user)
    
    list_current_sentences =[]
    for i in current_sentences:
        list_current_sentences.append(i.frase)
        print(i.frase)

    list_current_nivel_senteces=[]
    for j in current_sentences:
        list_current_nivel_senteces.append(j.valor_frase)
        print(j.valor_frase)    
    
    aleatorio_1 = random.randint(0,len(list_current_sentences)-1)
    aleatorio_2 = random.randint(0,len(list_current_sentences)-1)
    if list_current_nivel_senteces[aleatorio_1] >= list_current_nivel_senteces[aleatorio_2]:
        aleatorio_win=aleatorio_1
    else:
        aleatorio_win=aleatorio_2
    print(' ')
    print(list_current_sentences[aleatorio_1])
    print(list_current_nivel_senteces[aleatorio_1])
    print("###########")
    print(list_current_sentences[aleatorio_2])
    print(list_current_nivel_senteces[aleatorio_2])

    linea_Eng=list_current_sentences[aleatorio_win]
    translator=google_translator()
    translation=translator.translate(linea_Eng,lang_src="en", lang_tgt="es")

    nivel_sentce = list_current_nivel_senteces[aleatorio_win]
    context={
        
        'contador': aleatorio_win,
        'text_esp':translation,
        'nivel': nivel_sentce,
        'english_sentence': ' ',
    }
    return render(request, 'rebase/phrase.html', context)

def listen(request):
    user = User.objects.get(id=request.session["id"])
    current_sentences =Sentence.objects.filter(user_frase=user)
    
    list_current_sentences =[]
    for i in current_sentences:
        list_current_sentences.append(i.frase)
        print(i.frase)

    list_current_nivel_senteces=[]
    for j in current_sentences:
        list_current_nivel_senteces.append(j.valor_frase)
        
    aleatorio_1 = int(request.POST['contador'])
    linea_Eng=list_current_sentences[aleatorio_1]
    translator=google_translator()
    translation=translator.translate(linea_Eng,lang_src="en", lang_tgt="es")

    nivel_sentce = list_current_nivel_senteces[aleatorio_1]
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[1].id)
    engine.setProperty("rate", 120)
    engine.say(linea_Eng)
    engine.runAndWait()
    context={
        
        'contador': aleatorio_1,
        'text_esp':translation,
        'nivel': nivel_sentce,
        'english_sentence': ' ',
    }
    return render(request, 'rebase/phrase.html', context)

def phrase2(request):
    user = User.objects.get(id=request.session["id"])
    current_sentences =Sentence.objects.filter(user_frase=user)
    
    list_current_sentences =[]
    for i in current_sentences:
        list_current_sentences.append(i.frase)

    list_current_nivel_senteces=[]
    for j in current_sentences:
        list_current_nivel_senteces.append(j.valor_frase)

    list_id = []
    for l in current_sentences:
        list_id.append(l.id)

    
    indice_sentencia = int(request.POST['contador'])
    linea_Eng=list_current_sentences[indice_sentencia]
    translator=google_translator()
    translation=translator.translate(linea_Eng,lang_src="en", lang_tgt="es")

    nivel_sentce = list_current_nivel_senteces[indice_sentencia]
    
    if (str(request.POST['answer_sentence'])).lower()== linea_Eng.lower():
        answer = 'correcto'
        frase = Sentence.objects.get(id=list_id[indice_sentencia])
        frase.valor_frase= list_current_nivel_senteces[indice_sentencia]-1
        frase.save()
        nivel_sentce = list_current_nivel_senteces[indice_sentencia]-1
    else:
        answer = 'incorrecto'
        frase = Sentence.objects.get(id=list_id[indice_sentencia])
        frase.valor_frase= list_current_nivel_senteces[indice_sentencia]+1
        frase.save()
        nivel_sentce = list_current_nivel_senteces[indice_sentencia]+1

    context={
        
        'contador': indice_sentencia,
        'text_esp':translation,
        'nivel': nivel_sentce,
        'english_sentence': linea_Eng,
        'answer':answer,
        'respuesta': request.POST['answer_sentence'],
    }

    return render(request, 'rebase/phrase2.html', context)

def delete_sentence(request):
    user = User.objects.get(id=request.session["id"])
    current_sentences =Sentence.objects.filter(user_frase=user)
    
    list_current_sentences =[]
    for i in current_sentences:
        list_current_sentences.append(i.frase)

    list_id=[]
    for j in current_sentences:
        list_id.append(j.id)
        print(j.id)    
    
    indice_sentencia = int(request.POST['contador'])
    linea_Eng=list_current_sentences[indice_sentencia]
    translator=google_translator()
    translation=translator.translate(linea_Eng,lang_src="en", lang_tgt="es")

    identification = list_id[indice_sentencia]
    
    context={
        'contador': indice_sentencia,
        'text_esp':translation,
        'identification': identification,
        'english_sentence': linea_Eng,
    }

    return render(request,('rebase/delete_sentence.html'), context)

def delete2(request, textId):
    Sentence.objects.get(id=textId).delete()
    return redirect('/rebase/phrase')

def video(request):
    return render(request, 'rebase/video.html')

def contact(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                print('correo')
                mensaje=EmailMessage(subject, message, from_email, to=['jcampillayworks@gmail.com'])
                mensaje.send()
            except BadHeaderError:
                return HttResponse('Invalid header found')
            return redirect('thankyou')
        print('correo2')
    return render(request, 'rebase/contact.html', {'form':form})

def thankyou(request):
    print('how close')
    return render(request,'rebase/thankyou.html')