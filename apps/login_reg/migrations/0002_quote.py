# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-10-24 18:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login_reg', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=255)),
                ('author', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('favorites', models.ManyToManyField(default=None, related_name='favorites', to='login_reg.User')),
                ('poster', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='authored_quotes', to='login_reg.User')),
            ],
        ),
    ]
