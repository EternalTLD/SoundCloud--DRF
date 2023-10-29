from datetime import datetime
from typing import Optional

import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed

from ..models import AuthUser


class AuthBackend(BaseAuthentication):
    authentication_header_prefix = 'Token'

    def authenticate(self, request, token=None, **kwargs) -> Optional[tuple]:
        auth_header = get_authorization_header(request).split()
        if not auth_header or auth_header[0].lower() != b'token':
            return None
        
        if len(auth_header) == 1:
            raise AuthenticationFailed('Invalid token header. No credential provided.')
        elif len(auth_header) > 2:
            raise AuthenticationFailed('Token string should not contain spaces.')

        try:
            token = auth_header[1].decode('utf-8')
        except UnicodeError:
            raise AuthenticationFailed(
                'Invalid token header. Token string should not contain invalid characters'
            )
        
        return self.authenticate_credential(token)
    
    def authenticate_credential(self, token) -> tuple:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        except jwt.PyJWTError:
            raise AuthenticationFailed('Invalid authentication. Could not decode token.')
        
        token_exp = datetime.fromtimestamp(payload['exp'])
        if token_exp < datetime.utcnow():
            raise AuthenticationFailed('Token is expired.')
        
        try:
            user = AuthUser.objects.get(id=payload['user_id'])
        except AuthUser.DoesNotExist:
            raise AuthenticationFailed('No user matching this token was found.')
        
        return user, None