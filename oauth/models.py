from django.db import models
from django.core.validators import FileExtensionValidator

from base.services import get_path_upload_profile_image, validate_image_size


class AuthUser(models.Model):
    """User model"""
    nickname = models.CharField(max_length=25, unique=True)
    email = models.EmailField(unique=True)
    join_date = models.DateTimeField(auto_now_add=True)
    country = models.CharField(max_length=30, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    profile_image = models.ImageField(
        upload_to=get_path_upload_profile_image, 
        blank=True, 
        null=True, 
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg']),
            validate_image_size
        ]
    )
    
    @property
    def is_authenticated():
        return True
    
    def __str__(self) -> str:
        return self.email


class Follower(models.Model):
    """Follower model"""
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name='owner')
    subscriber = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name='subscribers')

    def __str__(self) -> str:
        return f"{self.user} is subscribed to {self.subscriber}"
    

class SocialLink(models.Model):
    """User social links model"""
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name='social_links')
    link = models.URLField(max_length=100)

    def __str__(self) -> str:
        return self.user
