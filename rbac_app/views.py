from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminUser, IsModeratorUser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class RegisterView(APIView):
    @swagger_auto_schema(
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email')
        },
        required=['username', 'password', 'email']
    ),
    responses=
    {
        201: 'User registered successfully',
        400: 'Invalid data'
    })
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    @swagger_auto_schema(
    responses=
    {
        201: 'User logged out successfully',
        400: 'Something went wrong'
    })

    def post(self, request):
        try:
            token = RefreshToken(request.data.get("refresh"))
            token.blacklist()
            return Response({"message": "User logged out successfully"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AdminDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    @swagger_auto_schema(
    responses=
    {
        200: 'Welcome to the Admin Dashboard'
    })
    def get(self, request):
        return Response({"message": "Welcome to the Admin Dashboard"}, status=status.HTTP_200_OK)


class ModeratorToolsView(APIView):
    permission_classes = [IsAuthenticated, IsModeratorUser]

    @swagger_auto_schema(
    responses=
    {
        200: 'Welcome to the Moderator Tools'
    })

    def get(self, request):
        return Response({"message": "Welcome to the Moderator Tools"}, status=status.HTTP_200_OK)
    