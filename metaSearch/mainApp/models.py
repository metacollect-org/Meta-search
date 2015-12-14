from django.db import models

STATUS = (
    (0, 'Inactive'),
    (1, 'Active'),
    (2, 'In Progress'),
)

KINDS = (
    (0, 'Website'),
    (1, 'App'),
    (2, 'Map'),
    (3, 'Facebook'),
)

PROGRAMMING_LANGUAGES = (
    (0, 'Python'),
)

PAGE_LANGUAGES = (
    (0, 'en'),
)

# Create your models here.
class Project(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField()
    kind = models.IntegerField(choices=KINDS) # multiple
    organisation_name = models.CharField(max_length=200)
    categories = models.IntegerField() # tag field; id references one or more categories;
    description = models.TextField()
    area_country = models.CharField(max_length=200)
    area_state = models.CharField(max_length=200) # bundesland
    area_city = models.CharField(max_length=200)
    status = models.IntegerField(choices=STATUS)
    logo = models.FileField(upload_to='uploads/') # maybe better to use URL
    contact_socialmedia = models.URLField() # comma separated
    contact_telephone = models.CharField(max_length=200) # comma separated
    contact_address_street = models.CharField(max_length=200)
    contact_address_housenr = models.CharField(max_length=20)
    contact_address_zip = models.CharField(max_length=20)
    contact_address_city = models.CharField(max_length=200)
    contact_address_country = models.CharField(max_length=200)
    languages = models.IntegerField(choices=PAGE_LANGUAGES) # multiple
    needs = models.CharField(max_length=200) # optional
    programming_language = models.IntegerField(choices=PROGRAMMING_LANGUAGES) # multiple

    def __str__(self):
        return self.title

    def is_online(self):
        return self.status==1
