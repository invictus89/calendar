# Generated by Django 2.2.2 on 2019-06-21 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cal', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='uploaded_at',
            field=models.DateTimeField(blank=True),
        ),
    ]