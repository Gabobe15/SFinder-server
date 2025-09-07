from rest_framework import permissions, generics, status
from .permissions import IsAdmin
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _




from .serializers import *
from .models import *
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.response import Response
from knox.models import AuthToken
from knox.auth import TokenAuthentication
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
User = get_user_model()


class RegisterView(APIView):
    serializer_class = RegisterSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        
            
        token = AuthToken.objects.create(user)[1]
        fullname = getattr(user, 'fullname','No Name')
        role = getattr(user, 'role', 'No role')
        
        response = Response(
            {
                'user': {
                    'id': user.id,
                    'email':user.email,
                    'fullname': fullname,
                    'role':role
                },
                'token':token
            }
        )
        response.set_cookie(
            'auth_token',
            token,
            httponly = True,
            secure = not settings.DEBUG,
            
            samesite = "Lax",
            max_age = 48 * 60 * 60,
            path='/',
            domain=None if settings.DEBUG else '.yourdomain.com'
        )
        return response


class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    
    def post(self, request):
        if request.auth:
            AuthToken.objects.filter(token_key=request.auth.token_key).delete()
        response = Response({"message": "Logout successful"})
        response.delete_cookie('auth_token')
        return response


class ChangePasswordView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(
            data=request.data, 
            context={'request':request}
            )
        serializer.is_valid(raise_exception=True)
        

        user = request.user
        new_password = serializer.validated_data.get('new_password')
        
        user.set_password(new_password)
        user.save()
        
        
        return Response(
            {
                "message":  "Password changed successfully", 
                "icon":"success"
                }, 
            status=status.HTTP_200_OK)

token_generator = PasswordResetTokenGenerator()


from django.utils.translation import gettext_lazy as _

class PasswordResetRequestView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = User.objects.filter(email=email).first()
        
        if user:
            token = token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            base_url = settings.FRONTEND_PASSWORD_RESET_URL.rstrip('/')
            reset_url = f"{base_url}/{uid}/{token}"
            
            # Get the username part from email (before @)
            username = user.email.split('@')[0] if user.email else "User"
            
            # Create the email subject and message - CORRECTED VERSION
            subject = _('Password Reset Request')
            
            # Single translated string with placeholders
            message_template = _(
                "Hello {username},\n\n"
                "You requested a password reset for your {site_name} account.\n"
                "Please click the following link to reset your password:\n\n"
                "{reset_url}\n\n"
                "If you didn't request this, please ignore this email.\n\n"
                "Thank you.\n"
                "The {site_name} Team"
            )
            
            # Format the message with actual values
            message = message_template.format(
                username=username,
                site_name=settings.SITE_NAME,
                reset_url=reset_url
            )
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False
            )

        return Response(
            {"detail": _("If this email is registered, you will receive a password reset link shortly.")},
            status=status.HTTP_200_OK
        )

# class PasswordResetRequestView(APIView):
#     permission_classes = [permissions.AllowAny]
    
    
#     def post(self, request, *args, **kwargs):
#         serializer = PasswordResetRequestSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         email = serializer.validated_data['email']
#         user = User.objects.filter(email=email).first()
        
#         if user:
#             token = token_generator.make_token(user)
#             uid = urlsafe_base64_encode(force_bytes(user.pk))
            
#             base_url = settings.FRONTEND_PASSWORD_RESET_URL.rstrip('/')
#             reset_url = f"{base_url}/{uid}/{token}"
            
            
#             # send mail 
#             subject=_('Password Reset Request'),
#             message = _(
#                 "Hello {user.get_email_field_name()}, \n\n", 
#                 "You requested a password reset for your {settings.SITE_NAME} account, \n", 
#                 "Please click the following link to reset your password. \n\n", 
#                 "{reset_url}. \n", 
#                 "If you don't request this, please ignore this email. \n\n", 
#                 "Thank you. \n", 
#                 "The {settings.SITE_NAME} Team", 
#             ).format(
#                 email = user.get_email_field_name(),
#                 site_name = settings.SITE_NAME,
#                 reset_url = reset_url
#             )
            
#             send_mail(
#                 subject,
#                 message,
#                 settings.DEFAULT_FROM_EMAIL,
#                 [email],
#                 fail_silently=False
#             )

#         return Response(
#             {"detail": _("If this email is registered, you will receive a password reset link shortly.")},
#             status=status.HTTP_200_OK
#         )

class PasswordResetConfirmView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        uid = serializer.validated_data['uid']
        token = serializer.validated_data['token']
        new_password = serializer.validated_data['new_password']
        
        
        try:
             user_id = force_str(urlsafe_base64_decode(uid))
             user = User.objects.get(pk=user_id)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response(
                {"detail": _("Invalid reset link")},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not token_generator.check_token(user, token):
            return Response(
                {"detail":_("Invalid link or expired") },
                status=status.HTTP_400_BAD_REQUEST
            )
        user.set_password(new_password)
        user.save()
        
        return Response(
            {
                "detail": _("Password has been reset successfully")
            },
            status=status.HTTP_200_OK
        )
        
        
class UsersList(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    queryset = User.objects.all()
    serializer_class = ListUsersSerializer
    permission_classes = [IsAdmin]

class UpdateUser(generics.RetrieveUpdateDestroyAPIView):
    pass 




class UserView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    
    
    def get(self, request):
        user = request.user
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)



