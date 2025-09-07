from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _


from .models import *
from django.contrib.auth import get_user_model
User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'fullname', 'role', 'email', 'password', 'sex', 'tel_no')
        
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),email=email, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials.')
        else:
            raise serializers.ValidationError('Both email and password are required.')

        return user

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_new_password = serializers.CharField(required=True, write_only=True)
    
    def validate(self, data):
        user = self.context.get('request').user
        
        old_password = data.get('old_password')
        if not user.check_password(old_password):
            raise serializers.ValidationError({'old_password': 'old password is incorrect'})
        
        new_password = data.get('new_password')
        confirm_new_password = data.get('confirm_new_password')
        
        if new_password != confirm_new_password:
            raise serializers.ValidationError({'confirm_new_password':"Password do not match"})
        
        try:
            validate_password(new_password, user=user)
        except DjangoValidationError as e:
            raise serializers.ValidationError({'new_password': list(e.messages)})
        
        return data

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    
    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("We could not find an account with that email address")
        return value 
    
    
class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)
    

    
    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError(_, ("Passwords do not match"))
        return data

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    
    class Meta:
        model = User 
        fields = ['id', 'fullname', 'role', 'email']
    
class ListUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'fullname', 'email', 'role', 'sex', 'tel_no']
        