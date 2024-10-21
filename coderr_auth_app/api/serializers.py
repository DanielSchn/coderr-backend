from rest_framework import serializers
from django.contrib.auth.models import User


class RegistrationSerializer(serializers.ModelSerializer):

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
        
    # def validate(self, value):
    #     print('validate username')
    #     username_exists = User.objects.filter(username=value.get('username')).exists()
    #     if username_exists:
    #         raise serializers.ValidationError({'username': ['Dieser Benutzername ist bereits vergeben.']})
    #     return value


    def save(self):
        print('save method')
        pw = self.validated_data['password']
        repeated_pw = self.validated_data['repeated_password']
        username_exists = User.objects.filter(username=self.validated_data['username']).exists()
        email_exists = User.objects.filter(email=self.validated_data['email']).exists()

        if pw != repeated_pw:
            raise serializers.ValidationError({'password': ['Das Passwort ist nicht gleich mit dem wiederholten Passwort']})
        if username_exists:
            print('if username')
            raise serializers.ValidationError({'username': ['Dieser Benutzername ist bereits vergeben.']})
        if email_exists:
            raise serializers.ValidationError({'email': ['Diese E-Mail-Adresse wird bereits verwendet']})
        
        account = User(email=self.validated_data['email'], username=self.validated_data['username'])
        account.set_password(pw)
        account.save()

        return account