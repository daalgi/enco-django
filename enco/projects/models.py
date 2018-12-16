from django.db import models
from contacts.models import Company


def increment_project_id():
    pass

def increment_task_id(stage):
    #https://techstream.org/Web-Development/Custom-Auto-Increment-Field-Django
    last_task = Task.objects.all().filter(stage).last()

def increment_revision_id():
    pass

class Contract(models.Model):
    created = models.DateField(auto_now_add=True)
    #status = models.CharField(max_length=20, default='negotiation')
    provider = models.ForeignKey(Company, related_name='provider', on_delete=models.CASCADE)
    client = models.ForeignKey(Company, related_name='client', on_delete=models.CASCADE)
    # contacts...
    signed = models.DateField(default=None, null=True, blank=True)  
    deadline = models.DateField(default=None, null=True, blank=True)
    def __str__(self):
        if self.signed is not None:
            return (f'Signed: {str(self.signed)}, Client: {self.client}')
        else:
            return (f'Created: {str(self.created)}, Client: {self.client}')


class Project(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    internal_id = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=50)
    country = models.CharField(max_length=30)

    def __str__(self):
        return (f"{self.internal_id} - {self.name} ({self.country})")


class Stage(models.Model):
    project = models.ForeignKey(Project, related_name='stages', on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=True)
    created = models.DateField(auto_now_add=True)
    def __str__(self):
        return f"{self.project.internal_id} - {self.name}"


class ScopeType(models.Model):
    name = models.CharField(max_length=30, default='Pre-design')
    def __str__(self):
        return f"{self.name}"


class TaskType(models.Model):
    name = models.CharField(max_length=30, default='Shallow foundation')
    def __str__(self):
        return f"{self.name}"
        

class Task(models.Model):
    task_id = models.PositiveIntegerField(default=increment_task_id, editable=False)
    stage = models.ForeignKey(Stage, related_name='tasks', on_delete=models.CASCADE)
    scope = models.ForeignKey(ScopeType, related_name='+', on_delete=models.CASCADE)
    task_type = models.ForeignKey(TaskType, related_name='+', on_delete=models.CASCADE)
    description = models.CharField(max_length=50, default='', blank=True)
    deadline = models.DateField()

    def __str__(self):
        return f'{self.stage.project.internal_id}.{self.task_id} - {self.scope} - {self.task_type}'

    @property
    def task_id(self):
        tasks = 



class Revision(models.Model):
    revision_id = models.PositiveIntegerField(default=increment_revision_id)
    task = models.ForeignKey(Task, related_name='revisions', on_delete=models.CASCADE)
    comments = models.TextField(max_length=300, blank=True)
    
    def __str__(self):
        return f'{self.task} - Rev.{self.revision_id}'