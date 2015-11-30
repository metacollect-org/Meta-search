from django.db import models

STATUS = (
    (0, 'Offline'),
    (1, 'Online'),
    (2, 'In Progress'),
)

# Create your models here.
class Organisation(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField()
    kind = models.CharField(max_length=200)
    area = models.CharField(max_length=200)
    status = models.IntegerField(choices=STATUS)
    description = models.TextField()

    def __str__(self):
        return self.title

    def is_online(self):
        return self.status==1
