# Generated by Django 3.0.8 on 2020-09-04 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_post_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]