from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from dico.models import*
from .forms import*
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from django.db.models import Min, Q
from django.core.files import File
from decimal import *
import random
from datetime import*
from django.utils import timezone
import time
import ast
import matplotlib.pyplot as plt
import os
import smtplib
# Create your views here.

PASSWORD_DEFAULT = "luffy"
USERNAME_DEFAULT = "SAGBO Philippe"

def suppress():
    list_suppress = []
    for objects_phil in User.objects.all():
        user = NumberWord.objects.get(username=objects_phil.username)
        if (((datetime.now(timezone.utc))-user.last_connexion).days > 90 and user.groupe_admin == False and user.username != USERNAME_DEFAULT):
            list_suppress.append(objects_phil.username)

    if list_suppress != []:
        for ancientUsername in list_suppress:
            for objects_phil in WordTranslate.objects.filter(username=ancientUsername):
                objects_phil.delete()

            for objects_phil in Wordnym.objects.filter(username=ancientUsername):
                objects_phil.delete()

            for objects_phil in Word.objects.filter(username=ancientUsername):
                objects_phil.delete()

            for objects_phil in NumberWord.objects.filter(username=ancientUsername):
                objects_phil.delete()

            for objects_phil in Score.objects.filter(username=ancientUsername):
                objects_phil.delete()

            for objects_phil in UltimateScore.objects.filter(username=ancientUsername):
                objects_phil.delete()

            User.objects.get(username=ancientUsername).delete()


def connexion(request):
    error = False
    form = ConnexionForm(request.POST or None)
    if form.is_valid():
        last_name = form.cleaned_data["last_name"]
        first_name = form.cleaned_data["first_name"]
        password = form.cleaned_data["password"]
        username = last_name.upper() + " " + first_name.capitalize()
        user = authenticate(last_name=last_name,
            first_name=first_name, password=password, username=username)
        if user:
            login(request, user)
            a = NumberWord.objects.get(username=str(request.user))
            a.last_connexion = datetime.now(timezone.utc)
            a.save()
            suppress()
            # There, we redirrecting the user in accueil
            if a.groupe_admin:
                return redirect(reverse(admin_accueil))
            return redirect(reverse(accueil))
        else:
            error = True

    return render(request, "dico/connexion.html", locals())

def true_accueil(request):
    return render(request, "dico/true_accueil.html", locals())


@login_required(login_url='connexion')
def account(request):
    user = User.objects.get(username=str(request.user))
    a = NumberWord.objects.get(username=str(request.user))

    return render(request, "dico/account.html", locals())

@login_required(login_url='connexion')
def send_mail(request):
    mmail = False
    a = NumberWord.objects.get(username=str(request.user))
    form = EmailForm(request.POST or None)
    if form.is_valid():
        message = form.cleaned_data["message"]
        send_mail_perso(request, message, 'vocabularyenglish0@gmail.com', 'vocabularyenglish0@gmail.com', 'English vocabulary website', 'artificialintelligence')
        mmail = True

    return render(request, "dico/send_mail.html", locals())

@login_required(login_url='connexion')
def send_mail_perso(request, message, mail_from, mail_to, subject, password, cc = None):
    user = User.objects.get(username = str(request.user))

    msg_header = 'From: {sender_name} <{mail_from}>\n' \
             'To: Ralph <{mail_to}>\n' \
             'MIME-Version: 1.0\n' \
             'Content-type: text/html\n' \
             'Subject: {subject}\n'.format(sender_name=str(request.user),
                mail_from=mail_from,
                mail_to=mail_to,
                subject=subject)
    message = '<h3>' + message + '\n' + ' ' + '\n' + str(request.user) + '\n' + str(user.email) + '</h3>'
    msg_content = message.replace('\n', '</h3> <h3>')
    msg_full = (''.join([msg_header, msg_content])).encode()
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(mail_from, password)
    server.sendmail(mail_from, mail_to, msg_full)
    server.quit()

    """ we can use 'CC: Receiver2 Name <jkfkfklfk...' in msg_header
    also go to this link

    https://www.google.com/settings/security/lesssecureapps
    you will unsertand
    """
    return 0

