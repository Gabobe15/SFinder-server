from knox.auth import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

class KnoxCookieAuthentication(TokenAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get('auth_token')
        
        if not token:
            return None
        
        user, auth_token = self.authenticate_credentials(token)
        if not user:
            raise AuthenticationFailed('Invalid token')
        return user, auth_token
        