from django.contrib import admin
from projects.models import Contract, Project, DesignSituation, Task, Revision

admin.site.register(Contract)
admin.site.register(Project)
admin.site.register(DesignSituation)
admin.site.register(Task)
admin.site.register(Revision)
