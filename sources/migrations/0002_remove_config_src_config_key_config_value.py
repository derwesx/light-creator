# Generated by Django 4.0.3 on 2022-05-08 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sources', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='config',
            name='src',
        ),
        migrations.AddField(
            model_name='config',
            name='key',
            field=models.CharField(default='conf', max_length=128),
        ),
        migrations.AddField(
            model_name='config',
            name='value',
            field=models.CharField(default='val', max_length=131072),
        ),
    ]
