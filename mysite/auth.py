from rest_framework.authentication import BaseAuthentication
import jwt
from jwt import exceptions
class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        return super().authenticate(request)