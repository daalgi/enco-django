from django.db import models
from contacts.models import Company


class Contract(models.Model):
    created = models.DateField(auto_now_add=True)
    internal_id = models.PositiveIntegerField(blank=True, null=True)    
    #status = models.CharField(max_length=20, default='negotiation')
    provider = models.ForeignKey(Company, related_name='provider', on_delete=models.CASCADE)
    client = models.ForeignKey(Company, related_name='client', on_delete=models.CASCADE)
    # contacts...
    signed = models.DateField(default=None, null=True, blank=True)  
    deadline = models.DateField(default=None, null=True, blank=True)
    def __str__(self):
        if self.signed is not None:
            return (f'{self.provider.name} #{self.internal_id} - Signed: {str(self.created)}, Client: {self.client}')
        else:
            return (f'{self.provider.name} #{self.internal_id} - Created: {str(self.created)}, Client: {self.client}')

    def save(self, *args, **kwargs):
        if self.internal_id is None:
            last_internal_id = Contract.objects.filter(provider=self.provider).aggregate(max_id=models.Max('internal_id')).get('max_id', 0)
            if last_internal_id is None:
                self.internal_id = 1  
            else:
                self.internal_id = last_internal_id + 1
        super().save(*args, **kwargs)


class Project(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    internal_id = models.PositiveIntegerField(blank=True, null=True)
    name = models.CharField(max_length=50)
    country = models.CharField(max_length=30)

    def __str__(self):
        return (f"{self.internal_id} - {self.name} ({self.country})")

    def save(self, *args, **kwargs):
        if self.internal_id is None:
            last_internal_id = Project.objects.filter(contract__provider=self.contract.provider).aggregate(max_id=models.Max('internal_id')).get('max_id', 0)
            if last_internal_id is None:
                self.internal_id = 1  
            else:
                self.internal_id = last_internal_id + 1
        super().save(*args, **kwargs)


class Stage(models.Model):
    project = models.ForeignKey(Project, related_name='stages', on_delete=models.CASCADE)
    internal_id = models.PositiveIntegerField(blank=True, null=True)
    name = models.CharField(max_length=50, blank=True)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.project.contract.provider.name} - P{self.project.internal_id} - S{self.internal_id} {self.name}"

    def save(self, *args, **kwargs):
        if self.internal_id is None:
            last_internal_id = Stage.objects.filter(project=self.project).aggregate(max_id=models.Max('internal_id')).get('max_id', 0)
            if last_internal_id is None:
                self.internal_id = 1  
            else:
                self.internal_id = last_internal_id + 1
        super().save(*args, **kwargs)


class ScopeType(models.Model):
    name = models.CharField(max_length=30, default='Pre-design')
    def __str__(self):
        return f"{self.name}"


class TaskType(models.Model):
    name = models.CharField(max_length=30, default='Shallow foundation')
    def __str__(self):
        return f"{self.name}"
        

class Task(models.Model):
    stage = models.ForeignKey(Stage, related_name='tasks', on_delete=models.CASCADE)
    internal_id = models.PositiveIntegerField(blank=True, null=True)
    scope = models.ForeignKey(ScopeType, related_name='+', on_delete=models.CASCADE)
    task_type = models.ForeignKey(TaskType, related_name='+', on_delete=models.CASCADE)
    description = models.CharField(max_length=50, default='', blank=True)
    deadline = models.DateField()

    def __str__(self):
        return f'{self.stage}.{self.internal_id} - {self.task_type}'

    def save(self, *args, **kwargs):
        if self.internal_id is None:
            last_internal_id = Task.objects.filter(stage=self.stage).aggregate(max_id=models.Max('internal_id')).get('max_id', 0)
            if last_internal_id is None:
                self.internal_id = 1  
            else:
                self.internal_id = last_internal_id + 1
        super().save(*args, **kwargs)

class Revision(models.Model):
    task = models.ForeignKey(Task, related_name='revisions', on_delete=models.CASCADE)
    internal_id = models.PositiveIntegerField(blank=True, null=True)
    comments = models.TextField(max_length=300, blank=True)

    def save(self, *args, **kwargs):
        if self.internal_id is None:
            last_internal_id = Revision.objects.filter(task=self.task).aggregate(max_id=models.Max('internal_id')).get('max_id', 0)
            if last_internal_id is None:
                self.internal_id = 0  
            else:
                self.internal_id = last_internal_id + 1
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.task} - Rev.{self.internal_id}'
