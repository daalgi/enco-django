from django.db import models

#class CompanyGroup(models.Model):
#    pass

class Company(models.Model):
    name = models.CharField(max_length=30)
    country = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.name} ({self.country})'

class Colaborator(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    company = models.ForeignKey(Company, related_name='colaborators', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.company.name})'