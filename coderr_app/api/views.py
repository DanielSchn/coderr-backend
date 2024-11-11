from rest_framework import generics, viewsets, filters, status
from coderr_app.models import UserProfile, OfferDetails, Offers, Orders, User, Reviews
from .serializers import UserProfileSerializer, OfferDetailsSerializer, OffersSerializer, OrdersSerializer, UserProfileDetailSerializer, ReviewsSerializer, CustomerProfileDetailSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsObjectOwnerOrAdminPermission, IsBusinessOrAdminPermission, IsCustomerReadOnlyPermission, OrderAccessPermission, IsReviewerOrAdminPermission
from .paginations import LargeResultsSetPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Min, Subquery, OuterRef
import django_filters
from rest_framework.response import Response
from rest_framework.views import APIView


class UserProfileDetailView(generics.RetrieveUpdateAPIView):
    """
    Ansicht zur Abfrage und Aktualisierung von Benutzerprofilen.

    **URL**: `/profile/{pk}/`

    **Methoden**:
    - **GET**: Ruft das Benutzerprofil mit dem angegebenen Primärschlüssel (pk) ab.
    - **PATCH**: Aktualisiert das Benutzerprofil mit dem angegebenen Primärschlüssel (pk).

    **Berechtigungen**: 
    - Der Benutzer muss der Eigentümer des Profils oder ein Administrator sein.
    """
    permission_classes = [IsObjectOwnerOrAdminPermission | IsCustomerReadOnlyPermission]

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    
class BusinessProfilesViewSet(viewsets.ModelViewSet):
    """
    ViewSet zur Verwaltung von Geschäftprofilen.

    **URL**: `/profiles/business/`

    **Methoden**:
    - **GET**: Listet alle Geschäftprofile auf.
    - **POST**: Erstellt ein neues Geschäftprofil.

    **Berechtigungen**:
    - Erfordert Authentifizierung.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileDetailSerializer

    def get_queryset(self):
        """
        Gibt nur Geschäftsbenutzerprofile zurück.
        """
        return UserProfile.objects.filter(type='business')
    

class CustomerProfilesViewSet(viewsets.ModelViewSet):
    """
    ViewSet zur Verwaltung von Kundenprofilen.

    **URL**: `/profiles/customer/`

    **Methoden**:
    - **GET**: Listet alle Kundenprofile auf.
    - **POST**: Erstellt ein neues Kundenprofil.

    **Berechtigungen**:
    - Erfordert Authentifizierung.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CustomerProfileDetailSerializer

    def get_queryset(self):
        """
        Gibt nur Kundenbenutzerprofile zurück.
        """
        return UserProfile.objects.filter(type='customer')
    

class OfferFilter(django_filters.FilterSet):
    """
    FilterSet zum Filtern von Angeboten basierend auf der Lieferzeit und dem Ersteller.
    """
    max_delivery_time = django_filters.NumberFilter(method='filter_by_max_delivery_time')
    creator_id = django_filters.NumberFilter(field_name='user__id')

    class Meta:
        model = Offers
        fields = ['max_delivery_time', 'creator_id']

    def filter_by_max_delivery_time(self, queryset, name, value):
        """
        Filtert Angebote nach maximaler Lieferzeit.
        """
        return queryset.filter(max_delivery_time__lte=value)
     

class OffersViewSet(viewsets.ModelViewSet):
    """
    ViewSet zur Verwaltung von Angeboten.

    **URL**: `/offers/`

    **Methoden**:
    - **GET**: Listet alle Angebote mit optionalen Filtern und Suchanfragen auf.
    - **POST**: Erstellt ein neues Angebot.
    - **PATCH**: Aktualisiert ein bestehendes Angebot.
    - **DELETE**: Entfernt ein Angebot.

    **Berechtigungen**:
    - Erfordert Berechtigungen für Geschäftsbenutzer oder Administratoren.
    """
    permission_classes = [IsBusinessOrAdminPermission]
    serializer_class = OffersSerializer
    queryset = Offers.objects.all()
    pagination_class = LargeResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = OfferFilter
    ordering_fields = ['min_price', 'created_at', 'max_delivery_time']
    ordering = ['created_at']
    search_fields = ['title', 'description']

    def get_serializer_context(self):
        """
        Fügt die Anfrage zum Serializer-Kontext hinzu.
        """
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_queryset(self):
        """
        Annotiert Angebote mit dem minimalen Preis und der minimalen/maximalen Lieferzeit.
        """
        min_price_subquery = OfferDetails.objects.filter(offer=OuterRef('pk')).values('offer').annotate(
            min_price=Min('price')
        ).values('min_price')

        min_delivery_time_subquery = OfferDetails.objects.filter(offer=OuterRef('pk')).values('offer').annotate(
            min_delivery_time=Min('delivery_time_in_days')
        ).values('min_delivery_time')

        return Offers.objects.annotate(
            min_price=Subquery(min_price_subquery),
            min_delivery_time=Subquery(min_delivery_time_subquery),
            max_delivery_time=Subquery(min_delivery_time_subquery)
        )


