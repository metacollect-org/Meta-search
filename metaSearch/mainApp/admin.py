from django.contrib import admin

from .models import Organisation
# Register your models here.

class OrganisationAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'is_online')

admin.site.register(Organisation, OrganisationAdmin)
