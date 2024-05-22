from rest_framework import serializers
from django.forms import ValidationError
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import Utilisateurs, InfoEspeces, Soumission, Identification
from django.contrib.auth import get_user_model

User = get_user_model()

class UtilisateursSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'phone_number', 'first_name', 'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

class LoginSerializer(serializers.Serializer):
    username = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(**attrs)
        if user:
            return {'user': user}
        else:
            raise serializers.ValidationError('Identifiants incorrects')

    
class InfoEspeceSerializer(serializers.ModelSerializer):
    cover = serializers.ImageField(use_url=True)
    class Meta:
        model = InfoEspeces
        fields = ['id', 'espece_nom', 'description', 'nom_latin', 'famille', 'region', 'habitat', 'fun_fact', 'cover']

class IdentificationSerializer(serializers.ModelSerializer):
    id_infoEspece = InfoEspeceSerializer()

    class Meta:
        model = Identification
        fields = ['id', 'especetrouve', 'niveau_correspondance', 'id_infoEspece']

class SoumissionSerializer(serializers.ModelSerializer):
    id_identification = IdentificationSerializer()

    class Meta:
        model = Soumission
        fields = ['id', 'date_soumission', 'id_utilisateur', 'image', 'id_identification']

