# Generated by Django 4.2.6 on 2023-10-23 03:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shortend_url',
            name='no_of_visitor',
            field=models.IntegerField(null=True),
        ),
    ]