"""
URL configuration for coderr project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from coderr_auth_app.api.views import RegistrationView, LoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('coderr_app.api.urls')),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/registration/', RegistrationView.as_view(), name='registration'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


"""
URLs der API:

### Admin

- **GET /admin/**: Zugriff auf das Django Admin-Interface für die Verwaltung der Anwendung.

### Authentifizierung

- **POST /api/login/**: Authentifiziert einen Benutzer und gibt ein Authentifizierungstoken zurück.
- **POST /api/registration/**: Registriert einen neuen Benutzer und erstellt dessen Profil.

### API-Module

- **/api/**: Basisroute für alle API-Endpunkte der Anwendung. Weitere spezifische Endpunkte wie Benutzerprofile, Angebote, Bestellungen und Bewertungen sind unter dieser Route verfügbar (definiert in `coderr_app.api.urls`).

### Medien

- **/media/**: Dynamische Route für den Zugriff auf Medien-Dateien, die in der Anwendung hochgeladen wurden (z.B. Profilbilder).
"""