from django.contrib import admin
from projects.models import Contract, Project, Stage, Task, ScopeType, TaskType, Revision

admin.site.register(Contract)
admin.site.register(Project)
admin.site.register(Stage)
admin.site.register(ScopeType)
admin.site.register(TaskType)
admin.site.register(Task)
admin.site.register(Revision)
