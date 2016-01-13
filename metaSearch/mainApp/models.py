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

PROGRAMMING_LANGUAGES = (
    (0, 'Python'),
    (1, 'Unspecified'),
)
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
PAGE_LANGUAGES = (
    (0, 'en'), # english
    (1, 'de'), # deutsch
    (3, 'fr'), # french
    (4, 'ar'), # arabic
    (5, 'fa'), # farsi/persian
    (6, 'mk'), # македонски
    (7, 'ps'), # pashto
    (8, 'ti'), # Tigrinya
    (9, 'sr'), # Srpski (Serbisch) (српски)
    (10, 'sq'), # shqip, Albanien
    (11, 'Unspecified'),
)

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)

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
    #categories = models.IntegerField() # tag field; id references one or more categories;
    categories = models.ManyToManyField(Category)
    description = models.TextField()
    area_country = models.CharField(max_length=200)
    area_state = models.CharField(max_length=200) # bundesland
    area_city = models.CharField(max_length=200)
    status = models.IntegerField(choices=STATUS)
    #logo = models.FileField(upload_to='mainApp/'+settings.UPLOAD_PATH, null=True, blank=True) # maybe better to use URL
    logo = models.URLField(null=True, blank=True)
    contact_socialmedia = models.URLField(null=True, blank=True) # comma separated
    contact_telephone = models.CharField(max_length=200) # comma separated
    contact_address_street = models.CharField(max_length=200)
    contact_address_housenr = models.CharField(max_length=20)
    contact_address_zip = models.CharField(max_length=20)
    contact_address_city = models.CharField(max_length=200)
    contact_address_country = models.CharField(max_length=200)
    languages = models.IntegerField(choices=PAGE_LANGUAGES) # multiple
    needs = models.CharField(max_length=200, null=True, blank=True) # optional
#    programming_language = models.IntegerField(choices=PROGRAMMING_LANGUAGES, null=True, blank=True) # multiple
    programming_languages = models.ManyToManyField(ProgrammingLanguage)

    def __str__(self):
        return self.title

    def is_online(self):
        return self.status==1
