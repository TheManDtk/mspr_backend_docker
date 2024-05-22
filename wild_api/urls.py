from django.contrib import admin
from django.urls import path
from .views import RegisterView, LoginView, SoumettreImageView, ObtenirInfoEspecesView,ObtenirSoumissionsUtilisateurView



urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('soumissions/', SoumettreImageView.as_view(), name='soumettre_image'),
    path('info-especes/', ObtenirInfoEspecesView.as_view(), name='obtenir_info_especes'),
    path('list-soumissions/', ObtenirSoumissionsUtilisateurView.as_view(), name='soumissions'),
    #path('infoespeces/', InfoEspecesView.as_view(), name='infoespeces'),
    #path('soumissions/', SoumissionView.as_view(), name='soumissions'),
    #path('identifications/', IdentificationView.as_view(), name='identifications'),
]