class OfferDetailsViewSet(viewsets.ModelViewSet):
    """
    ViewSet zur Verwaltung von Angebotsdetails.

    **URL**: `/offerdetails/`

    **Methoden**:
    - **GET**: Listet alle Angebotsdetails auf.
    - **POST**: Erstellt ein neues Angebotsdetail.
    - **PATCH**: Aktualisiert ein bestehendes Angebotsdetail.
    - **DELETE**: Entfernt ein Angebotsdetail.

    **Berechtigungen**:
    - Erfordert Authentifizierung.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = OfferDetailsSerializer
    queryset = OfferDetails.objects.all()


class OrdersViewSet(viewsets.ModelViewSet):
    """
    ViewSet zur Verwaltung von Bestellungen.

    **URL**: `/orders/`

    **Methoden**:
    - **GET**: Listet alle Bestellungen auf, die mit dem authentifizierten Benutzer verbunden sind.
    - **POST**: Erstellt eine neue Bestellung.
    - **PATCH**: Aktualisiert eine bestehende Bestellung.
    - **DELETE**: Entfernt eine Bestellung.

    **Berechtigungen**:
    - Benötigt benutzerdefinierte Berechtigungen für den Zugriff auf Bestellungen.
    """
    permission_classes = [OrderAccessPermission]
    serializer_class = OrdersSerializer
    queryset = Orders.objects.all()

    def get_queryset(self):
        """
        Gibt Bestellungen zurück, die mit dem authentifizierten Benutzer verbunden sind.
        """
        user = self.request.user
        if user.user_profile.type == 'staff':
            return Orders.objects.all()
        else:
            customer_orders = Orders.objects.filter(customer_user=user)
            business_orders = Orders.objects.filter(business_user=user)
            return customer_orders | business_orders

    def perform_create(self, serializer):
        """
        Erstellt eine neue Bestellung mit Details und verknüpft sie mit dem Kunden und dem Geschäftsbenutzer.

        Erfordert 'offer_detail_id' in den Anfragedaten.
        """
        offer_detail_id = self.request.data.get('offer_detail_id')

        try:
            offer_detail = OfferDetails.objects.get(id=offer_detail_id)
            offer = offer_detail.offer
            customer_user = self.request.user
            business_user = offer.user

            serializer.save(
                customer_user=customer_user,
                business_user=business_user,
                offer=offer,
                offer_details=offer_detail,
                title=offer.title,
                revisions=offer_detail.revisions,
                delivery_time_in_days=offer_detail.delivery_time_in_days,
                price=offer_detail.price,
                features=offer_detail.features,
                offer_type=offer_detail.offer_type,
                status='in_progress'
            )

        except OfferDetails.DoesNotExist:
            raise ValueError('Invalid offer_detail_id')
        
    def create(self, request, *args, **kwargs):
        """
        Überschreibt die Methode create, um spezifische Fehler elegant zu behandeln.
        """
        try:
            return super().create(request, *args, **kwargs)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class InProgressOrderCountView(APIView):
    """
    API-Ansicht zur Zählung der laufenden Bestellungen für einen Geschäftsbenutzer.

    **URL**: `/order-count/{business_user_id}/`

    **Methoden**:
    - **GET**: Ruft die Anzahl der laufenden Bestellungen für den angegebenen Geschäftsbenutzer ab.

    **Berechtigungen**:
    - Erfordert Authentifizierung.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id, *args, **kwargs):
        """
        Erhält die Anzahl der laufenden Bestellungen für einen bestimmten Geschäftsbenutzer.
        """
        if not User.objects.filter(id=business_user_id, user_profile__type='business').exists():
            return Response({'error': 'Business user not found.'}, status.HTTP_400_BAD_REQUEST)

        in_progress_count = Orders.objects.filter(
            business_user_id=business_user_id,
            status='in_progress'
        ).count()

        return Response({'order_count': in_progress_count})
    

