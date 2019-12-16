from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from decimal import Decimal
# Create your models here.

from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os

class OverwriteStorage(FileSystemStorage):

    def get_available_name(self, name, max_length=None):
        """Returns a filename that's free on the target storage system, and
        available for new content to be written to.

        Found at http://djangosnippets.org/snippets/976/

        This file storage solves overwrite on upload problem. Another
        proposed solution was to override the save method on the model
        like so (from https://code.djangoproject.com/ticket/11663):

        def save(self, *args, **kwargs):
            try:
                this = MyModelName.objects.get(id=self.id)
                if this.MyImageFieldName != self.MyImageFieldName:
                    this.MyImageFieldName.delete()
            except: pass
            super(MyModelName, self).save(*args, **kwargs)
        """
        # If the filename already exists, remove it as if it was a true file system
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name


class WordTranslate(models.Model):
    username = models.CharField(max_length=1000)
    mot = models.CharField(max_length=100)
    ultimate = models.IntegerField(default=0)

    def __str__(self):
        return self.mot


class Wordnym(models.Model):
    username = models.CharField(max_length=1000)
    mot = models.CharField(max_length=100)
    ultimate = models.IntegerField(default=0)

    def __str__(self):
        return self.mot


class Word(models.Model):
    username = models.CharField(max_length=1000)
    mot = models.CharField(max_length=100)
    comment = models.TextField(null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)
    synonym = models.ManyToManyField(Wordnym, blank=True)
    translate_word = models.ManyToManyField(WordTranslate)
    translate_mot = models.CharField(max_length=100)
    date_challenge = models.DateTimeField(default=timezone.now)
    score_d = models.DecimalField(default=Decimal(0), max_digits=3, decimal_places=2)
    score = models.DecimalField(default=Decimal(0), max_digits=3, decimal_places=2)
    ultimate = models.IntegerField(default=0)

    def __str__(self):
        return self.mot

class NumberWord(models.Model):
    number = models.IntegerField(default=0)
    prof = models.CharField(max_length=30, default="")
    groupe_admin = models.BooleanField(default=False)
    username = models.CharField(max_length=100)
    taille_max = models.IntegerField(default=5)
    taille_ultime = models.IntegerField(default=10)
    first_connexion = models.DateTimeField(default=timezone.now)
    last_connexion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{}".format(self.number)

class Score(models.Model):
    username = models.CharField(max_length=100)
    date_challenge = models.DateTimeField(default=timezone.now)
    score = models.DecimalField(default=Decimal(0), max_digits=3, decimal_places=2)

    def __str__(self):
        return "{}".format(self.score)


class UltimateScore(models.Model):
    username = models.CharField(max_length=100)
    # mettre une image ici
    image = models.ImageField(storage=OverwriteStorage(), upload_to="dico/static/dico/images")
    score = models.ManyToManyField(Score)

    def __str__(self):
        return self.username