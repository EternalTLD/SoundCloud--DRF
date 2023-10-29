from rest_framework import viewsets, parsers, permissions

from ...base.permissions import IsAuthor
from ..serializers import UserSerializer, AuthorSerializer, SocialLinkSerializer
from ..models import AuthUser


class UserView(viewsets.ModelViewSet):
    """Viewing and editing user data"""
    parser_classes = (parsers.MultiPartParser,)
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user
    
    def get_object(self):
        return self.get_queryset()
    

class AuthorView(viewsets.ReadOnlyModelViewSet):
    """Author list"""
    queryset = AuthUser.objects.all().prefetch_related('social_links')
    serializer_class = AuthorSerializer


class SocialLinksView(viewsets.ModelViewSet):
    """CRUD users social links"""
    serializer_class = SocialLinkSerializer
    permission_classes = [IsAuthor]

    def get_queryset(self):
        return self.request.user.social_links.all()
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)