# Generated by Django 2.0.5 on 2020-06-24 03:37

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('photoapp', '0012_auto_20200624_0336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadlist',
            name='pub_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]