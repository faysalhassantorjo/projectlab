from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Project)
admin.site.register(project_studnet)
admin.site.register(Category)
admin.site.register(Dataset)
admin.site.register(DatasetDownloadHistory)
admin.site.register(News)