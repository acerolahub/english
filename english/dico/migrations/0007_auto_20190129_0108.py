# Generated by Django 2.1.5 on 2019-01-29 01:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dico', '0006_auto_20190128_1720'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='word',
            name='synonym',
        ),
        migrations.AddField(
            model_name='word',
            name='synonym',
            field=models.ManyToManyField(null=True, to='dico.Wordnym'),
        ),
    ]
