from rest_framework import serializers
from coderr_app.models import UserProfile
from django.contrib.auth.models import User


class UserProfileSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    username = serializers.CharField(source='user.username')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')    
    class Meta:
        model = UserProfile
        fields = [
            'user', 'file', 'location', 'tel', 'description',
            'working_hours', 'type', 'email', 'created_at', 'username',
            'first_name', 'last_name'
        ]
        read_only_fields = ['created_at']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        file_path = str(instance.file)
        if file_path.startswith('http://') or file_path.startswith('https://'):
            representation['file'] = file_path[file_path.index('/media/'):]
        else:
            representation['file'] = file_path

        return representation

    def update(self, instance, validated_data):

        user_data = validated_data.pop('user', None)
        instance = super().update(instance, validated_data)

        if user_data:
            user = instance.user
            user.username = user_data.get('username', user.username)
            user.first_name = user_data.get('first_name', user.first_name)
            user.last_name = user_data.get('last_name', user.last_name)
            user.save()

        return instance