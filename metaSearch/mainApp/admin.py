from django.contrib import admin

from .models import Project
from .models import Category
# Register your models here.

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'is_online')

admin.site.register(Project, ProjectAdmin)
admin.site.register(Category)
