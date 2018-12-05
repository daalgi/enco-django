from django.db import models
from contacts.models import Company


class Contract(models.Model):
    created = models.DateField(auto_now_add=True)
    #status = models.CharField(max_length=20, default='negotiation')
    provider = models.ForeignKey(Company, related_name='provider', on_delete=models.CASCADE)
    client = models.ForeignKey(Company, related_name='client', on_delete=models.CASCADE)
    # contacts...
    signed = models.DateField(default=None, blank=True)  
    deadline = models.DateField(default=None, blank=True)
    def __str__(self):
        if self.signed is not None:
            return (f'Signed: {str(self.signed)}, Client: {self.client}')
        else:
            return (f'Created: {str(self.created)}, Client: {self.client}')

class Project(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    internal_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=50)
    country = models.CharField(max_length=30)

    def __str__(self):
        return (f"{self.internal_id} - {self.name} ({self.country})")

class DesignSituation(models.Model):
    project = models.ForeignKey(Project, related_name='design_situations', on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.design_situation.project.internal_id}'

class Task(models.Model):
    design_situation = models.ForeignKey(DesignSituation, related_name='tasks', on_delete=models.CASCADE)
    scope = models.CharField(max_length=30)
    deadline = models.DateField()

    def __str__(self):
        return f'{self.design_situation.project.internal_id}.{self.pk}'

class Revision(models.Model):
    task = models.ForeignKey(Task, related_name='revisions', on_delete=models.CASCADE)
    comments = models.TextField(max_length=300, blank=True)
    
