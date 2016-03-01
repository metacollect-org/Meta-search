from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Project, Category, ProgrammingLanguage, Kind, PageLanguage, GeoLocation

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

class GeoLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeoLocation

class ProjectSerializer(serializers.ModelSerializer):
    kind = KindSerializer(many=True, read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    languages = PageLanguageSerializer(many=True, read_only=True)
    programming_languages = ProgrammingLanguageSerializer(many=True, read_only=True)
    geo_location = GeoLocationSerializer(read_only=True)
    contact_loc = GeoLocationSerializer(read_only=True)
    class Meta:
        model = Project
        # fields = [] # Excluding updated_at and created_at as the property 'auto_now_add=True' makes them read-only, resulting in an error when adding them to this form.
        # for f in Project._meta.get_fields():
        #     fields.append(f.name)

