from django.forms import ModelForm, CharField
from .models import Project


class JoinForm(ModelForm):
   class Meta:
      model = Project
      fields = []  # Excluding updated_at and created_at as the property 'auto_now_add=True'
      # makes them read-only, resulting in an error when adding them to this form.
      for f in Project._meta.get_fields():
         if f.name != 'updated_at' and f.name != 'created_at' and f.name!='contact_loc' and f.name!='geo_location':
            fields.append(f.name)

   contact_loc = CharField(max_length=200, required=False)
   geo_location = CharField(max_length=200, required=False)
