# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-25 19:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dispatch', '0010_image_tags'),
    ]

    operations = [
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('question', models.CharField(max_length=255)),
                ('is_open', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='PollAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='dispatch.Poll')),
            ],
        ),
        migrations.CreateModel(
            name='PollVote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='dispatch.PollAnswer')),
            ],
        ),
    ]
