# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0003_auto_20151009_2237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignmentsubmission',
            name='pull_request',
            field=models.URLField(blank=True, null=True),
        ),
    ]
