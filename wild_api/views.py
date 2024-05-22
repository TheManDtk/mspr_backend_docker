import logging
import json
from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework import status
from model_ia.preprocess import predict_image
from .models import Utilisateurs, InfoEspeces, Soumission, Identification
from .serializers import UtilisateursSerializer, SoumissionSerializer, IdentificationSerializer, InfoEspeceSerializer, LoginSerializer
from django.contrib.auth.hashers import make_password
from PIL import Image
import io
import numpy as np
from uuid import uuid4

# Configuration du logging
logging.basicConfig(level=logging.INFO)

# Configuration du FileSystemStorage
fs = FileSystemStorage(location='media/soumissions/')

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UtilisateursSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            password = validated_data.pop('password')
            user = Utilisateurs.objects.create_user(**validated_data)
            user.set_password(password)
            user.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            user_serializer = UtilisateursSerializer(user)
            return Response({'token': token.key, 'user': user_serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SoumettreImageView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, FileUploadParser]

    @csrf_exempt
    def post(self, request, format=None):
        logging.info("Réception d'une nouvelle demande de soumission d'image.")

        if 'image' not in request.data:
            logging.warning("Aucune image fournie dans la requête.")
            return Response({'error': 'Aucune image fournie'}, status=status.HTTP_400_BAD_REQUEST)

        image = request.FILES['image']
        try:
            espece, probabilite = predict_image(image)
            logging.info(f"Espèce prédite : {espece} avec une probabilité de {probabilite:.2f}.")
        except Exception as e:
            logging.error(f"Erreur lors de la prédiction de l'image : {e}")
            return Response({'error': 'Erreur lors de la prédiction de l\'image'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        probabilite_percent = probabilite * 100
        probabilite_percent = "{:.2f}".format(probabilite_percent)

        try:
            identification = Identification.objects.create(
                especetrouve=espece,
                niveau_correspondance=probabilite_percent
            )
            soumission = Soumission.objects.create(
                id_utilisateur=request.user,
                id_identification=identification,
                image=image
            )
            info_espece = InfoEspeces.objects.get(espece_nom=espece)

            identification_serializer = IdentificationSerializer(identification)
            info_espece_serializer = InfoEspeceSerializer(info_espece)
            data = {
                'identification': identification_serializer.data,
                'info_espece': info_espece_serializer.data,
                'probabilite': {'probabilite': probabilite_percent}
            }

            logging.info("Soumission et identification enregistrées avec succès.")
            return Response(data, status=status.HTTP_201_CREATED)

        except Exception as e:
            logging.error(f"Erreur lors de l'enregistrement des données : {e}")
            return Response({'error': 'Erreur lors de l\'enregistrement des données'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ObtenirInfoEspecesView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        info_especes = InfoEspeces.objects.all()
        serializer = InfoEspeceSerializer(info_especes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ObtenirSoumissionsUtilisateurView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        soumissions = Soumission.objects.filter(id_utilisateur=request.user)
        serializer = SoumissionSerializer(soumissions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
