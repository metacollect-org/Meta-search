from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Project, Category, ProgrammingLanguage, Kind, PageLanguage

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        # fields = [] # Excluding updated_at and created_at as the property 'auto_now_add=True' makes them read-only, resulting in an error when adding them to this form.
        # for f in Project._meta.get_fields():
        #     fields.append(f.name)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category

class PageLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageLanguage

class KindSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kind

class ProgrammingLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgrammingLanguage
