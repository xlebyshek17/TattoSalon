# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-10-13 21:01
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('salon', '0007_auto_20191006_2150'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('phone', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=255)),
                ('buying_type', models.CharField(choices=[('Самовывоз', 'Самовывоз'), ('Доставка', 'Доставка')], max_length=40)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('comments', models.TextField()),
                ('status', models.CharField(choices=[('Принят в обработку', 'Принят в обработку'), ('Выполняется', 'выполняется'), ('Оплачен', 'Оплачен')], max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='cart',
            name='items',
            field=models.ManyToManyField(blank=True, to='salon.CartItem'),
        ),
        migrations.AddField(
            model_name='ord',
            name='items',
            field=models.ManyToManyField(to='salon.Cart'),
        ),
        migrations.AddField(
            model_name='ord',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
