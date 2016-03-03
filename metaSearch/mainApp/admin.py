from django.contrib import admin

from .models import Project
from .models import Category
from .models import PageLanguage
from .models import Kind
from guardian.admin import GuardedModelAdmin

# Register your models here.

class ProjectAdmin(GuardedModelAdmin):
    list_display = ('title', 'url', 'is_online')

admin.site.register(Project, ProjectAdmin)
admin.site.register(Category)
admin.site.register(PageLanguage)
admin.site.register(Kind)