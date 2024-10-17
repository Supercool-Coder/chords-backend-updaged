from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage
from user_auth.models import Token, User 
from django.contrib.auth.hashers import check_password, is_password_usable, make_password
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
import uuid
from pyfcm import FCMNotification
import traceback
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from user_auth.serializers import PasswordResetSerializer, TokensSerializer, UserLoginSerializers, UserRegistrationSerializer , UserInformationSerializer , UpdateProfileSerializer ,  UserRoleCountingSerializer, TotalUserCountSerializer
from user_auth.models import Songs , Artist , Collections ,User
# Create your views here.
from rest_framework import generics
from rest_framework.response import Response
from django.db import models  # Import models here

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        # 'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
# class UserRegistrationView(APIView):
#     def post(self, request, format=None):
#         serializer = UserRegistrationSerializer(data=request.data)
        
#         # Validate the registration data
#         if serializer.is_valid():
#             # Save the user data from the serializer
#             user = serializer.save()

#             # Generate a unique 12-character uppercase string for some additional process
#             uuidTemp = uuid.uuid4().hex[:12].upper()  # If needed elsewhere

#             # Generate tokens for the registered user
#             key = get_tokens_for_user(user)

#             # Prepare data for the token serializer
#             token_data = {
#                 "key": key["access"],
#                 "user": user.id
#             }

#             # Serialize the token data
#             token_serializer = TokensSerializer(data=token_data)

#             # Validate and save the token data
#             if token_serializer.is_valid():
#                 token_serializer.save()

#             # Return a success response with user details
#             return Response({
#                 'status': True, 
#                 'status_code': '200', 
#                 'message': 'Registration Successful', 
#                 'data': {
#                     'user': serializer.data,  # Serialized user data from registration
#                     'token': token_data["key"]  # Return the access token as well
#                 }
#             }, status=status.HTTP_200_OK)

#         # If serializer validation fails, return an error response
#         return Response({
#             'status': False, 
#             'status_code': '400', 
#             'message': 'Email already exists or validation error occurred',
#             'errors': serializer.errors,  # Return validation errors for better debugging
#             'data': None
#         }, status=status.HTTP_400_BAD_REQUEST)

class UserRegistrationView(APIView):
    def post(self, request, format=None):
        # Get data from the request and pass it to the serializer
        serializer = UserRegistrationSerializer(data=request.data)

        # Validate the registration data
        if serializer.is_valid():
            # Save the user data from the serializer
            user = serializer.save()

            # Generate a unique code (12 characters)
            uuidTemp = uuid.uuid4().hex[:12].upper()

            # Get the role if provided, otherwise default to "user"
            user_role = serializer.validated_data.get("role", "user").lower()  # Default to "user"

            # Create a profile based on the role
            if user_role == "songs":
                songs_profile = Songs(
                    code=uuidTemp,
                    user=user,
                    bio="NA",
                )
                songs_profile.save()

            elif user_role == "artist":
                artist_profile = Artist(
                    code=uuidTemp,
                    user=user,
                    bio="NA",
                )
                artist_profile.save()

            elif user_role == "collections":
                collections_profile = Collections(
                    code=uuidTemp,
                    user=user,
                    bio="NA",
                )
                collections_profile.save()

            else:
                # If the role is invalid or not recognized, register as a default "user"
                # You can choose to do nothing or create a default profile for a "user"
                pass  # Or create a default UserProfile if necessary

            # Generate tokens for the registered user
            key = get_tokens_for_user(user)

            # Prepare data for the token serializer
            token_data = {
                "key": key["access"],
                "user": user.id
            }

            # Serialize the token data
            user_serializers = TokensSerializer(data=token_data)

            # Validate and save the token data
            if user_serializers.is_valid():
                user_serializers.save()

            # Return a success response with user details
            return Response({
                'status': 'SUCCESS',
                'status_code': '200',
                'message': 'Registration Successful',
                'data': {
                    'user': serializer.data,  # Serialized user data from registration
                    'token': token_data["key"]  # Return the access token as well
                }
            }, status=status.HTTP_201_CREATED)

        # If serializer validation fails, return an error response
        return Response({
            'status': 'Error',
            'status_code': '400',
            'message': 'Email already exists or validation error occurred',
            'errors': serializer.errors,  # Return validation errors for better debugging
            'data': None
        }, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    def post(self, request, format=None):
        
        serializer = UserLoginSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            
            if user is not None:
                key = get_tokens_for_user(user)

                token_data = {
                    "key": key["access"],
                    "user": user.id
                }

                token_serializer = TokensSerializer(data=token_data)
                if token_serializer.is_valid():
                    token_serializer.save()

                profile_serializer = UserRegistrationSerializer(user)

                return Response({
                    'status': True,
                    'status_code': '200',
                    'message': 'SignIn Success',
                    'data': {
                        'user': {
                            'name': user.name,
                            'email': user.email,
                            'phone': user.phone,
                            'role':user.role
                        },
                        
                        'profile': profile_serializer.data,
                        'token': key
                    }
                }, status=status.HTTP_202_ACCEPTED)
            else:
                return Response({
                    'status': False,
                    'status_code': '400',
                    'message': 'Invalid Credentials, Please try again',
                    'data': None
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                'status': False,
                'status_code': '400',
                'message': 'Invalid data',
                'data': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = PasswordResetSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'status': True, 'message': 'Password has been reset successfully.'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserListView(APIView):
    # Remove permission_classes to allow unauthenticated access
    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserInformationSerializer(users, many=True)
        return Response({
            'status': True,
            'status_code': '200',
            'message': 'User list retrieved successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
    

# user_auth/views.py
# user_auth/views.py

class UserUpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can update profiles

    def patch(self, request, user_id, format=None):
        try:
            user = User.objects.get(id=user_id)  # Fetch user by ID
        except User.DoesNotExist:
            return Response({
                'status': False,
                'status_code': '404',
                'message': 'User not found',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UpdateProfileSerializer(user, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': True,
                'status_code': '200',
                'message': 'Profile updated successfully',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        
        return Response({
            'status': False,
            'status_code': '400',
            'message': 'Invalid data provided',
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class UserRoleCountView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        # Get user counts grouped by role
        role_counts = User.objects.values('role').annotate(count=models.Count('id')).order_by('role')

        # Prepare data for serialization
        role_data = []
        for item in role_counts:
            role_data.append({'role': item['role'], 'count': item['count']})

        # Calculate total user count
        total_users_count = User.objects.count()

        # Create the response data
        response_data = {
            'user_counts': role_data,
            'total_users': total_users_count,
        }

        return Response(response_data)