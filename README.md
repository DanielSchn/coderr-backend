# Backend for JOIN Project

Ein Test-Projekt zum erlernen der Permissions und der Authentication im Django-Restframework.

## Funktionen
- User registrieren mit Name, Mail und Passwort.

## Voraussetzungen
- Python (Version 3.x)
- Django (Version und zusätzliche Pakete siehe requirements.txt)

Alles benötigte kann über die requirements.txt installiert werden. (Siehe Punkt 3)

## Installation
### 1. Projekt klonen
```
git clone git@github.com:DanielSchn/market_hub.git
cd market_hub
```
### 2. Virtual Environment erstellen
Virtuelles Python-Umfeld erstellen und aktivieren
```
python -m venv env
source env/bin/activate # Linux/Mac
"env/Scripts/activate"
```
### 3. Abhängigkeiten installieren
```
pip install -r requirements.txt
```
### 4. Django-Projekt initialisieren
Datenbank migrieren und Server starten
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
Projekt läuft, je nach Konfiguration, unter `http://127.0.0.1:8000`.
### 5. Superuser (Admin) erstellen
In die Python Shell gehen. Dafür folgende Befehle im Terminal ausführen:
```
python manage.py shell
```
Import der models
```
from django.contrib.auth.models import User
from coderr_app.models import UserProfile
```
Erstellen des Superuser. **Bitte die Angaben email, password auf die eigenen Bedürfnisse abändern!** Location, Telefon usw. kann nach Bedarf geändert werden. Zum testen kann es so belassen werden wie angegeben.
```
superuser = User.objects.create_superuser(username='admin', email='admin@example.com', password='securepassword')
user_profile = UserProfile.objects.create(user=superuser, location='Berlin', tel='1234567890', description='This is the admin profile.', working_hours='9 AM - 5 PM', type='staff', email=superuser.email)
```

## Konfiguration
In der Datei `settings.py` wurden einige wichtige Einstellungen vorgenommen, um das Projekt lokal auszuführen:
```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'market_app',
    'rest_framework.authtoken',
    'user_auth_app',
]
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ]
}
```
Diese Einstellungen ermöglichen 'Permissions' und die 'Authentication'.

## Nutzung
Nachdem der Server läuft, kannst du die API verwenden, um Posts zu erstellen, zu liken, zu kommentieren und den Feed anzusehen. Hier einige nützliche Befehle:

- Starte den Entwicklungsserver:
```
python manage.py runserver
```
- Migriere die Datenbank:
```
python manage.py makemigrations
python manage.py migrate
```

## Deployment
Für dieses Projekt gibt es derzeit keine spezifischen Deployment-Anweisungen.

## Lizenz
Dieses Projekt wurde als Teil eines Lernprojekts erstellt und steht ohne spezifische Lizenz zur Verfügung.
