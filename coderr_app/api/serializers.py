from rest_framework import serializers
from coderr_app.models import UserProfile, OfferDetails, Offers, Orders, Reviews
from django.contrib.auth.models import User


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer für das UserProfile-Modell.
    
    Fügt zusätzliche Felder aus dem User-Modell hinzu, wie username, first_name und last_name.
    
    Attributes:
        user (PrimaryKeyRelatedField): Benutzer, dem das Profil gehört.
        username (CharField): Benutzername des zugehörigen Benutzers.
        first_name (CharField): Vorname des Benutzers.
        last_name (CharField): Nachname des Benutzers.
    
    Meta:
        model: UserProfile
        fields: alle relevanten Felder.
    """
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
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
        """
        Anpassung der Ausgabe, um das Feld 'file' zu bereinigen und das `pk` zu überschreiben.
        """
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
        """
        Erlaubt Updates der Benutzerinformationen durch das verschachtelte User-Modell.
        """
        user_data = validated_data.pop('user', None)
        instance = super().update(instance, validated_data)

        if user_data:
            user = instance.user
            user.username = user_data.get('username', user.username)
            user.first_name = user_data.get('first_name', user.first_name)
            user.last_name = user_data.get('last_name', user.last_name)
            user.save()

        return instance
    

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer für das User-Modell, um Benutzerbasisinformationen bereitzustellen.
    
    Attributes:
        file (SerializerMethodField): Gibt die URL des Profilbildes zurück, falls vorhanden.
    
    Meta:
        model: User
        fields: Benutzer-ID, username, first_name, last_name und file.
    """
    file = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['pk', 'username', 'first_name', 'last_name', 'file']

    def get_file(self, obj):
        """
        Gibt die URL des Profilbildes zurück, wenn vorhanden.
        """
        user_profile = UserProfile.objects.filter(user=obj).first()
        return user_profile.file.url if user_profile and user_profile.file else None


class UserProfileDetailSerializer(serializers.ModelSerializer):
    """
    Detail-Serializer für UserProfile mit eingebetteten User-Daten.
    
    Attributes:
        user (UserSerializer): Eingebetteter Serializer für Benutzerinformationen.
    
    Meta:
        model: UserProfile
        fields: Alle relevanten Felder, einschließlich der eingebetteten Benutzerinformationen.
    """
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = [
            'user', 'file', 'location', 'tel', 'description',
            'working_hours', 'type', 'email', 'created_at', 'pk'
        ]
        read_only_fields = ['created_at']

    def to_representation(self, instance):
        """
        Anpassung der Darstellung des Profilbilds.
        """
        representation = super().to_representation(instance)
        representation['pk'] = instance.user.id
        
        if instance.file:
            file_url = str(instance.file.url)
            if '/media/' in file_url:
                representation['file'] = file_url[file_url.index('media/'):]
            else:
                representation['file'] = None
        
        return representation
    

class CustomerProfileDetailSerializer(UserProfileDetailSerializer):
    """
    Serializer für Kundenprofile, der das `created_at`-Feld als `uploaded_at` zurückgibt.

    Meta:
        model (UserProfile): Modell des Kundenprofils.
        fields (list): Felder des Kundenprofils, inklusive `user`, `file`, `type`, und `created_at`.

    Methods:
        to_representation(instance): Passt die Darstellung an, um `created_at` in `uploaded_at` umzubenennen.
    """
    class Meta:
        model = UserProfile
        fields = ['user', 'file', 'created_at', 'type']


class OfferDetailsSerializer(serializers.ModelSerializer):
    """
    Serializer für das OfferDetails-Modell, das Details und den Link zu einzelnen Angebotsdetails bereitstellt.
    
    Meta:
        model: OfferDetails
        fields: Alle relevanten Felder des Angebotsdetails.
    """
    class Meta:
        model = OfferDetails
        fields = ['id', 'url', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']

    def to_representation(self, instance):
        """
        Fügt eine URL zum Angebotsdetail hinzu.
        """
        representation = super().to_representation(instance)
        representation['url'] = f'/offerdetails/{instance.id}/'

        representation['price'] = float(instance.price)
        
        return representation
    

class OffersSerializer(serializers.ModelSerializer):
    """
    Serializer für das Offers-Modell, inklusive Details und Benutzerinformationen.
    
    Attributes:
        details (OfferDetailsSerializer): Serializer für Angebotsdetails.
        min_price (DecimalField): Minimaler Preis des Angebots.
        min_delivery_time (IntegerField): Minimale Lieferzeit des Angebots.
        max_delivery_time (IntegerField): Maximale Lieferzeit des Angebots.
        user_details (SerializerMethodField): Informationen über den Benutzer, der das Angebot erstellt hat.
        user (PrimaryKeyRelatedField): Der Benutzer, der das Angebot erstellt hat.
    
    Meta:
        model: Offers
        fields: Alle relevanten Felder des Angebots.
    """
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
        """
        Erstellt ein neues Angebot mit Validierung und Details.
        """
        details_data = validated_data.pop('details')
        validated_data['user'] = self.context['request'].user
        offer = Offers.objects.create(**validated_data)

        for detail in details_data:
            if 'price' not in detail:
                raise serializers.ValidationError({'details': ['Jedes Detail muss einen Preis haben!']})
            OfferDetails.objects.create(offer=offer, **detail)

        return offer
    
    def update(self, instance, validated_data):
        """
        Aktualisiert das Angebot und seine Details.
        """
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
        """
        Gibt Benutzerdetails zurück, die das Angebot erstellt haben.
        """
        return {
            'first_name': obj.user.first_name,
            'last_name': obj.user.last_name,
            'username': obj.user.username,
        }
    

class OrdersSerializer(serializers.ModelSerializer):
    """
    Serializer für das Orders-Modell mit Feldern, die aus verbundenen Offer- und OfferDetails-Modellen abgeleitet sind.
    
    Attributes:
        title (CharField): Titel des Angebots.
        revisions (IntegerField): Anzahl der Revisionen des Angebots.
        delivery_time_in_days (IntegerField): Lieferzeit des Angebots.
        price (DecimalField): Preis des Angebots.
        features (JSONField): Funktionen des Angebots.
        offer_type (CharField): Typ des Angebots.
    
    Meta:
        model: Orders
        fields: Alle relevanten Felder des Auftrags.
    """
    title = serializers.CharField(source='offer.title', required=False)
    revisions = serializers.IntegerField(source='offer_details.revisions', required=False)
    delivery_time_in_days = serializers.IntegerField(source='offer_details.delivery_time_in_days', required=False)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, source='offer_details.price', required=False)
    features= serializers.JSONField(source='offer_details.features', required=False)
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


class ReviewsSerializer(serializers.ModelSerializer):
    """
    Serializer für das Reviews-Modell, das Bewertungen von Benutzern für Business-Anbieter darstellt.
    
    Attributes:
        reviewer (PrimaryKeyRelatedField): Der Benutzer, der die Bewertung abgegeben hat.
    
    Meta:
        model: Reviews
        fields: Alle relevanten Felder der Bewertung.
    """
    reviewer = serializers.PrimaryKeyRelatedField(source='customer_user', read_only=True)
    class Meta:
        model = Reviews
        fields = ['id', 'business_user', 'reviewer', 'rating', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'customer_user']

    def create(self, validated_data):
        """
        Erstellt eine neue Bewertung für einen Business-Benutzer.
        """
        customer_user = validated_data.pop('customer_user')
        review = Reviews.objects.create(customer_user=customer_user, **validated_data)
        return review