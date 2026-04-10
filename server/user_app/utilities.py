from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework import exceptions

class CookieAuthentication(JWTAuthentication):
        
        def get_auth_cookie(self, request):
             return request.COOKIES.get('access')
    
        def authenticate(self, request):
            access_token = self.get_auth_cookie(request)

            if not access_token:
                  raise exceptions.AuthenticationFailed("Authentication Cookie is not present")
            
            try:
                  validate_token = self.get_validated_token(access_token)
                  return self.get_user(validate_token), validate_token
            except (InvalidToken, TokenError) as e:
                  raise exceptions.AuthenticationFailed(str(e))
            