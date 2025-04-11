from django.db import transaction
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User, UserNextOfKin
from .serializers import (NextOfKinSerializer, UserLoginSerializer,
                          UserSerializer, UserSignUpSerializer)


class UserSignUpViewSet(GenericViewSet):
    permission_classes = []
    serializer_class = UserSignUpSerializer

    @action(detail=False, methods=['post'])
    def signup(self, request):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {
                    'success': True,
                    'message': 'User created successfully',
                }, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'success': False, 'error': str(e.args[0])}, status=status.HTTP_400_BAD_REQUEST)
        


class UserLoginViewSet(TokenObtainPairView, GenericViewSet):
    permission_classes = []
    serializer_class = UserLoginSerializer

    @action(detail=False, methods=['post'])
    def login(self, request):
        # try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data

            print(user)

            _res = super().post(request=request)
            print(_res)
            print(type(_res))
            access_token = _res.data.get('access')
            refresh_token = _res.data.get('refresh')

            user_serializer = UserSerializer(user)
            # print(user_serializer)


            return Response(
                data={
                    'success': True,
                    'message': 'User logged in successfully',
                    'data': {
                        'user': user_serializer.data,
                        'access_token': str(access_token),
                        'refresh_token': str(refresh_token)
                    }
                }, status=status.HTTP_200_OK)
        # except Exception as e:
        #     return Response({'success': False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        # except ValidationError as e:
        #     return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def me(self, request):
        user = request.user
        serializer = self.get_serializer(user)

        return Response(
            data={
                'success': True,
                'data': serializer.data
            }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def logout(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            assert refresh_token, "Refresh token is required"

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                data={
                    'success': True,
                    'message': 'User logged out successfully'
                }, status=status.HTTP_200_OK)
        except TokenError as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    
    @action(detail=False, methods=['get'])
    def all(self, request):
        """Get all users"""
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(
            data={
                'success': True,
                'data': serializer.data,
                "extra": {
                    "total": users.count()
                }
            }, status=status.HTTP_200_OK)
    

class UserProfileViewSet(GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_user_detail(self, request, *args, **kwargs):
        try:
            pass
        except Exception as e:
            return Response(data={'success': True, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# class UserViewSet(GenericViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

#     @action(detail=True, methods=['get'])
#     def next_of_kin(self, request, pk=None):
#         user = self.get_object()
#         next_of_kin = UserNextOfKin.objects.filter(user=user)
#         serializer = NextOfKinSerializer(next_of_kin, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)