@login_required(login_url='connexion')
def profil(request, number):
    change = False
    user = User.objects.get_or_create(username=str(request.user))[0]
    a = NumberWord.objects.get(username=str(request.user))
    if number==1 or number == 11:
        form = ProfilUserForm(request.POST or None)
        if form.is_valid():
            last_name = form.cleaned_data['last_name']
            first_name = form.cleaned_data['first_name']
            username = last_name.upper() + " " + first_name.capitalize()
            if (len(User.objects.filter(username=username)) > 0):
                return redirect(reverse(profil, kwargs={'number':11}))
            else:
                ancientUsername = user.username
                user.username = username
                user.last_name = last_name
                user.first_name = first_name
                user.save()

                for objects_phil in WordTranslate.objects.filter(username=ancientUsername):
                    objects_phil.username = username
                    objects_phil.save()

                for objects_phil in Wordnym.objects.filter(username=ancientUsername):
                    objects_phil.username = username
                    objects_phil.save()

                for objects_phil in Word.objects.filter(username=ancientUsername):
                    objects_phil.username = username
                    objects_phil.save()

                for objects_phil in NumberWord.objects.filter(username=ancientUsername):
                    objects_phil.username = username
                    objects_phil.save()

                for objects_phil in Score.objects.filter(username=ancientUsername):
                    objects_phil.username = username
                    objects_phil.save()

                for objects_phil in UltimateScore.objects.filter(username=ancientUsername):
                    objects_phil.username = username
                    objects_phil.save()

                login(request, user)
                change = True


    if number == 2:
        form = ProfilEmailForm(request.POST or None)
        if form.is_valid():
            email = form.cleaned_data['email']
            user.email = email
            user.save()
            change = True

    if number == 3 or number == 33 or number == 34:
        form = ProfilPasswForm(request.POST or None)
        if form.is_valid():
            ancienpass = form.cleaned_data['ancienpass']
            password = form.cleaned_data['password']
            for objects_phil in User.objects.all():
                if objects_phil.check_password(password) and password != PASSWORD_DEFAULT:
                    return redirect(reverse(profil, kwargs={'number':33}))
            if user.check_password(ancienpass)==False:
                return redirect(reverse(profil, kwargs={'number':34}))
            if password == PASSWORD_DEFAULT and user.username == USERNAME_DEFAULT:
                user.is_staff = True
                user.is_superuser = True
            else:
                user.is_staff = False
                user.is_superuser = False
            user.set_password(password)
            user.save()
            login(request, user)
            change = True

    if number == 4:
        form = ProfilProfForm(request.POST or None)
        if form.is_valid():
            newprof = form.cleaned_data['prof']
            ancientprof = a.prof
            a.prof = newprof.upper()
            a.save()
            change = True
            if a.groupe_admin:
                for objects_phil in NumberWord.objects.filter(prof=a.prof):
                    objects_phil.prof = newprof
                    objects_phil.save()

    return render(request, "dico/profil.html", locals())

def suc_pro(request):
    return render(request, "dico/suc_pro.html", locals())

def first_connexion(request, number=0):
    form = FirstConnexionForm(request.POST or None)
    if form.is_valid():
        last_name = form.cleaned_data["last_name"]
        first_name = form.cleaned_data["first_name"]
        password = form.cleaned_data["password"]
        prof = form.cleaned_data["prof"]
        groupe_admin = form.cleaned_data["groupe_admin"]
        for objects_phil in User.objects.all():
            if objects_phil.check_password(password):
                return redirect(reverse(first_connexion, kwargs={'number':1}))

        email = form.cleaned_data["email"]
        username = last_name.upper() + " " + first_name.capitalize()

        try:
            user = authenticate(last_name=last_name,
                first_name=first_name, password=password)
            answer=0
            if user == None:
                user = User.objects.create_user(username = username,
                    password=password, last_name=last_name, first_name=first_name, email=email)
                answer = "new"
                # There, we redirrecting the user in accueil
                if password == PASSWORD_DEFAULT and user.username == USERNAME_DEFAULT:
                    user.is_staff = True
                    user.is_superuser = True
                    user.save()
                    answer = "super"
                    # There, we are redirecting the superuser towards an another page
                login(request, user)
                a = NumberWord(username=str(request.user))
                a.username = username
                a.prof = prof.strip().upper()
                a.groupe_admin = groupe_admin
                a.save()

                if groupe_admin == True and a.prof.upper() != a.username.upper():
                    a.groupe_admin = False
                    a.save()

                if groupe_admin:
                    return redirect(reverse(admin_accueil))
                return redirect(reverse(accueil))
        except IntegrityError:
            answer = "deja"
            return redirect(reverse(connexion))
    return render(request, "dico/first_connexion.html", locals())


