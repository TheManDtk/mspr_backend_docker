import tensorflow as tf
from PIL import Image
import numpy as np
import io
import os
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)

# Chemin vers le modèle sauvegardé
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'best_model_20240521_214333.h5')
# Impression du chemin du modèle pour vérification
logging.info(f"Le chemin du modèle est : {MODEL_PATH}")
# Chargement du modèle
model = None
try:
    if os.path.exists(MODEL_PATH):
        model = tf.keras.models.load_model(MODEL_PATH)
        logging.info("Modèle chargé avec succès.")
    else:
        logging.error(f"Le fichier modèle {MODEL_PATH} n'existe pas.")
except Exception as e:
    logging.error(f"Erreur lors du chargement du modèle : {e}")

# Classes d'espèces
CLASSES = [
    'Castor', 'Chat', 'Chien', 'Coyote', 'Ecureuil', 
    'Loup', 'Lynx', 'Ours', 'Puma', 'Raton Laveur', 
    'Renard', 'background'
]

def preprocess_image(image):
    """
    Redimensionne l'image et normalise les valeurs des pixels.
    """
    try:
        # Redimensionnement de l'image à la taille requise par le modèle
        image = image.resize((224, 224))
        # Conversion de l'image en tableau numpy et normalisation
        image_array = np.array(image) / 255.0
        # Expansion de la dimension pour correspondre aux entrées du modèle
        return np.expand_dims(image_array, axis=0)
    except Exception as e:
        logging.error(f"Erreur lors du préprocessing de l'image : {e}")
        raise

def predict_image(image):
    """
    Prédiction de l'espèce présente dans l'image.
    """
    global model
    try:
        # Lecture de l'image depuis l'objet BytesIO
        image = Image.open(io.BytesIO(image.read()))
        # Conversion de l'image en RGB si nécessaire
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Prétraitement de l'image
        preprocessed_image = preprocess_image(image)
        
        # Prédiction
        predictions = model.predict(preprocessed_image)
        
        # Identification de l'espèce et de la probabilité associée
        espece_index = np.argmax(predictions)
        espece = CLASSES[espece_index]
        probabilite = predictions[0][espece_index]
        
        return espece, probabilite
    except Exception as e:
        logging.error(f"Erreur lors de la prédiction de l'image : {e}")
        raise
