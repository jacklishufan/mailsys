# Generated by Django 2.2.4 on 2020-04-10 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0004_auto_20200409_0806'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='passwd',
            field=models.CharField(max_length=20),
        ),
    ]
