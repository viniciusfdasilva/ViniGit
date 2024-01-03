from django.db import models

class Repository(models.Model):
    
    name = models.CharField(max_length=64)
    
    class Meta:
        verbose_name = 'Repository'
        db_table = 'repository'
        
class Release(models.Model):
    release_name = models.CharField(max_length=100)
    description  = models.TextField()
    changelog    = models.TextField()
    repository   = models.ForeignKey(Repository, on_delete=models.SET_NULL)
    
    class Meta:
        verbose_name = 'release'
        db_table     = 'release'
        
class PullRequest(models.Model):
    
    title       = models.CharField(max_length=64)
    description = models.TextField()
    is_merged   = models.BooleanField()
    repository  = models.ForeignKey(Repository, on_delete=models.SET_NULL)
    to_branch   = models.CharField(max_length=100)
    from_branch = models.CharField(max_length=100)
    
    class Meta:
        verbose_name = 'PullRequest'
        db_table = 'pull_request'
    

