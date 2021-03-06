from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from torshavn_api import serializers
from torshavn_api import models
from torshavn_api import permissions
from torshavn_api.serializers import MarkerSerializer
from torshavn_api.serializers import UserSerializer

# Create your views here.

class HelloApiView(APIView):
    """Test API View"""
    serializer_class = serializers.HelloSerializer

    def get(self, request, format=None):
        """Returns a list of APIView features"""
        an_apiview = [
            'Uses HTTP methods as function (get, post, patch, put, delete)',
            'Is similar to a traditional Django View',
            'Gives you the most control over your application logic',
            'Is mapped manually to URLS',
        ]

        return Response({'message': 'Hello!', 'an_apiview': an_apiview})

    def post(self, request):
        """Create a hello message with our name"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status = status.HTTP_400_BAD_REQUEST
                 )

    def put(self, request, pk=None):
        """Handle updating an object"""
        return Response({'method': 'PUT'})

    def patch(self, request, pk=None):
        """Handle a partial update of an object"""
        return Response({'method': 'PATCH'})
    
    def delete(self, request, pk=None):
        """Delete an object"""
        return Response({'method': 'DELETE'})

class HelloViewSet(viewsets.ViewSet):
    """Test API ViewSet"""
    serializer_class = serializers.HelloSerializer

    def list(self, request):
        """Return a hello message"""

        a_viewset = [
            'Uses actions (list, create, retrieve, update, partial_update)',
            'Automatically maps to URLs using Routers',
            'Provides more functionality with less code',
        ]

        return Response({'message': 'Hello!', 'a_viewset': a_viewset})

    def create(self, request):
        """Create a new hello message"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}!'
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def retrieve(self, request, pk=None):
        """Handle getting an object by its ID"""
        return Response({'http_method': 'GET'})

    def update(self, request, pk=None):
        """Handle updating an object"""
        return Response({'http_method': 'PUT'})

    def partial_update(self, request, pk=None):
        """Handle updating part of an object"""
        return Response({'http_method': 'PATCH'})

    def destroy(self, request, pk=None):
        """Handle removing an object"""
        return Response({'http_method': 'DELETE'})

class UserViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()
    # authentication_classes = (JSONWebTokenAuthentication,)
    # permission_classes = (
    #     permissions.UpdateOwnStatus,
    #     IsAuthenticated
    # )
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)

    # def list(self, request):
    #     queryset = self.get_queryset()
    #     serializer = UserSerializer(queryset, many=True)
    #     return Response(serializer.data)
    
    # def retrieve(self, request, pk=None):
    #     """Handle getting an object by its ID"""
    #     queryset = self.get_queryset()
    #     marker = get_object_or_404(queryset, pk=pk)
    #     serializer = MarkerSerializer(marker)
    #     return Response(serializer.data)

    def create(self, request):
        """Create a new user"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            # token = serializer.data.get('token')
            # return Response({'token': token})
            return Response({'status': 'OK'})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )    

    def update(self, request, pk=None):
        """Handle updating an object"""
        authentication_classes = (JSONWebTokenAuthentication,)
        permission_classes = (
            permissions.UpdateOwnStatus,
            IsAuthenticated
        )
        return Response({'http_method': 'PUT'})

class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentication tokens"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class UserFeedViewSet(viewsets.ModelViewSet):
    """Handles creating , reading and updating profile feed items"""
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (
        permissions.UpdateOwnStatus,
        IsAuthenticated
    )

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user"""
        serializer.save(user_profile=self.request.user)

class MarkerViewSet(viewsets.ModelViewSet):
    """Marker API ViewSet"""
    # serializer_class = serializers.MarkerSerializer
    # queryset = models.Marker.objects.all()
    # authentication_classes = (JSONWebTokenAuthentication,)
    # permission_classes = (
    #     IsAuthenticated,
    # )
    def list(self, request):
        serializer_class = serializers.MarkerSerializer
        queryset = models.Marker.objects.all()
        authentication_classes = (JSONWebTokenAuthentication,)
        permission_classes = (
            IsAuthenticated,
        )
        # queryset = self.get_queryset()
        serializer = MarkerSerializer(queryset, many=True)
        return Response(serializer.data)
    
    # def retrieve(self, request, pk=None):
    #     """Handle getting an object by its ID"""
    #     queryset = self.get_queryset()
    #     marker = get_object_or_404(queryset, pk=pk)
    #     serializer = MarkerSerializer(marker)
    #     return Response(serializer.data)

    # def create(self, request):
    #     """Create a new marker"""
    #     serializer = self.serializer_class(data=request.data)

    #     if serializer.is_valid():
    #         serializer.save()
    #         label = serializer.validated_data.get('label')
    #         message = f'Marker: {label} saved'
    #         return Response({'message': message})
    #     else:
    #         return Response(
    #             serializer.errors,
    #             status=status.HTTP_400_BAD_REQUEST
    #         )    

    # def update(self, request, pk=None):
    #     """Handle updating an object"""
    #     return Response({'http_method': 'PUT'})

    # def partial_update(self, request, pk=None):
    #     """Handle updating part of an object"""
    #     return Response({'http_method': 'PATCH'})

    # def destroy(self, request, pk=None):
    #     """Handle removing an object"""
    #     return Response({'http_method': 'DELETE'})
