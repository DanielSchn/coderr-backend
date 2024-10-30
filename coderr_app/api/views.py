from rest_framework import generics, viewsets, filters, status
from coderr_app.models import UserProfile, OfferDetails, Offers, Orders, User
from .serializers import UserProfileSerializer, OfferDetailsSerializer, OffersSerializer, OrdersSerializer, CustomerUserProfileSerializer, UserProfileDetailSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsOwnerOrAdmin, IsBusinessUserOrAdmin, IsCustomerToReadOnly, CustomOrdersPermission
from .paginations import LargeResultsSetPagination
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, NumberFilter
from django.db.models import Min, Max, Subquery, OuterRef
import django_filters
from rest_framework.response import Response
from rest_framework.views import APIView


class UserProfileDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsOwnerOrAdmin | IsCustomerToReadOnly]

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    
class BusinessProfilesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileDetailSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(type='business')
    

class CustomerProfilesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileDetailSerializer

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


class OrdersViewSet(viewsets.ModelViewSet):
    permission_classes = [CustomOrdersPermission]
    serializer_class = OrdersSerializer
    queryset = Orders.objects.all()

    def perform_create(self, serializer):
        
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
        try:
            return super().create(request, *args, **kwargs)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class InProgressOrderCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id, *args, **kwargs):
        if not User.objects.filter(id=business_user_id, user_profile__type='business').exists():
            return Response({'error': 'Business user not found.'}, status.HTTP_400_BAD_REQUEST)

        in_progress_count = Orders.objects.filter(
            business_user_id=business_user_id,
            status='in_progress'
        ).count()

        return Response({'order_count': in_progress_count})
    

class CompletedOrderCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id, *args, **kwargs):
        if not User.objects.filter(id=business_user_id, user_profile__type='business').exists():
            return Response({'error': 'Business user not found.'}, status.HTTP_400_BAD_REQUEST)

        completed_count = Orders.objects.filter(
            business_user_id=business_user_id,
            status='completed'
        ).count()

        return Response({'completed_order_count': completed_count})
    

class ReviewsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id, *args, **kwargs):
        pass