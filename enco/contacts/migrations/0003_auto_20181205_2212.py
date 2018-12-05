# Generated by Django 2.1.4 on 2018-12-05 21:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0002_auto_20181205_2154'),
    ]

    operations = [
        migrations.CreateModel(
            name='Colaborator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='colaborators', to='contacts.Company')),
            ],
        ),
        migrations.RemoveField(
            model_name='person',
            name='company',
        ),
        migrations.DeleteModel(
            name='Person',
        ),
    ]
