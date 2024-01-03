import os, environ
from vinigit.settings import BASE_DIR
from git.models import Repository

class GitManager():
    
    def git_push(git_dir, branch):
        os.chdir(f'{git_dir}') 
        return os.system(f'git push origin {branch}')
        
    def git_clone(git_url, dst_clone):
        return os.system(f'git clone {git_url} {dst_clone}')
    
    def git_merge(git_url, from_branch, to_branch, message=None):
        
        clone_result = GitManager.git_clone(git_url, '/tmp/')
        
        if clone_result and clone_result == 0:
            
            rep_name = git_url.split('/')[-1].replace('.git', '')
            os.chdir(f'/tmp/{rep_name}')        
            return os.system(f'git merge {from_branch} {to_branch}')
        
        return None
    
class RepositoryManager():
    
    def remove_dir(dir_path):
        return os.system(f'rm -r {dir_path}')
    
    def remove_repository(id):
        env = environ.Env()
        environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
        
        rep = Repository.objects.get(pk=id)
        
        try:
            if rep:
                
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
    
                directory = f'{env("GIT_PATH")}/{input_value}.{env("REPO_EXTENTION")}'

                os.makedirs(directory, mode=500)
                os.chdir(directory)
                os.system('git init --bare')

                Repository(nome=input_value).save()

                return True, False
        except OSError as e:
            return False, False
