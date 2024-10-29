from rest_framework import serializers
from coderr_app.models import UserProfile, OfferDetails, Offers, Orders
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk', 'username', 'first_name', 'last_name']


class UserProfileSerializer(serializers.ModelSerializer):

    user = UserSerializer()
    username = serializers.CharField(source='user.username')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')    
    class Meta:
        model = UserProfile
        fields = [
            'user', 'file', 'location', 'tel', 'description',
            'working_hours', 'type', 'email', 'created_at', 'username',
            'first_name', 'last_name', 'pk'
        ]
        read_only_fields = ['created_at']


    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation['pk'] = instance.user.id
        
        if instance.file:
            file_url = str(instance.file.url)
            if '/media/' in file_url:
                representation['file'] = file_url[file_url.index('media/'):]
            else:
                representation['file'] = None
        
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
        fields = ['id', 'url', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['url'] = f'/offerdetails/{instance.id}/'
        
        return representation
    

class OffersSerializer(serializers.ModelSerializer):
    details = OfferDetailsSerializer(many=True)
    min_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    min_delivery_time = serializers.IntegerField(read_only=True)
    max_delivery_time = serializers.IntegerField(read_only=True)
    user_details = serializers.SerializerMethodField()
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Offers
        fields = ['id', 'user', 'title', 'image', 'description', 'created_at', 'updated_at', 'details', 'min_delivery_time', 'min_price', 'user_details', 'max_delivery_time']

    def create(self, validated_data):
        # print(validated_data)
        details_data = validated_data.pop('details')
        validated_data['user'] = self.context['request'].user
        offer = Offers.objects.create(**validated_data)

        for detail in details_data:
            if 'price' not in detail:
                raise serializers.ValidationError({'details': ['Jedes Detail muss einen Preis haben!']})
            OfferDetails.objects.create(offer=offer, **detail)

        return offer
    
    def update(self, instance, validated_data):
        details_data = validated_data.pop('details', None)
        instance.title = validated_data.get('title', instance.title)
        instance.image = validated_data.get('image', instance.image)
        instance.description = validated_data.get('description', instance.description)
        instance.save()

        if details_data:
            instance.details.all().delete()

            for detail in details_data:
                OfferDetails.objects.create(offer=instance, **detail)

        return instance

    def get_user_details(self, obj):
        return {
            'first_name': obj.user.first_name,
            'last_name': obj.user.last_name,
            'username': obj.user.username,
        }
    

class OrdersSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='offer.title', required=False)
    revisions = serializers.IntegerField(source='offer_details.revisions', required=False)
    delivery_time_in_days = serializers.IntegerField(source='offer_details.delivery_time_in_days', required=False)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, source='offer_details.price', required=False)
    features= serializers.JSONField(source='offer_details.fetures', required=False)
    offer_type = serializers.CharField(source='offer_details.offer_type', required=False)

    class Meta:
        model = Orders
        fields = [
            'id', 'customer_user', 'business_user', 'title', 'revisions', 'delivery_time_in_days', 
            'price', 'features', 'offer_type', 'status', 'created_at', 'updated_at'
        ]

        extra_kwargs = {
            'customer_user': {'read_only': True},
            'business_user': {'read_only': True},
            'title': {'read_only': True},
            'revisions': {'read_only': True},
            'delivery_time_in_days': {'read_only': True},
            'price': {'read_only': True},
            'features': {'read_only': True},
            'offer_type': {'read_only': True},
            'status': {'required': False},
        }