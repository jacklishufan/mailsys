# Generated by Django 2.2.4 on 2020-04-10 12:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0005_auto_20200410_0908'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loginactivity',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.User'),
        ),
    ]