@login_required(login_url='connexion')
def admin_affiche_graphe(request, username):
    user = User.objects.get(username=username)
    number = NumberWord.objects.get(username=username)
    a = NumberWord.objects.get(username=str(request.user))
    schema = False
    xabs = []
    yord = []
    if UltimateScore.objects.get_or_create(username=username)[1] == False:
        SCORES = UltimateScore.objects.get(username=username)

        if len(SCORES.score.all()) > 1:
            point1 = UltimateScore.objects.get_or_create(username=username)[0]
        else:
            schema = True
    else:
        schema = True

    return render(request, "dico/admin_affiche_graphe.html", locals())



@login_required(login_url='connexion')
def deconnexion(request):
    logout(request)
    return render(request, "dico/deconnexion.html", locals())

@login_required(login_url='connexion')
def append_word(request):
    dico_state = 0
    form = WordForm(request.POST or None)
    number_user = NumberWord.objects.get(username=str(request.user))
    TAILLE_LIMIT = number_user.taille_max
    number_user.number = len(Word.objects.filter(username=str(request.user)))
    number_user.save()

    tt = verification_score(request)
    h=len(tt)
    if h != 0:
        i = tt[0]
        yo = True
        return render(request, "dico/ul_test.html", locals())

    if form.is_valid():
        word1 = form.cleaned_data["word1"]
        word2 = form.cleaned_data["word2"]
        comment = form.cleaned_data["comment"]
        dico2 = WordTranslate.objects.filter(username=str(request.user), mot=word2)
        dico1 = Word.objects.filter(username=str(request.user), mot=word1)
        dico1nym = Wordnym.objects.filter(username=str(request.user), mot=word1)
        if(len(dico1)==0 and len(dico2)==0 and len(dico1nym)==0):
            dico_state = 1
            mot1 = Word(username=str(request.user), mot=word1, comment=comment, translate_mot=word2)
            mot1.save()
            mot2 = WordTranslate(username=str(request.user), mot=word2)
            mot2.save()
            mot1.translate_word.add(mot2)
            mot1.save()
            number_user.number = len(Word.objects.filter(username=str(request.user)))
            number_user.save()
        elif(len(dico1nym)!=0 and len(dico2)==0):
            mot1nym = dico1nym.get(username=str(request.user), mot=word1)
            mot1nym.save()
            mmot1 = mot1nym.word_set.get(username=str(request.user))
            mmot1.synonym.add(mot1nym)
            if comment!='':
                mmot1.comment = mmot1.comment + '</br>' + comment
            mmot1.save()
            mot2 = WordTranslate(username=str(request.user), mot=word2)
            mot2.save()
            mmot1.translate_word.add(mot2)
            mmot1.save()
        elif(len(dico1)!=0 and len(dico2)==0):
            dico_state = 2
            mot2 = WordTranslate(username=str(request.user), mot=word2)
            mot2.save()
            mot1 = dico1.get(username=str(request.user), mot=word1)
            if comment!='':
                mot1.comment = mot1.comment + '</br>' + comment
            mot1.translate_word.add(mot2)
            mot1.save()
        elif(len(dico1)==0 and len(dico2)!=0 and len(dico1nym)==0):
            dico_state = 3
            mot1 = Wordnym(username=str(request.user), mot=word1)
            mot1.save()
            mot2 = dico2.get(username=str(request.user), mot=word2)
            mot2.save()
            mmot1 = mot2.word_set.get(username=str(request.user))
            if comment!='':
                mmot1.comment = mmot1.comment + '</br>' + comment
            mmot1.save()
            mmot1.synonym.add(mot1)
            mmot1.save()
        else:
            dico_state = 4
        form = WordForm()  # in order to erase fields of the form
    return render(request, "dico/append_word.html", locals())


