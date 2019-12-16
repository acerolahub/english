from django.contrib import admin
from .models import*
# Register your models here.

class NumberWordAdmin(admin.ModelAdmin):
	list_display = ('username', 'number', 'taille_max', 'taille_ultime')
	list_filter = ('username', 'number')
	search_fields = ('number', 'username')

class WordAdmin(admin.ModelAdmin):
	list_display = ('mot', 'translate_mot', 'username', 'date', 'comment', 'ultimate', 'score', 'date_challenge')
	search_fields = ('username', 'mot', 'translate_mot')
	

class ScoreAdmin(admin.ModelAdmin):
	list_display = ('score', 'date_challenge', 'username')

	
admin.site.register(Word, WordAdmin)
admin.site.register(NumberWord, NumberWordAdmin)
admin.site.register(UltimateScore)

admin.site.register(Wordnym)
admin.site.register(WordTranslate)
admin.site.register(Score, ScoreAdmin)