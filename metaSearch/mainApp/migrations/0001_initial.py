# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Organisation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('url', models.URLField(verbose_name='date published')),
                ('kind', models.CharField(max_length=200)),
                ('area', models.CharField(max_length=200)),
                ('status', models.IntegerField(choices=[(0, 'Offline'), (1, 'Online'), (2, 'In Progress')], max_length=1)),
                ('description', models.TextField()),
            ],
        ),
    ]
