# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0002_auto_20151127_2132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organisation',
            name='url',
            field=models.URLField(),
        ),
    ]
