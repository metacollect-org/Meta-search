# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings

STATUS = (
    (0, 'Inactive'),
    (1, 'Active'),
    (2, 'In Progress'),
    (3, 'Unspecified'),
)

KINDS = (
    (0, 'Website'),
    (1, 'App'),
    (2, 'Map'),
    (3, 'Facebook'),
    (4, 'Unspecified'),
)

#PROGRAMMING_LANGUAGES = (
    #(0, 'Python'),
    #(1, 'Unspecified'),
#)
#English,
# German,
# French,
# Arab,
# Pashto,
# Persian,
# Tigrinya,
# Srpski,
# српски,
# Albanian,
# македонски
class PageLanguage(models.Model):
    #ENGLISH = 'en', # english
    #GERMAN = 'de', # deutsch
    #FRENCH = 'fr', # french
    #ARABIC = 'ar', # arabic
    #FARSI = 'fa', # farsi/persian
    #(6, 'mk'), # македонски
    #(7, 'ps'), # pashto
    #(8, 'ti'), # Tigrinya
    #(9, 'sr'), # Srpski (Serbisch) (српски)
    #(10, 'sq'), # shqip, Albanien
    #(11, 'Unspecified'),
    name = models.CharField(max_length=200)
    abbreviation = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.name;

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)
    parent = models.ForeignKey('self', null=True, blank=True)
    def __str__(self):
        return self.name

class ProgrammingLanguage(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField()
    kind = models.IntegerField(choices=KINDS) # multiple
    organisation_name = models.CharField(max_length=200, null=True, blank=True)
    categories = models.ManyToManyField(Category)
    description = models.TextField()
    area_country = models.CharField(max_length=200, null=True, blank=True)
    area_state = models.CharField(max_length=200, null=True, blank=True) # bundesland
    area_city = models.CharField(max_length=200, null=True, blank=True)
    status = models.IntegerField(choices=STATUS)
    logo = models.URLField(null=True, blank=True)
    contact_socialmedia = models.URLField(null=True, blank=True) # comma separated
    contact_telephone = models.CharField(max_length=200, null=True, blank=True) # comma separated
    contact_address_street = models.CharField(max_length=200, null=True, blank=True)
    contact_address_housenr = models.CharField(max_length=20, null=True, blank=True)
    contact_address_zip = models.CharField(max_length=20, null=True, blank=True)
    contact_address_city = models.CharField(max_length=200, null=True, blank=True)
    contact_address_country = models.CharField(max_length=200, null=True, blank=True)
    languages = models.ManyToManyField(PageLanguage) # multiple
    needs = models.CharField(max_length=200, null=True, blank=True) # optional
    programming_languages = models.ManyToManyField(ProgrammingLanguage, blank=True)

    def __str__(self):
        return self.title

    def is_online(self):
        return self.status==1
