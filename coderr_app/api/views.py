from rest_framework import generics, viewsets
from coderr_app.models import UserProfile
from .serializers import UserProfileSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrAdmin


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