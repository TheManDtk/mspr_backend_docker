# Backend de notre projet MSPR de classification d'empreinte

Il s'agit ici du backend de notre projet MSPR de classification d'empreinte. Pour qu'il soit utilisable, il vous faut, après avoir entraîné le modèle, le télécharger et le placer dans le dossier `model_ia`.

## Configuration pour la conteneurisation

Notre application a été configurée pour être dockerisée et donc le processus de conteneurisation avec les contenus des fichiers `Dockerfile` et `docker-compose.yml`. Ces fichiers retracent la configuration pour conteneuriser notre backend.

### Dockerfile

Le fichier `Dockerfile` contient les instructions pour construire l'image Docker de notre application. Il spécifie notamment :

- La version de Python à utiliser
- Les dépendances à installer
- Les fichiers à copier dans l'image

### docker-compose.yml

Le fichier `docker-compose.yml` est utilisé pour définir et exécuter les différents services de notre application en tant que conteneurs Docker. Il spécifie notamment :

- Les images Docker à utiliser
- Les ports à ouvrir
- Les volumes à monter

Pour plus d'informations sur la conteneurisation avec Docker, vous pouvez consulter la [documentation officielle](https://docs.docker.com/).
