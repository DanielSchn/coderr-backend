from rest_framework import generics
from coderr_app.models import UserProfile
from .serializers import UserProfileSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .permissions import IsOwnerOrAdmin


class UserProfileDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsOwnerOrAdmin]

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    