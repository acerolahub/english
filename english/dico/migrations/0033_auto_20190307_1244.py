# Generated by Django 2.1.5 on 2019-03-07 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dico', '0032_auto_20190307_0154'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(max_length=30)),
                ('first_name', models.CharField(max_length=30)),
                ('email', models.EmailField(default=False, max_length=254)),
                ('password', models.CharField(max_length=50)),
                ('password2', models.CharField(max_length=50)),
            ],
        ),
        migrations.RemoveField(
            model_name='score',
            name='username',
        ),
    ]
