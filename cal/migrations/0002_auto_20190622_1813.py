# Generated by Django 2.2.2 on 2019-06-22 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cal', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='title_type',
            field=models.CharField(max_length=50),
        ),
    ]