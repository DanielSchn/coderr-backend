from rest_framework import generics, viewsets, filters
from coderr_app.models import UserProfile, OfferDetails, Offers
from .serializers import UserProfileSerializer, OfferDetailsSerializer, OffersSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrAdmin, IsBusinessUserOrAdmin
from .paginations import LargeResultsSetPagination
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, NumberFilter
from django.db.models import Min, Max, Subquery, OuterRef
import django_filters


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
    

class OfferFilter(django_filters.FilterSet):
    max_delivery_time = django_filters.NumberFilter(method='filter_by_max_delivery_time')

    class Meta:
        model = Offers
        fields = ['max_delivery_time']

    def filter_by_max_delivery_time(self, queryset, name, value):
        return queryset.filter(max_delivery_time__lte=value)
    
    

class OffersViewSet(viewsets.ModelViewSet):
    permission_classes = [IsBusinessUserOrAdmin]
    serializer_class = OffersSerializer
    queryset = Offers.objects.all()
    pagination_class = LargeResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = OfferFilter
    ordering_fields = ['min_price', 'created_at', 'max_delivery_time']
    ordering = ['created_at']
    search_fields = ['title', 'description']

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)

    def get_queryset(self):
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
    permission_classes = [IsAuthenticated]
    serializer_class = OfferDetailsSerializer
    queryset = OfferDetails.objects.all()