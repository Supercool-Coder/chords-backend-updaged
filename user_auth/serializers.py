from datetime import date
from email.policy import default
# from importlib.metadata import requires
from rest_framework import serializers
from user_auth.models import  Token, User 
import logging
import uuid
import random
from django.contrib.auth.hashers import check_password, is_password_usable, make_password
from django.contrib.auth.password_validation import validate_password
from user_auth.models import Artist , Songs , Collections , User
logger = logging.getLogger(__name__)
from collections import defaultdict
from rest_framework import serializers
from user_auth.models import User


class UserSerializer(serializers.ModelSerializer):
  id=serializers.IntegerField()
  code=serializers.CharField(max_length=200,default="")  
  name=serializers.CharField(max_length=200,default="")  
  role = serializers.CharField(max_length=20, default="",required=False)
  email=serializers.CharField(max_length=200,default="")  
  password=serializers.CharField(max_length=200, default="")
  phone = serializers.IntegerField() 
  profile=serializers.ImageField()
  remember_token=serializers.CharField(max_length=200, default="")  
  login_mode = serializers.CharField(max_length=200, default='Email')  
  status = serializers.CharField(max_length=200, default='Active')  
  is_active = serializers.BooleanField(default=True)      
  auth_provider = serializers.CharField(max_length=255,default="Email")  
  auth_token =  serializers.CharField(max_length=255,default="Email") 
  # created_at = serializers.DateTimeField(default=date.today)
  # updated_at = serializers.DateTimeField(default=date.today) 

  class Meta:
    model = User
    # fields= ('__all__')
    fields=['id','code','email', 'name','role', 'password','phone','profile','remember_token','login_mode','status','is_active' , 'user_type', 'auth_provider' ,'auth_token']
    extra_kwargs={
      'password':{'write_only':True},
      'id':{'read_only':True}
    }

  def validate(self, attrs):
    name = attrs.get('name')
    password = attrs.get('password')
    # password2 = attrs.get('password2')
    logger.info(attrs)
    # if name != '':
    #   raise serializers.ValidationError("Invalid Username")
    
    # if password != '':
    #   raise serializers.ValidationError("Invalid Password")
    return attrs
  


class UserRegistrationSerializer(serializers.ModelSerializer):

    profile = serializers.ImageField(required=False)
    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'role','profile', 'phone', 'auth_provider', 'auth_token']
        extra_kwargs = {
            'password': {'write_only': True},
            'role': {'required': False},  # Make role optional
            'profile': {'required': False},
        }

    def create(self, validated_data):
        # Extract role and remove from validated data
        role = validated_data.pop('role', None)  # Default to None if not provided
        profile = validated_data.pop('profile', None)
        # Hash the password before saving
        password = validated_data.pop('password')
        user_instance = User(**validated_data)
        user_instance.set_password(password)  # Hash the password

        if profile:
          user_instance.profile = profile

        user_instance.save()

        # Create a profile based on the role if specified
        if role:
            if role.lower() == 'songs':
                Songs.objects.create(
                    user=user_instance,
                    name=user_instance.name,
                    bio='',
                    profile='',
                )
            elif role.lower() == 'artist':
                Artist.objects.create(
                    user=user_instance,
                    name=user_instance.name,
                    bio='',
                    profile='',
                )
            elif role.lower() == 'collections':
                Collections.objects.create(
                    user=user_instance,
                    name=user_instance.name,
                    bio='',
                    profile='',
                )

        return user_instance
    
    def validate(self, attrs):
      password = attrs.get('password')
      return attrs
      
    def validate(self, attrs):
      auth_token = attrs.get('auth_token')
      return attrs

    def validate(self, attrs):
      auth_provider = attrs.get('auth_provider')
      return attrs

    def create(self, validate_data):    
      user_instance= User.objects.create_user(**validate_data) 
      uuidTemp=uuid.uuid4().hex[:12].upper()
      return user_instance

class ArtistSerializers(serializers.ModelSerializer):
  uuidTemp=uuid.uuid4().hex[:12].upper()
  code=serializers.CharField(default=uuidTemp )
  bio=serializers.CharField(default="My Bio")
  interests=serializers.CharField(default="NA")

  class Meta:
    model = Collections
    fields= '__all__'

    def create(self, validated_data):  
        validated_data['code']=uuid.uuid4().hex[:12].upper()
        artist_id=validated_data["songs"]
        user_instance = User.objects.get(id=artist_id)
        return Artist.objects.create(**validated_data)
    
class SongsSerializers(serializers.ModelSerializer):
  uuidTemp=uuid.uuid4().hex[:12].upper()
  code=serializers.CharField(default=uuidTemp )
  bio=serializers.CharField(default="My Bio")
  interests=serializers.CharField(default="NA")

  class Meta:
    model = Songs
    fields= '__all__'

    def create(self, validated_data):  
        validated_data['code']=uuid.uuid4().hex[:12].upper()
        songs_id=validated_data["songs"]
        user_instance = User.objects.get(id=songs_id)
        return Songs.objects.create(**validated_data)
    
class CollectionsSerializers(serializers.ModelSerializer):
  uuidTemp=uuid.uuid4().hex[:12].upper()
  code=serializers.CharField(default=uuidTemp )
  bio=serializers.CharField(default="My Bio")
  interests=serializers.CharField(default="NA")

  class Meta:
    model = Collections
    fields= '__all__'

    def create(self, validated_data):  
        validated_data['code']=uuid.uuid4().hex[:12].upper()
        collections_id=validated_data["songs"]
        user_instance = User.objects.get(id=collections_id)
        return Collections.objects.create(**validated_data)

class UserLoginSerializers(serializers.ModelSerializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    model = User
    fields = ['email', 'password' , 'role']
    


# User serializer to get Users details in any Serializer
class UserInformationSerializer(serializers.ModelSerializer):
  id= serializers.IntegerField(default=0)
  email=serializers.CharField(default="")
  name=serializers.CharField(default="")
  class Meta:
    model = User
    fields = ['id', 'email', 'name']  
    
    

class PasswordResetSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        # Validate that the new passwords match
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("New passwords do not match.")
        return data

    def validate_old_password(self, value):
        # Ensure old_password is correct
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is not correct.")
        return value

    def save(self):
        user = self.context['request'].user
        password = self.validated_data['new_password']
        user.set_password(password)
        user.save()
        return user


class SocialLoginSerializers(serializers.ModelSerializer):
  auth_token =  serializers.CharField(max_length=255 )
  auth_provider = serializers.CharField(max_length=255)
  class Meta:
    model = User
    fields = ['auth_token','auth_provider']
    
class TokensSerializer(serializers.ModelSerializer):
  key = serializers.CharField(max_length=4048)
  user = serializers.IntegerField(default=0)
  class Meta:
    model = Token
    fields = '__all__'

class UserInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'last_login', 'code', 'email', 'name', 'role', 'username', 'phone', 'profile',  'login_mode', ]



class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'username', 'phone', 'role']  # Add other fields that you want to allow for updating

    def update(self, instance, validated_data):
        # Updating user fields except for email and password
        instance.name = validated_data.get('name', instance.name)
        instance.username = validated_data.get('username', instance.username)
        # instance.bio = validated_data.get('bio', instance.bio)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.role = validated_data.get('role', instance.role)
        
        instance.save()
        return instance
    



class UserRoleCountingSerializer(serializers.Serializer):
    role = serializers.CharField()
    count = serializers.IntegerField()

class TotalUserCountSerializer(serializers.Serializer):
    total_users = serializers.IntegerField()