@login_required(login_url='connexion')
def accueil(request):
    verification_date(request)
    number_user = NumberWord.objects.get_or_create(username=str(request.user))[0]
    dico1 = Word.objects.filter(username=str(request.user))
    k=0
    for i, word in enumerate(dico1):
        if (i%number_user.taille_max != 0 and word.score != 0):
            k=1
            break
    if k==1:
        for word in dico1:
            word.score = 0
            word.date_challenge = datetime.now(timezone.utc)
            word.save()
    dico2 = WordTranslate.objects.filter(username=str(request.user))

    if 'search' in request.GET:
        search_term = request.GET['search']
        dico1_perso = []
        for objects_phil in Word.objects.filter(Q(username=str(request.user)) & (Q(mot__icontains=search_term) | Q(comment__icontains=search_term) | Q(translate_mot__icontains=search_term))):
            dico1_perso.append(objects_phil)

        ddico2_perso = WordTranslate.objects.filter(username=str(request.user), mot__icontains=search_term)
        if len(ddico2_perso) != 0:
            for objects_phil in ddico2_perso:
                for i in objects_phil.word_set.all():
                    dico1_perso.append(i)

        ddico2_perso = Wordnym.objects.filter(username=str(request.user), mot__icontains=search_term)
        if len(ddico2_perso) != 0:
            for objects_phil in ddico2_perso:
                for i in objects_phil.word_set.all():
                    dico1_perso.append(i)

        dico1 = list(set(dico1_perso))

    return render(request, "dico/accueil.html", locals())


@login_required(login_url='connexion')
def admin_accueil(request):
    number_user = NumberWord.objects.get_or_create(username=str(request.user))[0]
    a=number_user
    prof = number_user.prof
    students = []
    dico1 = []
    dico2 = []

    students = []

    ultimate_number1 = 0

    for user in User.objects.all():
        number_user_student = NumberWord.objects.get(username=user.username)
        if number_user_student.prof.upper() == prof.upper() and prof.upper() != number_user_student.username.upper():
            ultimate_number1 = ultimate_number1 + number_user_student.number

            students.append(user)

            for mot1 in Word.objects.filter(username=user.username):
                dico1.append(mot1)
            for mot2 in WordTranslate.objects.filter(username=user.username):
                dico2.append(mot2)

    ultimate_number = ultimate_number1
    if 'search' in request.GET:
        search_term = request.GET['search']
        dico1_perso = []
        for user in students:
            for objects_phil in Word.objects.filter(Q(username=user.username) & (Q(mot__icontains=search_term) | Q(comment__icontains=search_term) | Q(translate_mot__icontains=search_term) | Q(username__icontains=search_term))):
                dico1_perso.append(objects_phil)

        for user in students:
            ddico2_perso = WordTranslate.objects.filter(username=user.username, mot__icontains=search_term)
            if len(ddico2_perso) != 0:
                for objects_phil in ddico2_perso:
                    for i in objects_phil.word_set.all():
                        dico1_perso.append(i)

        for user in students:
            ddico2_perso = Wordnym.objects.filter(username=user.username, mot__icontains=search_term)
            if len(ddico2_perso) != 0:
                for objects_phil in ddico2_perso:
                    for i in objects_phil.word_set.all():
                        dico1_perso.append(i)


        dico1 = list(set(dico1_perso))


    return render(request, "dico/admin_accueil.html", locals())



@login_required(login_url='connexion')
def info(request, word, number, username=""):
    # Firstly, we display information about the word and then we take actions
    # delete or suppress
    a = NumberWord.objects.get(username=str(request.user))
    if username=="":
        username=str(request.username)

    if number == 1:
        mot = Word.objects.get(username=username, mot=word)
    if number == 2:
        motnym = Wordnym.objects.get(username=username, mot=word)
        mot = motnym.word_set.get(username=username)
    if number == 3:
        mottranslate = WordTranslate.objects.get(username=username, mot=word)
        mot = mottranslate.word_set.get(username=username)
    if number == 4:
        mot = Word.objects.get(username=username, mot=word)

    return render(request, "dico/info.html", locals())

