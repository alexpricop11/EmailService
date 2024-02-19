from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import CustomUser
from users.serializers import UserRegistrationSerializers, UserLoginSerializers


class UserRegisterView(APIView):
    serializer_class = UserRegistrationSerializers
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "User registered successfully",
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    serializer_class = UserLoginSerializers
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                user = None
            if user:
                authenticated_user = authenticate(email=email, password=password)
                token = AccessToken.for_user(authenticated_user)
                return Response({
                    "email": authenticated_user.email,
                    "message": "User logged in successfully",
                    "token": str(token)
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"error": "No user found with this email address"}, status=status.HTTP_404_NOT_FOUND)
