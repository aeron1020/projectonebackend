from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import NewUserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
    
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        reg_serializer = NewUserSerializer(data=request.data)

        if reg_serializer.is_valid():
            password = request.data.get('password') 
            if not self.validate_password_strength(password):
                return Response({"password": ["Password must be at least 8 characters long."]}, status=status.HTTP_400_BAD_REQUEST)
            
            new_user = reg_serializer.save()
            if new_user:
                return Response(status=status.HTTP_201_CREATED)

        return Response(reg_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def validate_password_strength(self, password):
        """
        Validates password strength.
        """
        if len(password) < 8:
            return False
        return True
    
class BlacklistTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        

