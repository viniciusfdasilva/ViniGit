import os, environ
from vinigit.settings import BASE_DIR
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from git.managers import RepositoryManager
from git.forms import UserForm

class LogoutView(ListView):
    template_name = 'auth/login.html'
    model = User

    def get(self, request):

        logout(request=request)
        return redirect('/')


class LoginView(ListView):
    template_name = 'auth/login.html'
    model = User
    
    def get(self, request):

        form = UserForm()
      
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('painel'))
            #return render(request, 'index.html', {'username': request.user.username})

        return render(request, self.template_name, {'form': form})


    def post(self, request):

        form = UserForm()
       
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if User.objects.all().count() > 0:

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

                return HttpResponseRedirect(reverse('painel'))

        messages.info(request,'Credenciais incorretas')
        return render(request, self.template_name, {'form': form})


class PainelView(ListView):
    template_name = 'index.html'

    def get(self, request):
        return render(request, self.template_name, {'username': request.user.username})

    def post(self, request):
        env = environ.Env()
        environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

        input_value = request.POST.get('value')
        
        status, is_pupkey = RepositoryManager.new_repository(input_value)

        url = f'{env("GIT_USER")}@{env("DOMAIN")}:{env("GIT_PATH")}/{input_value}.{env("REPO_EXTENTION")}'

        if status and is_pupkey:

            messages.info(request,'Chave pública adicionada com sucesso!')
            return render(request, self.template_name, {'username': request.user.username})

        elif status and not is_pupkey:  
        
            return render(request, self.template_name, {'url': url, 'username': request.user.username})

        else:
        
            messages.info(request,'Erro no processo!')
            return render(request, self.template_name, {'username': request.user.username})

# Create your views here.