# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('time', models.DateTimeField(verbose_name=b'date commented')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('link', models.CharField(max_length=200)),
                ('time', models.DateTimeField(verbose_name=b'date added')),
                ('updateTime', models.DateTimeField(verbose_name=b'date updated')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Stash',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('time', models.DateTimeField(verbose_name=b'date created')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.IntegerField(default=1, choices=[(1, b'New'), (2, b'Viewed'), (3, b'Updated'), (4, b'Archived')])),
                ('content', models.ForeignKey(to='polymer.Content')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=75)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='status',
            name='user',
            field=models.ForeignKey(to='polymer.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='stash',
            name='owner',
            field=models.ForeignKey(related_name='owner', to='polymer.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='stash',
            name='users',
            field=models.ManyToManyField(to='polymer.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='content',
            name='stash',
            field=models.ForeignKey(to='polymer.Stash'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='content',
            name='user',
            field=models.ForeignKey(to='polymer.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='content',
            field=models.ForeignKey(to='polymer.Content'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(to='polymer.User'),
            preserve_default=True,
        ),
    ]
