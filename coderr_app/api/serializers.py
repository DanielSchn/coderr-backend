from rest_framework import serializers
from coderr_app.models import UserProfile, OfferDetails, Offers
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
        
        file_url = str(instance.file.url)
        if '/media/' in file_url:
            representation['file'] = file_url[file_url.index('media/'):]
        
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
    

class OfferDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = OfferDetails
        fields = ['id', 'url']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['url'] = f'/offerdetails/{instance.id}/'
        
        return representation
    

class OffersSerializer(serializers.ModelSerializer):
    details = OfferDetailsSerializer(many=True, read_only=True)
    min_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    min_delivery_time = serializers.IntegerField(read_only=True)
    user_details = serializers.SerializerMethodField()

    class Meta:
        model = Offers
        fields = ['id', 'user', 'title', 'image', 'description', 'created_at', 'updated_at', 'details', 'min_price', 'min_delivery_time', 'user_details']

    def get_user_details(self, obj):
        return {
            'first_name': obj.user.first_name,
            'last_name': obj.user.last_name,
            'username': obj.user.username
        }