@login_required(login_url='connexion')
def action(request, word, number, number_action, username=""):
    a = NumberWord.objects.get(username=str(request.user))
    if username=="":
        username=str(request.username)
    if len(Word.objects.filter(username=username, mot=word))==0 and len(Wordnym.objects.filter(username=username, mot=word))==0 and len(WordTranslate.objects.filter(username=username, mot=word))==0:
        if a.groupe_admin == True:
            return redirect(reverse(admin_accueil))
        return redirect(reverse(accueil))

    if number == 1:
        mot = Word.objects.get(username=username, mot=word)
    if number == 2:
        motnym = Wordnym.objects.get(username=username, mot=word)
        mot = motnym.word_set.get(username=username)
    if number == 3:
        mottranslate = WordTranslate.objects.get(username=username, mot=word)
        mot = mottranslate.word_set.get(username=username)
    if number == 4:
        mot = Word.objects.get(username=username, mot=word)
    if number_action == 1:
        change=False
        if number==1 or number==2:
            form = Change_wordForm(request.POST or None)
            if form.is_valid():
                new_word = form.cleaned_data["new_word"]
                if number == 1:
                    mot.mot = new_word
                    mot.save()
                else:
                    motnym.mot = new_word
                    motnym.save()
                change=True
        elif number==3:
            form = Change_wordForm(request.POST or None)
            if form.is_valid():
                new_word = form.cleaned_data["new_word"]
                mottranslate.mot = new_word
                mottranslate.save()
                change=True
        else:
            form = Change_commentForm(request.POST or None)
            if form.is_valid():
                new_comment = form.cleaned_data["new_comment"]
                mot.comment = mark_safe(new_comment)
                mot.save()
                change=True
    elif number_action == 0:
        delete = False
        if number == 2:
            motnym.username = "a_supprimer"
            motnym.save()
            Wordnym.objects.filter(username="a_supprimer").delete()
        elif number == 3:
            translate = mot.translate_word.all()
            if len(translate) == 1:
                delete = False
            else:
                delete = True
                mottranslate.username = "a_supprimer"
                mottranslate.save()
                WordTranslate.objects.filter(username="a_supprimer").delete()
        elif number == 4:
            mot.comment = ""
            mot.save()


    return render(request, "dico/action.html", locals())

@login_required(login_url='connexion')
def test(request):
    tt = verification_score(request)
    h=len(tt)
    if h != 0:
        i = tt[0]
    number = NumberWord.objects.get(username=str(request.user)).number
    TAILLE_LIMIT = NumberWord.objects.get(username=str(request.user)).taille_max
    num = number % TAILLE_LIMIT

    return render(request, "dico/test.html", locals())

@login_required(login_url='connexion')
def test1inter(request, choice):
    TAILLE_LIMIT = NumberWord.objects.get(username=str(request.user)).taille_max
    mot, tt = [], []
    for i in range(TAILLE_LIMIT):
        mot.append([0,1])
        tt.append(i)
    score = []

    number = NumberWord.objects.get(username=str(request.user)).number
    list_word = Word.objects.filter(username=str(request.user))
    list_word = list_word[TAILLE_LIMIT*(choice-1):TAILLE_LIMIT*choice]

    choice_word = random.randint(0, len(tt)-1)
    ind = tt[choice_word]
    if len(mot[ind]) == 2:
        choice2_word = random.randint(0, 1)
        mot[ind].remove(choice2_word)
    elif len(mot[ind]) == 1:
        choice2_word = mot[ind][0]
        mot[ind] = []
        del(tt[choice_word])
    word1 = list_word[ind]

    if choice2_word == 0:
        word = []
        word.append(word1)
        for i in word1.synonym.all():
            word.append(i)
        word = word[random.randint(0, len(word)-1)]
        question = word
    else:
        question = word1.translate_word.all()[random.randint(0, len(word1.translate_word.all())-1)]

    mot1 = question.mot
    mot=str(mot)
    tt=str(tt)
    score=str(score)
    time1 = str(0)
    time2  = str(0)
    k = 0
    solution = '_'
    l=0

    return redirect(reverse(test1, kwargs={'choice':choice, 'choice2_word':choice2_word, 'mot':mot, 'tt':tt, 'score':score, 'solution':solution, 'mot1':mot1, 'temps':time1, 'temps_init':time2, 'k':k, 'l':l}))

