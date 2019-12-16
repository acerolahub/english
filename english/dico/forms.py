from django import forms
from django.utils.safestring import mark_safe

class ConnexionForm(forms.Form):
    last_name = forms.CharField(label="Nom", max_length=30, widget=forms.TextInput(attrs={'autofocus': 'autofocus'}))
    first_name = forms.CharField(label="Prénom", max_length=30)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)


class FirstConnexionForm(forms.Form):
    last_name = forms.CharField(label="Nom", max_length=30, widget=forms.TextInput(attrs={'autofocus': 'autofocus'}))
    first_name = forms.CharField(label="Prénom", max_length=30)
    email = forms.EmailField(label="Enter your adress mail or nothing if you don't have it", required=False)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmez votre mot de passe", widget=forms.PasswordInput)
    prof = forms.CharField(label="Superviseur (NOM Prénom)", max_length=30, required=False)
    groupe_admin = forms.BooleanField(label=mark_safe("Ce compte est-il utilisé pour administrer un groupe de personnes? Si oui, cochez cette case </br>"), label_suffix="", required=False)


    def clean(self):
        cleaned_data = super(FirstConnexionForm, self).clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            self.add_error("password", "Ces mots de passe ne sont pas identiques")

        return cleaned_data

class WordForm(forms.Form):
    word1 = forms.CharField(label="Enter a word in english", max_length=30, widget=forms.TextInput(attrs={'autofocus': 'autofocus'}))
    word2 = forms.CharField(label="Enter his translation into french", max_length=30)
    comment = forms.CharField(label="Enter a comment if you want", max_length=100, widget=forms.Textarea, required=False)

class Change_wordForm(forms.Form):
    new_word = forms.CharField(label="Enter a new word", max_length=30, widget=forms.TextInput(attrs={'autofocus': 'autofocus'}))

class Change_commentForm(forms.Form):
    new_comment = forms.CharField(label="Enter a new word", max_length=30, widget=forms.Textarea(attrs={'autofocus': 'autofocus'}))

class TestForm(forms.Form):
    proposition_answer = forms.CharField(label="", max_length=30, widget=forms.TextInput(attrs={'autofocus': 'autofocus', 'autocomplete':'off'}))

class EmailForm(forms.Form):
    message = forms.CharField(label="", max_length=10000, widget=forms.Textarea(attrs={'autofocus': 'autofocus'}))

class ProfilUserForm(forms.Form):
    last_name = forms.CharField(label="last_name", max_length=30, widget=forms.TextInput(attrs={'autofocus': 'autofocus'}))
    first_name = forms.CharField(label="first_name", max_length=30)

class ProfilPasswForm(forms.Form):
    ancienpass = forms.CharField(label="Enter your current password", widget=forms.PasswordInput(attrs={'autofocus': 'autofocus'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirme your password", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(ProfilPasswForm, self).clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            self.add_error("password", "These two passwords are not identical")

        return cleaned_data

class ProfilEmailForm(forms.Form):
    email = forms.EmailField(label="", required=False, widget=forms.TextInput(attrs={'autofocus': 'autofocus'}))

class ProfilProfForm(forms.Form):
    prof = forms.CharField(label="Supervisor (LAST_NAME First_name)", max_length=30, widget=forms.TextInput(attrs={'autofocus': 'autofocus'}))
