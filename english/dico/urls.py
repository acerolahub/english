from django.urls import path 
from django.contrib import admin
from . import views

urlpatterns = [
    path("connexion", views.connexion, name="connexion"),
    path("first_connexion/<int:number>", views.first_connexion, name="first_connexion"),
    path("accueil/", views.accueil, name="accueil"),
    path("deconnexion/", views.deconnexion, name="deconnexion"),
    path("append_word/", views.append_word, name="append_word"),
    path("infos/<str:word>/<int:number>/<str:username>/", views.info, name="info"),
    path("action/<str:word>/<int:number>/<int:number_action>/<str:username>/", views.action, name="action"),
    path("test/", views.test, name="test"),
    path("test1inter/<int:choice>", views.test1inter, name="test1inter"),
    path("test1/<int:choice>/<str:mot>/<str:tt>/<str:score>/<str:mot1>/<int:choice2_word>/<str:temps>/<str:temps_init>/<int:k>/<str:solution>/<int:l>", views.test1, name='test1'),
    path("affiche_score/<str:score>/<int:choice>", views.affiche_score, name='affiche_score'),
    path("ul_test/", views.ul_test, name="ul_test"),
    path("ul_test1/<str:mot>/<str:tt>/<str:score>/<str:mot1>/<int:choice2_word>/<str:temps>/<str:temps_init>/<int:k>/<str:solution>/<int:l>/<str:list_word_int>", views.ul_test1, name='ul_test1'),
    path("ul_affiche_score/<str:score>/<str:list_word_int>", views.ul_affiche_score, name="ul_affiche_score"),
    path("affiche_graphe/", views.affiche_graphe, name="affiche_graphe"),
    path("account/", views.account, name="account"),
    path("send_mail/", views.send_mail, name="send_mail"),
    path("profil/<int:number>", views.profil, name="profil"),
    path("suc_pro/", views.suc_pro, name="suc_pro"),
    path("", views.true_accueil, name="true_accueil"),
    path("admin_accueil", views.admin_accueil, name="admin_accueil"),
    path("admin_affiche_graphe/<str:username>/", views.admin_affiche_graphe, name="admin_affiche_graphe"),
]