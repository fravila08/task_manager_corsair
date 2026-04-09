from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions

class CookieAuthentication(TokenAuthentication):
        
        def get_auth_cookie(self, request):
             return request.COOKIES.get('token')
    
        def authenticate(self, request):
            auth = self.get_auth_cookie(request)

            if not auth:
                  raise exceptions.AuthenticationFailed("Authentication Cookie is not present")
            
            return self.authenticate_credentials(auth)