@login_required(login_url='connexion')
def test1(request, choice, choice2_word, mot, tt, score, mot1, temps, temps_init, k, solution, l):
    temps = ast.literal_eval(temps)
    temps_init = ast.literal_eval(temps_init)
    mot = ast.literal_eval(mot)
    tt = ast.literal_eval(tt)
    score = ast.literal_eval(score)
    TAILLE_LIMIT = NumberWord.objects.get(username=str(request.user)).taille_max
    number = NumberWord.objects.get(username=str(request.user)).number
    list_word = Word.objects.filter(username=str(request.user))
    list_word = list_word[TAILLE_LIMIT*(choice-1):TAILLE_LIMIT*choice]

    if k != 0:
        error = True
    if solution != '_':
        answer = True
        l=1
    if l==1:
        l=0
    elif l==0:
        solution = '_'


    form = TestForm(request.POST or None)
    if form.is_valid():
        proposition_answer = form.cleaned_data["proposition_answer"]
        if temps==0:
            temps_init = time.time()
        else:
            temps = time.time()-temps_init


        if choice2_word==0:
            if len(Word.objects.filter(username=str(request.user), mot=mot1))!=0:
                question = Word.objects.get(username=str(request.user), mot=mot1)
            else:
                question1 = Wordnym.objects.get(username=str(request.user), mot=mot1)
                question = question1.word_set.get(username=str(request.user))
            response = question.translate_word.all()
        else:
            question = WordTranslate.objects.get(username=str(request.user), mot=mot1)
            response = list(question.word_set.all())
            for i in response[0].synonym.all():
                response.append(i)


        if (verify(response, proposition_answer)==1 or k==2):
            if k==2:
                score_mot = 0
                solution = response[0].mot
            else:
                solution = '_'
                score_mot = 3 - k - temps//5
            score.append(score_mot)
            temps = str(0)
            temps_init = str(0)
            k = 0

            if len(tt)==0:
                score=str(score)
                return redirect(reverse(affiche_score, kwargs={'score':score, 'choice':choice}))
            choice_word = random.randint(0, len(tt)-1)
            ind = tt[choice_word]
            if len(mot[ind]) == 2:
                choice2_word = random.randint(0, 1)
                mot[ind].remove(choice2_word)
            elif len(mot[ind]) == 1:
                choice2_word = mot[ind][0]
                mot[ind] = []
                del(tt[choice_word])

            word1 = list_word[ind]
            if choice2_word == 0:
                word = []
                word.append(word1)
                for i in word1.synonym.all():
                    word.append(i)
                word = word[random.randint(0, len(word)-1)]
                question = word
            else:
                question = word1.translate_word.all()[random.randint(0, len(word1.translate_word.all())-1)]
            mot=str(mot)
            tt=str(tt)
            score=str(score)
            mot1=str(question.mot)
            temps=str(temps)
            temps_init = str(temps_init)
        else:
            k += 1



        return redirect(reverse(test1, kwargs={'choice':choice, 'choice2_word':choice2_word, 'mot':mot, 'tt':tt, 'score':score, 'mot1':mot1, 'temps':temps, 'temps_init':temps_init, 'k':k, 'solution':solution, 'l':l}))

    return render(request, "dico/test1.html", locals())

@login_required(login_url='connexion')
def affiche_score(request, score, choice):
    TAILLE_LIMIT = NumberWord.objects.get(username=str(request.user)).taille_max
    score = ast.literal_eval(score)
    score_f = float(sum(score))/(len(score)*3)
    list_word = Word.objects.filter(username=str(request.user))
    word = list_word[TAILLE_LIMIT*(choice-1)]
    word.score = Decimal(score_f)
    word.score_d = Decimal(score_f)
    word.date_challenge = datetime.now(timezone.utc)
    word.save()
    return render(request, "dico/affiche_score.html", locals())

def verify(querryset, word):
    "return 0 if word isn't the attribut mot of querryqet and 1 else"
    for mot in querryset:
        if mot.mot == word:
            return 1
    return 0

