# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organisation',
            name='status',
            field=models.IntegerField(choices=[(0, 'Offline'), (1, 'Online'), (2, 'In Progress')]),
        ),
    ]
