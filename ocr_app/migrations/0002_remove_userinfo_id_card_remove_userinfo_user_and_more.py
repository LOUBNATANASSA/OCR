# Generated by Django 5.0.5 on 2024-08-14 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ocr_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinfo',
            name='id_card',
        ),
        migrations.RemoveField(
            model_name='userinfo',
            name='user',
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='date_naissance',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='id',
            field=models.CharField(max_length=20, primary_key=True, serialize=False, unique=True),
        ),
    ]
