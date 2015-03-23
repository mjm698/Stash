# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polymer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='content',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
    ]
