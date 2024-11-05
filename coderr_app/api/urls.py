from django.contrib import admin
from django.urls import path, include
from .views import UserProfileDetailView, BusinessProfilesViewSet, CustomerProfilesViewSet, OffersViewSet, OfferDetailsViewSet, OrdersViewSet, InProgressOrderCountView, CompletedOrderCountView, ReviewsViewSet, BaseInfoView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'profiles/business', BusinessProfilesViewSet, basename='business-profiles')
router.register(r'profiles/customer', CustomerProfilesViewSet, basename='customer-profiles')
router.register(r'offerdetails', OfferDetailsViewSet, basename='offerdetails')
router.register(r'offers', OffersViewSet, basename='offers')
router.register(r'orders', OrdersViewSet, basename='orders')
router.register(r'reviews', ReviewsViewSet, basename='reviews')


urlpatterns = [
    path('', include(router.urls)),
    path('profile/<int:pk>/', UserProfileDetailView.as_view(), name='profile-detail'),
    path('order-count/<int:business_user_id>/', InProgressOrderCountView.as_view(), name='order-count'),
    path('completed-order-count/<int:business_user_id>/', CompletedOrderCountView.as_view(), name='completed-order-count'),
    path('base-info/', BaseInfoView.as_view(), name='base-info')
]


"""
URLs der API:

### Benutzerprofile

- **GET /profiles/business/**: Gibt eine Liste aller Business-Profile zurück.
- **GET /profiles/customer/**: Gibt eine Liste aller Kundenprofile zurück.

### Angebote

- **GET /offers/**: Gibt eine Liste aller Angebote zurück.
- **POST /offers/**: Erstellt ein neues Angebot.
- **PATCH /offers/{id}/**: Aktualisiert ein spezifisches Angebot.

### Angebotsdetails

- **GET /offerdetails/**: Gibt eine Liste aller Angebotsdetails zurück.
- **GET /offerdetails/{id}/**: Gibt die Details eines spezifischen Angebots zurück.

### Bestellungen

- **GET /orders/**: Gibt eine Liste aller Bestellungen zurück.
- **POST /orders/**: Erstellt eine neue Bestellung.
- **PATCH /orders/{id}/**: Aktualisiert eine spezifische Bestellung.
- **GET /orders/{id}/**: Gibt die Details einer spezifischen Bestellung zurück.
- **GET /order-count/{business_user_id}/**: Gibt die Anzahl der offenen Bestellungen für einen bestimmten Geschäftsnutzer zurück.
- **GET /completed-order-count/{business_user_id}/**: Gibt die Anzahl der abgeschlossenen Bestellungen für einen bestimmten Geschäftsnutzer zurück.

### Bewertungen

- **GET /reviews/**: Gibt eine Liste aller Bewertungen zurück.
- **POST /reviews/**: Erstellt eine neue Bewertung.
- **PATCH /reviews/{id}/**: Aktualisiert eine spezifische Bewertung.

### Basisinformationen

- **GET /base-info/**: Gibt Basisinformationen der Anwendung zurück.
"""