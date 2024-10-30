from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from .views import UserProfileDetailView, BusinessProfilesViewSet, CustomerProfilesViewSet, OffersViewSet, OfferDetailsViewSet, OrdersViewSet, InProgressOrderCountView, CompletedOrderCountView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'profiles/business', BusinessProfilesViewSet, basename='business-profiles')
router.register(r'profiles/customer', CustomerProfilesViewSet, basename='customer-profiles')
router.register(r'offerdetails', OfferDetailsViewSet, basename='offerdetails')
router.register(r'offers', OffersViewSet, basename='offers')
router.register(r'orders', OrdersViewSet, basename='orders')

urlpatterns = [
    path('', include(router.urls)),
    path('profile/<int:pk>/', UserProfileDetailView.as_view(), name='profile-detail'),
    path('order-count/<int:business_user_id>/', InProgressOrderCountView.as_view(), name='order-count'),
    path('completed-order-count/<int:business_user_id>/', CompletedOrderCountView.as_view(), name='completed-order-count'),
]