from django.shortcuts import render, redirect
from .forms import RessourceForm
from utils.api_youtube import get_metadata
from utils.get_article import get_title, clean_text, tf_idf, get_article_text_goos
from utils.tfidf_pipeline import pipeline_tfidf
from .models import Ressource
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django_q.tasks import AsyncTask


def index(request):
    if request.user.is_authenticated:

        return render(request, 'app_veille/index.html')

    else:
        return redirect('login')

@login_required(login_url='login')
def form_ressource_view(request):
    current_user = request.user
    id_user = current_user.id
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RessourceForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            obj = Ressource()
            obj.lien = form.cleaned_data['lien']
            obj.ressource = form.cleaned_data['ressource']
            obj.user = User.objects.get(id=id_user)

            if str(form.cleaned_data['ressource']) == "Video":
                metadata=get_metadata(form.cleaned_data['lien'])
                obj.titre=metadata['title']
                key_words=metadata['tags']
                str_key_words=' '.join(key_words)
                obj.key_word=str_key_words
                obj.save()
                
            elif str(form.cleaned_data['ressource']) == "Article":
                article_text = get_article_text_goos(form.cleaned_data['lien'])

                article = get_title(form.cleaned_data['lien'])
                obj.titre=article
                obj.corpus = article_text
                obj.save()
                a = AsyncTask('utils.tfidf_pipeline.pipeline_tfidf', id_user)
                a.run()
            
            # redirect to a new URL:
            return redirect('validation')
    else:
        form = RessourceForm()
        return render(request, 'app_veille/form_ressource.html', {'form': form})

@login_required(login_url='login')
def validation(request):
    return render(request, 'app_veille/validation.html')

def login_page(request):

    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password =request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.add_message(request, messages.INFO, 'Login et/ou mot de passe incorrect')
    
        context = {}

        return render(request, 'registration/login.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password =request.POST.get('password')
        password2 = request.POST.get('password2')

        if password == password2:
            user = User.objects.create_user(username=username, password=password)
            user.save()
            return redirect('login')
        else:
            messages.add_message(request, messages.INFO, 'Les mots de passe ne correspondent pas')
        
    context = {}

    return render(request, 'registration/sign_in.html', context=context)