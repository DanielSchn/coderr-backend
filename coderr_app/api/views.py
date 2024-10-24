from rest_framework import generics, viewsets, filters
from coderr_app.models import UserProfile, OfferDetails, Offers
from .serializers import UserProfileSerializer, OfferDetailsSerializer, OffersSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrAdmin
from .paginations import LargeResultsSetPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Min


class UserProfileDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsOwnerOrAdmin]

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    
class BusinessProfilesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(type='business')
    

class CustomerProfilesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(type='customer')
    
    

class OffersViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = OffersSerializer
    queryset = Offers.objects.all()
    pagination_class = LargeResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['min_price', 'created_at']
    ordering = ['created_at']
    search_fields = ['title', 'description']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        min_price = self.request.query_params.get('min_price')
        if min_price:
            queryset = queryset.filter(min_price__gte=min_price)
        return queryset


class OfferDetailsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = OfferDetailsSerializer
    queryset = OfferDetails.objects.all()