from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from .models import CustomUser
from .renderers import UserJSONRenderer
from .serializers import UserListSerializer, UserSerializer

# Create your views here.


class UserListApiView(ListAPIView):
    model = CustomUser
    queryset = CustomUser.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # renderer_classes = [UserJSONRenderer]
    serializer_class = UserListSerializer


class UserDetailsView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()

