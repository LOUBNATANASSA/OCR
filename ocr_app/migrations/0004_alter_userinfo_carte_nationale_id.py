# Generated by Django 5.0.5 on 2024-08-14 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ocr_app', '0003_userinfo_carte_nationale_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='carte_nationale_id',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]