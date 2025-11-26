from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _
from core.models import Category

from .models import *
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import CustomUser

from core.serializers import CategorySerializer

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True,
        required=False,
        allow_null=True
    )


    field_study = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'fullname', 'role', 'email', 'password', 'sex', 'mobile','address', 'category_id', 'field_study')
        
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if not email and password:
            raise serializers.ValidationError("Both email and password are required")
        user = authenticate(
            request=self.context.get('request'),
            email=email,
            password=password
        )
        
        if not user:
            raise serializers.ValidationError('Invalid credentials')
         
        if not user.is_active:
             raise serializers.ValidationError('This account is inactive')

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
    field_study = serializers.CharField(source="category.name", read_only=True)
    email = serializers.EmailField()

    class Meta:
        model = User 
        fields = ['id', 'fullname', 'role', 'email', "field_study",'mobile','sex','address']
        read_only_fields = ['id', 'role']
    # 'created_at'

class ListUsersSerializer(serializers.ModelSerializer):
    field_study = serializers.CharField(source="category.name", read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'fullname', 'email', 'role', 'field_study','sex', 'mobile', 'is_active']
        # fields = '__all__'

class ListUniversitiesSerializer(serializers.ModelSerializer):
    field_study = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = User
        fields = [
            'id','fullname', 'email', 'role',
            'sex', 'mobile', 'is_active', 'field_study'
        ]


