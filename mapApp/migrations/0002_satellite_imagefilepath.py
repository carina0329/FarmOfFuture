# Generated by Django 4.1.7 on 2023-03-27 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mapApp", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="satellite",
            name="ImageFilePath",
            field=models.CharField(default="", max_length=500),
        ),
    ]
