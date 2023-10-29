from rest_framework import serializers

from .models import AuthUser, SocialLink


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUser
        fields = ('nickname', 'profile_image', 'country', 'city',)


class SocialLinkSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    
    class Meta:
        model = SocialLink
        fields = ('id', 'link')


class AuthorSerializer(serializers.ModelSerializer):
    social_links = SocialLinkSerializer(many=True)

    class Meta:
        model = AuthUser
        fields = ('id', 'nickname', 'profile_image', 'country', 'city', 'social_links')
