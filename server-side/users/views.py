# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
import random
import logging

from .models import CustomUser
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    ForgotPasswordSerializer,
    VerifyCodeSerializer,
    ResetPasswordSerializer,
    UserSerializer,
    UserUpdateSerializer
)

logger = logging.getLogger(__name__)


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                refresh = RefreshToken.for_user(user)
                
                return Response({
                    "message": "User registered successfully.",
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "user": {
                        "id": user.id,
                        "email": user.email,
                        "username": user.username,
                        "user_type": user.user_type,
                        "restaurant_name": user.restaurant_name if user.is_restaurant_owner() else None
                    }
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                logger.error(f"Registration error: {str(e)}")
                return Response({
                    "error": "Registration failed. Please try again."
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            username = serializer.validated_data.get('username')
            password = serializer.validated_data['password']

            try:
                # Find user by email or username
                if email:
                    user = CustomUser.objects.get(email=email)
                else:
                    user = CustomUser.objects.get(username=username)
                
                # Check password
                if not user.check_password(password):
                    return Response({
                        "error": "Invalid credentials."
                    }, status=status.HTTP_401_UNAUTHORIZED)
                
                # Check if user is active
                if not user.is_active:
                    return Response({
                        "error": "Account is deactivated."
                    }, status=status.HTTP_401_UNAUTHORIZED)

                # Generate tokens
                refresh = RefreshToken.for_user(user)
                
                return Response({
                    "message": "Login successful.",
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "user": {
                        "id": user.id,
                        "email": user.email,
                        "username": user.username,
                        "user_type": user.user_type,
                        "restaurant_name": user.restaurant_name if user.is_restaurant_owner() else None
                    }
                }, status=status.HTTP_200_OK)
                
            except CustomUser.DoesNotExist:
                return Response({
                    "error": "Invalid credentials."
                }, status=status.HTTP_401_UNAUTHORIZED)
            except Exception as e:
                logger.error(f"Login error: {str(e)}")
                return Response({
                    "error": "Login failed. Please try again."
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            
            try:
                user = CustomUser.objects.get(email=email)
                
                # Generate 6-digit verification code
                code = f"{random.randint(100000, 999999)}"
                user.verification_code = code
                user.save()
                
                # Send email
                try:
                    send_mail(
                        subject='Password Reset Code - Food Delivery App',
                        message=f'Your password reset code is: {code}\n\nThis code will expire in 15 minutes.',
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[email],
                        fail_silently=False,
                    )
                    
                    return Response({
                        "message": "Reset code sent to your email address."
                    }, status=status.HTTP_200_OK)
                    
                except Exception as e:
                    logger.error(f"Email sending error: {str(e)}")
                    return Response({
                        "error": "Failed to send email. Please try again."
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    
            except CustomUser.DoesNotExist:
                # Don't reveal if email exists for security
                return Response({
                    "message": "If an account with this email exists, a reset code has been sent."
                }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyResetCodeView(APIView):
    def post(self, request):
        serializer = VerifyCodeSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            code = serializer.validated_data['code']
            
            try:
                user = CustomUser.objects.get(email=email)
                
                if user.verification_code == code:
                    return Response({
                        "message": "Verification successful. You may now reset your password."
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        "error": "Invalid verification code."
                    }, status=status.HTTP_400_BAD_REQUEST)
                    
            except CustomUser.DoesNotExist:
                return Response({
                    "error": "User not found."
                }, status=status.HTTP_404_NOT_FOUND)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            code = serializer.validated_data['code']
            new_password = serializer.validated_data['new_password']
            
            try:
                user = CustomUser.objects.get(email=email)
                
                if user.verification_code == code:
                    user.set_password(new_password)
                    user.verification_code = None  # Clear the code
                    user.save()
                    
                    return Response({
                        "message": "Password reset successfully."
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        "error": "Invalid verification code."
                    }, status=status.HTTP_400_BAD_REQUEST)
                    
            except CustomUser.DoesNotExist:
                return Response({
                    "error": "User not found."
                }, status=status.HTTP_404_NOT_FOUND)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request):
        serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Profile updated successfully.",
                "user": UserSerializer(request.user).data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            
            return Response({
                "message": "Logged out successfully."
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "error": "Logout failed."
            }, status=status.HTTP_400_BAD_REQUEST)