@login_required(login_url='connexion')
def ul_test(request):
    TAILLE_LIMIT = NumberWord.objects.get(username=str(request.user)).taille_max
    TAILLE_ULTIME = NumberWord.objects.get(username=str(request.user)).taille_ultime
    tt = verification_score(request)
    h=len(tt)
    if h != 0:
        i = tt[0]
        yo = True
        return render(request, "dico/ul_test.html", locals())
    else:
        number = NumberWord.objects.get(username=str(request.user)).number
        if number >= TAILLE_ULTIME:
            list_w = Word.objects.filter(username=str(request.user))
            minimum = list_w.aggregate(minimum=Min('ultimate'))['minimum']
            if minimum == 0 and number%TAILLE_LIMIT!=0:
                list_w = Word.objects.filter(username=str(request.user), ultimate__gte=1)
                minimum = list_w.aggregate(minimum=Min('ultimate'))['minimum']
            words_min = Word.objects.filter(username=str(request.user), ultimate=minimum)

            number = number - number%TAILLE_LIMIT
            mot_ind = [x for x in range(number)]
            mot_ind_min = []
            for i in words_min:
                mot_ind_min.append(list(list_w).index(i))
            n_min = len(words_min)

            list_word_int = []
            random.shuffle(mot_ind_min)
            random.shuffle(mot_ind_min)

            if n_min >= TAILLE_ULTIME:
                for i in range(TAILLE_ULTIME):
                    list_word_int.append(mot_ind_min[i])
            else:
                for i in range(n_min):
                    list_word_int.append(mot_ind_min[i])
                n_mot = TAILLE_ULTIME - n_min
                for i in range(n_min):
                    mot_ind.remove(list_word_int[i])
                random.shuffle(mot_ind)
                random.shuffle(mot_ind)
                for i in range(n_mot):
                    list_word_int.append(mot_ind[i])

            score = []

            tt = [x for x in range(TAILLE_ULTIME)]

            mot=[]
            for i in range(TAILLE_ULTIME):
                mot.append([0,1])



            ind = random.randint(0, len(tt)-1)




            list_word = [list_w[x] for x in list_word_int]

            choice_word = random.randint(0, len(tt)-1)
            ind = tt[choice_word]
            if len(mot[ind]) == 2:
                choice2_word = random.randint(0, 1)
                mot[ind].remove(choice2_word)

            elif len(mot[ind]) == 1:
                choice2_word = mot[ind][0]
                mot[ind] = []
                del(tt[choice_word])
            word1 = list_word[ind]

            if choice2_word == 0:
                word = []
                word.append(word1)
                for i in word1.synonym.all():
                    word.append(i)
                word = word[random.randint(0, len(word)-1)]
                question = word
            else:
                question = word1.translate_word.all()[random.randint(0, len(word1.translate_word.all())-1)]

            mot1 = question.mot
            mot=str(mot)
            tt=str(tt)
            score=str(score)
            time1 = str(0)
            time2  = str(0)
            k = 0
            solution = '_'
            list_word_int = str(list_word_int)

            return redirect(reverse(ul_test1, kwargs={'choice2_word':choice2_word, 'mot':mot, 'tt':tt, 'score':score, 'solution':solution, 'mot1':mot1, 'temps':time1, 'temps_init':time2, 'k':k, 'l':0, 'list_word_int':list_word_int}))
        else:
            return render(request, "dico/ul_test.html", locals())


@login_required(login_url='connexion')
def ul_test1(request, choice2_word, mot, tt, score, mot1, temps, temps_init, k, solution, l, list_word_int):
    list_word_int = ast.literal_eval(list_word_int)
    temps = ast.literal_eval(temps)
    temps_init = ast.literal_eval(temps_init)
    mot = ast.literal_eval(mot)
    tt = ast.literal_eval(tt)
    score = ast.literal_eval(score)

    words = Word.objects.filter(username=str(request.user))
    list_word = [words[x] for x in list_word_int]

    if k != 0:
        error = True
    if solution != '_':
        answer = True
        l=1
    if l==1:
        l=0
    elif l==0:
        solution = '_'

    form = TestForm(request.POST or None)
    if form.is_valid():
        proposition_answer = form.cleaned_data["proposition_answer"]
        if temps==0:
            temps_init = time.time()
        else:
            temps = time.time()-temps_init

        if choice2_word==0:
            if len(Word.objects.filter(username=str(request.user), mot=mot1))!=0:
                question = Word.objects.get(username=str(request.user), mot=mot1)
            else:
                question1 = Wordnym.objects.get(username=str(request.user), mot=mot1)
                question = question1.word_set.get(username=str(request.user))
            response = question.translate_word.all()
        else:
            question = WordTranslate.objects.get(username=str(request.user), mot=mot1)
            response = list(question.word_set.all())
            for i in response[0].synonym.all():
                response.append(i)


        if (verify(response, proposition_answer)==1 or k==2):

            if k==2:
                score_mot = 0
                solution = response[0].mot
            else:
                solution = '_'
                score_mot = 3 - k - temps//5
            score.append(score_mot)
            temps = str(0)
            temps_init = str(0)
            k = 0

            if len(tt)==0:
                score = str(score)
                list_word_int = str(list_word_int)
                return redirect(reverse(ul_affiche_score, kwargs={'score':score, 'list_word_int':list_word_int}))
            choice_word = random.randint(0, len(tt)-1)
            ind = tt[choice_word]
            if len(mot[ind]) == 2:
                choice2_word = random.randint(0, 1)
                mot[ind].remove(choice2_word)
            elif len(mot[ind]) == 1:
                choice2_word = mot[ind][0]
                mot[ind] = []
                del(tt[choice_word])

            word1 = list_word[ind]
            if choice2_word == 0:
                word = []
                word.append(word1)
                for i in word1.synonym.all():
                    word.append(i)
                word = word[random.randint(0, len(word)-1)]
                question = word
            else:
                question = word1.translate_word.all()[random.randint(0, len(word1.translate_word.all())-1)]

            mot=str(mot)
            tt=str(tt)
            score=str(score)
            mot1=str(question.mot)
            temps=str(temps)
            temps_init = str(temps_init)
        else:
            k += 1

        list_word_int = str(list_word_int)

        return redirect(reverse(ul_test1, kwargs={'choice2_word':choice2_word, 'mot':mot, 'tt':tt, 'score':score, 'mot1':mot1, 'temps':temps, 'temps_init':temps_init, 'k':k, 'solution':solution, 'l':l, 'list_word_int':list_word_int}))

    return render(request, "dico/test1.html", locals())

