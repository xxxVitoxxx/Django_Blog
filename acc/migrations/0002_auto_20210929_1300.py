# Generated by Django 3.2.7 on 2021-09-29 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acc', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='website',
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=200),
        ),
    ]
