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
from git.models import Repository

class LogoutView(ListView):
    template_name = 'auth/login.html'
    model = User

    def get(self, request):

        logout(request=request)
        return redirect('/git/')
        #return render(request, self.template_name)


class LoginView(ListView):
    template_name = 'auth/login.html'
    model = User
    
    def get(self, request):
        repositorio = Repository.objects.all()

        form = UserForm()
      
        if request.user.is_authenticated:
            #return HttpResponseRedirect(reverse('/git/painel'))
            return render(request, 'painel.html', {'username': request.user.username, "repositorios": repositorio})

        return render(request, self.template_name, {'form': form})


    def post(self, request):

        form = UserForm()
       
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if User.objects.all().count() > 0:

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

                return redirect('/git/painel')

        messages.info(request,'Credenciais incorretas')
        return render(request, self.template_name, {'form': form})


class PainelView(ListView):
    template_name = 'painel.html'

    def get(self, request):

        repositorio = Repository.objects.all()
        context = {'username': request.user.username, "repositorios": repositorio}
       
        return render(request, self.template_name, context)

    def post(self, request):
        name = request.POST.get('id')
        repo = request.POST.get('id_repo')
        repositorio = Repository.objects.all()

        env = environ.Env()
        environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

        if name is None and repo is None:    

            input_value = request.POST.get('value')

            print(f'[82] PASSOU POR AQUI {input_value}')
            status, is_pupkey = RepositoryManager.new_repository(input_value)

            url = f'{env("GIT_USER")}@{env("DOMAIN")}:{env("GIT_PATH")}/{input_value}.{env("REPO_EXTENTION")}'

            if status and is_pupkey:

                messages.info(request,'Chave pública adicionada com sucesso!')
                return render(request, self.template_name, {'username': request.user.username, "repositorios": repositorio})

            elif status and not is_pupkey:  

                context = {'url': url, 'username': request.user.username, "repositorios": repositorio}

                return render(request, self.template_name, context)

            else:
            
                messages.info(request,'Erro no processo!')
                return render(request, self.template_name, {'username': request.user.username, "repositorios": repositorio})
        
        elif repo is not None and name is None:
        
            RepositoryManager.remove_repository(repo)
            return HttpResponse('Repositório removido com sucesso!')
        else:

            url = f'{env("GIT_USER")}@{env("DOMAIN")}:{env("GIT_PATH")}/{name}.{env("REPO_EXTENTION")}'
            return HttpResponse(url)
            
# Create your views here.
