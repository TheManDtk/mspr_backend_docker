from django.db import models
from django.contrib.auth.models import AbstractUser
import re
# Create your models here.
class Utilisateurs(AbstractUser):
    username = models.EmailField(unique=True, null=True, verbose_name="Mail")
    phone_number = models.CharField(max_length=17, null=True, unique=True, blank=True, verbose_name="Téléphone")
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    
    class Meta:
        swappable = 'AUTH_USER_MODEL'

    def format_phone_number(self):
        # Replace a space with an empty string
        self.phone_number = re.sub(r"\s", "", self.phone_number)
        # Replace a + with '00'
        self.phone_number = re.sub(r"\+", "00", self.phone_number)
        # Make sure phone_number only contains digits
        self.phone_number = re.sub(r"[^0-9]", "", self.phone_number)
        if not self.phone_number.startswith('0033'):
            self.phone_number = '0033' + self.phone_number
            
    
    def __str__(self):
        return f'{self.first_name} ({self.last_name})'

class InfoEspeces(models.Model):
    espece_nom = models.CharField(max_length=50)
    description = models.TextField()
    nom_latin = models.CharField(max_length=100)
    famille = models.CharField(max_length=13, default='Mammifères') 
    region = models.TextField() 
    habitat = models.TextField()
    fun_fact = models.TextField()
    cover = models.ImageField(upload_to='covers/', null = True)

class Soumission(models.Model):
    date_soumission = models.DateField(auto_now_add=True)
    id_utilisateur = models.ForeignKey(Utilisateurs, on_delete=models.PROTECT, null = True)
    id_identification = models.OneToOneField('Identification', null=True, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='soumissions/')  # Champ pour stocker l'image soumise
    
class Identification(models.Model):
    especetrouve = models.CharField(max_length=20, null = True)
    niveau_correspondance = models.FloatField(null = True)
    id_soumission = models.OneToOneField(Soumission, on_delete=models.PROTECT,null = True)
    id_infoEspece = models.ForeignKey(InfoEspeces, on_delete=models.PROTECT, null = True)