@login_required(login_url='connexion')
def ul_affiche_score(request, score, list_word_int):
    ultimate = False
    list_word_int = ast.literal_eval(list_word_int)
    score = ast.literal_eval(score)
    score_f = float(sum(score))/(len(score)*3)
    point = Score()
    point.username = str(request.user)
    point.score = Decimal(score_f)
    point.date_challenge = datetime.now(timezone.utc)
    point.save()
    point1 = UltimateScore.objects.get_or_create(username=str(request.user))[0]
    point1.save()
    point1.score.add(point)
    point1.save()
    xabs = []
    yord = []

    if len(point1.score.all())!=0:
        if len(point1.score.all()) > 1:
            ultimate = True
        for score in point1.score.all():
            debut = score
            break
        for score in point1.score.all():
            xabs.append((score.date_challenge-debut.date_challenge).days)
            yord.append(score.score)

        plt.title("Evolution of " + str(request.user))
        plt.axis()
        plt.xlabel("days")
        plt.ylabel("score")
        plt.plot(xabs, yord)
        image_name = str(request.user)
        image_name = image_name.replace(" ", "_")
        image_name = image_name + ".png"
        if os.path.isfile(image_name):
            os.remove(image_name)
        plt.savefig(image_name)

        content = File(open(image_name, 'rb'))

        point1.image.save(image_name, content)

    words = Word.objects.filter(username=str(request.user))

    list_word = [words[x] for x in list_word_int]

    for word in list_word:
        word.ultimate += 1
        word.save()

    return render(request, "dico/affiche_score.html", locals())

@login_required(login_url='connexion')
def affiche_graphe(request):
    schema = False
    xabs = []
    yord = []
    if UltimateScore.objects.get_or_create(username=str(request.user))[1] == False:
        SCORES = UltimateScore.objects.get(username=str(request.user))

        if len(SCORES.score.all()) > 1:
            point1 = UltimateScore.objects.get_or_create(username=str(request.user))[0]
        else:
            schema = True
    else:
        schema = True

    return render(request, "dico/affiche_graphe.html", locals())

def verification_score(request):
    list_word =  Word.objects.filter(username=str(request.user))
    TAILLE_LIMIT = NumberWord.objects.get(username=str(request.user)).taille_max
    tt = []
    for i, word in enumerate(list_word):
        if i % TAILLE_LIMIT == 0:
            if word.score < 0.7 and len(list_word) >= i+TAILLE_LIMIT:
                tt.append(i)
    return tt


def verification_date(request):
    TAILLE_LIMIT = NumberWord.objects.get(username=str(request.user)).taille_max
    list_word =  Word.objects.filter(username=str(request.user))
    tt = []
    for i, word in enumerate(list_word):
        if i % TAILLE_LIMIT == 0:
            word.score = word.score_d - Decimal(((datetime.now(timezone.utc) - word.date_challenge).days)/10)
            word.save()