# Generated by Django 2.1.4 on 2018-12-18 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_auto_20181218_1348'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='internal_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]