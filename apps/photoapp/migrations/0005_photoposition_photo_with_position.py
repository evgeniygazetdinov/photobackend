# Generated by Django 2.0.5 on 2020-06-23 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photoapp', '0004_auto_20200623_1019'),
    ]

    operations = [
        migrations.AddField(
            model_name='photoposition',
            name='photo_with_position',
            field=models.ManyToManyField(to='photoapp.Photo'),
        ),
    ]