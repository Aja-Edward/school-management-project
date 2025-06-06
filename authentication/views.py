# from django.contrib.auth import authenticate, login, logout, get_user_model
# from django.contrib.auth.tokens import default_token_generator
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.utils.encoding import force_bytes, force_str
# from django.core.mail import send_mail
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import AllowAny
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.authtoken.models import Token
# from django.conf import settings

# from rest_framework_simplejwt.views import TokenObtainPairView
# from .serializers import CustomTokenObtainPairSerializer

# User = get_user_model()


# # ------------------ LOGIN ------------------ #
# @api_view(["POST"])
# @permission_classes([AllowAny])
# def login_view(request):
#     email = request.data.get("email")
#     password = request.data.get("password")
#     user = authenticate(request, username=email, password=password)

#     if user is not None:
#         login(request, user)
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({"token": token.key}, status=status.HTTP_200_OK)
#     else:
#         return Response(
#             {"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED
#         )


# # ------------------ LOGOUT ------------------ #
# @api_view(["POST"])
# def logout_view(request):
#     request.user.auth_token.delete()
#     logout(request)
#     return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)


# # ------------------ PASSWORD RESET REQUEST ------------------ #
# @api_view(["POST"])
# @permission_classes([AllowAny])
# def password_reset_request(request):
#     email = request.data.get("email")
#     frontend_url = request.data.get("frontend_url")

#     if not email or not frontend_url:
#         return Response({"error": "Email and frontend_url are required."}, status=400)

#     user = User.objects.filter(email=email).first()
#     if user:
#         uid = urlsafe_base64_encode(force_bytes(user.pk))
#         token = default_token_generator.make_token(user)
#         reset_link = f"{frontend_url}/reset-password/{uid}/{token}/"

#         send_mail(
#             "Password Reset Request",
#             f"Click the link to reset your password:\n\n{reset_link}",
#             settings.DEFAULT_FROM_EMAIL,
#             [email],
#         )

#     return Response({"message": "If the email exists, a reset link has been sent."})


# # ------------------ PASSWORD RESET CONFIRM ------------------ #
# @api_view(["POST"])
# @permission_classes([AllowAny])
# def password_reset_confirm(request, uidb64, token):
#     password = request.data.get("password")
#     if not password:
#         return Response({"error": "Password is required."}, status=400)

#     try:
#         uid = force_str(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except Exception:
#         return Response({"error": "Invalid reset link."}, status=400)

#     if default_token_generator.check_token(user, token):
#         user.set_password(password)
#         user.save()
#         return Response({"message": "Password has been reset successfully."})
#     else:
#         return Response({"error": "Invalid or expired token."}, status=400)


# class CustomTokenObtainPairView(TokenObtainPairView):
#     serializer_class = CustomTokenObtainPairSerializer

# from django.contrib.auth.tokens import default_token_generator
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.utils.encoding import force_bytes, force_str
# from django.core.mail import send_mail
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import AllowAny, IsAuthenticated
# from rest_framework.response import Response
# from rest_framework import status

# from django.conf import settings
# from django.contrib.auth import get_user_model

# from .serializers import CustomTokenObtainPairSerializer

# User = get_user_model()


# # -------- JWT LOGIN VIEW -------- #
# @api_view(["POST"])
# @permission_classes([AllowAny])
# def jwt_login_view(request):
#     serializer = CustomTokenObtainPairSerializer(data=request.data)
#     if serializer.is_valid():
#         return Response(serializer.validated_data, status=status.HTTP_200_OK)
#     return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


# # -------- LOGOUT VIEW -------- #
# @api_view(["POST"])
# @permission_classes([IsAuthenticated])
# def logout_view(request):
#     # For JWT, logout is client-side token discard.
#     # Optionally implement refresh token blacklist if enabled.
#     return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)


# # -------- PASSWORD RESET REQUEST -------- #
# @api_view(["POST"])
# @permission_classes([AllowAny])
# def password_reset_request(request):
#     email = request.data.get("email")
#     frontend_url = request.data.get("frontend_url")

#     if not email or not frontend_url:
#         return Response({"error": "Email and frontend_url are required."}, status=400)

#     user = User.objects.filter(email=email).first()
#     if user:
#         uid = urlsafe_base64_encode(force_bytes(user.pk))
#         token = default_token_generator.make_token(user)
#         reset_link = f"{frontend_url}/reset-password/{uid}/{token}/"

#         send_mail(
#             "Password Reset Request",
#             f"Click the link to reset your password:\n\n{reset_link}",
#             settings.DEFAULT_FROM_EMAIL,
#             [email],
#         )

#     return Response({"message": "If the email exists, a reset link has been sent."})


# # -------- PASSWORD RESET CONFIRM -------- #
# @api_view(["POST"])
# @permission_classes([AllowAny])
# def password_reset_confirm(request, uidb64, token):
#     password = request.data.get("password")
#     if not password:
#         return Response({"error": "Password is required."}, status=400)

#     try:
#         uid = force_str(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except Exception:
#         return Response({"error": "Invalid reset link."}, status=400)

#     if default_token_generator.check_token(user, token):
#         user.set_password(password)
#         user.save()
#         return Response({"message": "Password has been reset successfully."})
#     else:
#         return Response({"error": "Invalid or expired token."}, status=400)

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.conf import settings
from django.contrib.auth import get_user_model

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken,
    OutstandingToken,
)

from .serializers import CustomTokenObtainPairSerializer

User = get_user_model()


# -------- JWT LOGIN VIEW -------- #
@api_view(["POST"])
@permission_classes([AllowAny])
def jwt_login_view(request):
    serializer = CustomTokenObtainPairSerializer(data=request.data)
    if serializer.is_valid():
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


# -------- LOGOUT VIEW -------- #
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    Logout by blacklisting the provided refresh token.
    Client must send refresh token in request data.
    """
    refresh_token = request.data.get("refresh")
    if not refresh_token:
        return Response(
            {"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        token = RefreshToken(refresh_token)
        # Blacklist the refresh token
        token.blacklist()
        return Response(
            {"message": "Successfully logged out."}, status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {"error": "Invalid or expired refresh token."},
            status=status.HTTP_400_BAD_REQUEST,
        )


# -------- PASSWORD RESET REQUEST -------- #
@api_view(["POST"])
@permission_classes([AllowAny])
def password_reset_request(request):
    email = request.data.get("email")
    frontend_url = request.data.get("frontend_url")

    if not email or not frontend_url:
        return Response({"error": "Email and frontend_url are required."}, status=400)

    user = User.objects.filter(email=email).first()
    if user:
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_link = f"{frontend_url}/reset-password/{uid}/{token}/"

        send_mail(
            "Password Reset Request",
            f"Click the link to reset your password:\n\n{reset_link}",
            settings.DEFAULT_FROM_EMAIL,
            [email],
        )

    return Response({"message": "If the email exists, a reset link has been sent."})


# -------- PASSWORD RESET CONFIRM -------- #
@api_view(["POST"])
@permission_classes([AllowAny])
def password_reset_confirm(request, uidb64, token):
    password = request.data.get("password")
    if not password:
        return Response({"error": "Password is required."}, status=400)

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception:
        return Response({"error": "Invalid reset link."}, status=400)

    if default_token_generator.check_token(user, token):
        user.set_password(password)
        user.save()
        return Response({"message": "Password has been reset successfully."})
    else:
        return Response({"error": "Invalid or expired token."}, status=400)