class CompletedOrderCountView(APIView):
    """
    API-Ansicht zur Zählung der abgeschlossenen Bestellungen für einen Geschäftsbenutzer.

    **URL**: `/completed-order-count/{business_user_id}/`

    **Methoden**:
    - **GET**: Ruft die Anzahl der abgeschlossenen Bestellungen für den angegebenen Geschäftsbenutzer ab.

    **Berechtigungen**:
    - Erfordert Authentifizierung.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id, *args, **kwargs):
        """
        Erhält die Anzahl der abgeschlossenen Bestellungen für einen bestimmten Geschäftsbenutzer.
        """
        if not User.objects.filter(id=business_user_id, user_profile__type='business').exists():
            return Response({'error': 'Business user not found.'}, status.HTTP_400_BAD_REQUEST)

        completed_count = Orders.objects.filter(
            business_user_id=business_user_id,
            status='completed'
        ).count()

        return Response({'completed_order_count': completed_count})
    

class ReviewsFilter(django_filters.FilterSet):
    """
    FilterSet zum Filtern von Bewertungen.

    **Felder**:
    - **business_user_id**: ID des Geschäftsbenutzers, dessen Bewertungen abgerufen werden sollen.
    - **reviewer_id**: ID des Kunden, der die Bewertung abgegeben hat.

    **Verwendete Modelle**: Reviews
    """
    business_user_id = django_filters.NumberFilter(field_name='business_user__id')
    reviewer_id = django_filters.NumberFilter(field_name='customer_user__id')

    class Meta:
        model = Reviews
        fields = ['business_user_id', 'reviewer_id']


class ReviewsViewSet(viewsets.ModelViewSet):
    """
    ViewSet zur Verwaltung von Bewertungen.

    **URL**: `/reviews/`

    **Methoden**:
    - **GET**: Listet alle Bewertungen auf, optional gefiltert nach Geschäftsbenutzer oder Rezensenten.
    - **POST**: Erstellt eine neue Bewertung.
    - **DELETE**: Löscht eine bestehende Bewertung.

    **Berechtigungen**:
    - Der Benutzer muss entweder der Rezensent oder ein Administrator sein.
    """
    permission_classes = [IsReviewerOrAdminPermission]
    serializer_class = ReviewsSerializer
    queryset = Reviews.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ReviewsFilter
    ordering_fields = ['updated_at', 'rating']
    ordering = ['-updated_at']

    def perform_create(self, serializer):
        """
        Erstellt eine neue Bewertung und verknüpft sie mit dem authentifizierten Benutzer.

        Der Benutzer wird als `customer_user` gespeichert.
        """
        serializer.save(customer_user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        """
        Löscht die angegebene Bewertung und gibt eine leere Antwort mit dem Status 200 zurück.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class BaseInfoView(generics.ListAPIView):
    """
    API-Ansicht zur Bereitstellung grundlegender Informationen über das System.

    **URL**: `/base-info/`

    **Methoden**:
    - **GET**: Gibt grundlegende Statistiken über Benutzerprofile, Bewertungen und Angebote zurück.

    **Antwort**:
    - Anzahl der Geschäftprofile
    - Anzahl der Bewertungen
    - Anzahl der Angebote
    - Durchschnittliche Bewertung
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfile

    def _calculate_average_rating(self):
        """
        Berechnet die durchschnittliche Bewertung aller Bewertungen.

        Gibt 0 zurück, wenn keine Bewertungen vorhanden sind.
        """
        ratings = Reviews.objects.values_list('rating', flat=True)
        total_ratings = ratings.count()
        if total_ratings == 0:
            return 0
        
        return round(sum(ratings) / total_ratings, 1)

    def list(self, request):
        """
        Gibt eine Zusammenfassung der Basisinformationen zurück:
        - Anzahl der Geschäftprofile
        - Anzahl der Bewertungen
        - Anzahl der Angebote
        - Durchschnittliche Bewertung
        """
        business_profile_count = UserProfile.objects.filter(type='business').count()
        review_count = Reviews.objects.count()
        offer_count = Offers.objects.count()
        average_rating = self._calculate_average_rating()

        return Response({
            'business_profile_count': business_profile_count,
            'review_count': review_count,
            'offer_count': offer_count,
            'average_rating': average_rating
        })