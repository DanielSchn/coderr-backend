from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from .views import UserProfileDetailView, BusinessProfilesViewSet, CustomerProfilesViewSet, OffersViewSet, OfferDetailsViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'profiles/business', BusinessProfilesViewSet, basename='business-profiles')
router.register(r'profiles/customer', CustomerProfilesViewSet, basename='customer-profiles')
router.register(r'offerdetails', OfferDetailsViewSet, basename='offerdetails')
router.register(r'offers', OffersViewSet, basename='offers')

urlpatterns = [
    path('', include(router.urls)),
    path('profile/<int:pk>/', UserProfileDetailView.as_view(), name='profile-detail'),
]