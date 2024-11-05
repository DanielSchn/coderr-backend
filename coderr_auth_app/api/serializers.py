from rest_framework import serializers
from django.contrib.auth.models import User
from coderr_app.models import UserProfile


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer für die Benutzerregistrierung.

    Dieser Serializer verarbeitet die Eingabedaten für die Registrierung eines neuen Benutzers. 
    Er führt Validierungen durch, um sicherzustellen, dass der Benutzername und die E-Mail-Adresse 
    eindeutig sind und dass die angegebenen Passwörter übereinstimmen.

    **Felder**:
    - `username`: Der gewünschte Benutzername des neuen Benutzers. Muss eindeutig sein.
    - `email`: Die E-Mail-Adresse des neuen Benutzers. Muss ebenfalls eindeutig sein.
    - `password`: Das Passwort des neuen Benutzers. Wird verschlüsselt gespeichert.
    - `repeated_password`: Eine zusätzliche Eingabe für die Passwortbestätigung.
    - `type`: Der Typ des Benutzerprofils (z.B. 'customer' oder 'business').

    **Beispiel-Request**:
    ```json
    {
        "username": "neuerBenutzer",
        "email": "benutzer@example.com",
        "password": "sicheresPasswort",
        "repeated_password": "sicheresPasswort",
        "type": "customer"
    }
    ```

    **Beispiel-Response (201)**:
    ```json
    {
        "username": "neuerBenutzer",
        "email": "benutzer@example.com"
    }
    ```

    **Beispiel-Response (400)**:
    ```json
    {
        "username": ["Bitte prüfe deine Eingaben. Email und/oder Benutzername bereits vergeben."],
        "password": ["Die Passwörter sind nicht identisch."]
    }
    ```

    **Validierungen**:
    - `validate_unique_username`: Überprüft, ob der angegebene Benutzername bereits existiert. Wenn ja, wird ein Fehler ausgegeben.
    - Die Passwörter müssen identisch sein. Wenn nicht, wird ein Fehler ausgegeben.
    - Die E-Mail-Adresse muss ebenfalls eindeutig sein.

    **Zugriffsrechte**: 
    - Jeder Benutzer kann diese Ansicht aufrufen (AllowAny).
    """

    def validate_unique_username(value):
        """
        Validiert, ob der Benutzername eindeutig ist.

        :param value: Der eingegebene Benutzername.
        :raises serializers.ValidationError: Wenn der Benutzername bereits vergeben ist.
        :return: Den eingegebenen Benutzernamen, wenn er eindeutig ist.
        """
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Bitte prüfe deine Eingaben. Email und/oder Benutzername bereits vergeben.')
        return value

    username = serializers.CharField(validators=[validate_unique_username])
    repeated_password = serializers.CharField(write_only=True)
    type = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'repeated_password', 'type']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }


    def save(self):
        """
        Speichert den neuen Benutzer und das zugehörige Benutzerprofil.

        Diese Methode wird aufgerufen, wenn der Serializer erfolgreich validiert wurde. 
        Sie erstellt einen neuen Benutzer und ein zugehöriges Benutzerprofil.

        :raises serializers.ValidationError: Wenn die Passwörter nicht übereinstimmen 
                                               oder die E-Mail bereits existiert.
        :return: Das neu erstellte Benutzerobjekt.
        """
        pw = self.validated_data['password']
        repeated_pw = self.validated_data['repeated_password']
        email_exists = User.objects.filter(email=self.validated_data['email']).exists()

        if pw != repeated_pw:
            raise serializers.ValidationError({'password': ['Die Passwörter sind nicht identisch.']})
        if email_exists:
            raise serializers.ValidationError({'error': ['Bitte prüfe deine Eingaben. Email und/oder Benutzername bereits vergeben.']})
        
        account = User(email=self.validated_data['email'], username=self.validated_data['username'])
        account.set_password(pw)
        account.save()

        UserProfile.objects.create(
            user=account,
            email=self.validated_data['email'],
            type=self.validated_data['type']
        )

        return account