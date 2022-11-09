import os, environ
from vinigit.settings import BASE_DIR
from git.models import Repository

class RepositoryManager():
    
    def remove_repository(id):
        env = environ.Env()
        environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
        
        rep = Repository.objects.get(pk=id)
        
        try:
           
            path = f'{env("GIT_PATH")}/{rep.nome}.{env("REPO_EXTENTION")}'
            os.system(f'rm -r {path}')
            rep.delete()
        except OSError as e:
            
            rep.delete()

    def new_repository(input_value):
        env = environ.Env()
        environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

        try:
            if str(input_value).__contains__("ssh-rsa"):

                os.system(f'echo {input_value} >> {env("SSH_PATH")}/{env("SSH_FILE")}')
                return True, True
            else:
                mode = 0o777
                directory = f'{env("GIT_PATH")}/{input_value}.{env("REPO_EXTENTION")}'

                os.makedirs(directory, mode)
                os.chdir(directory)
                os.system('git init --bare')

                Repository(nome=input_value).save()

                return True, False
        except OSError as e:
            return False, False