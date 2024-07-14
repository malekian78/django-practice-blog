from rest_framework.viewsets import ModelViewSet
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.throttling import ScopedRateThrottle
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
import jwt


from .serializers import (
    ProfileSerializer,
    CustomTokenObtainPairSerializer,
    ChangePasswordSerializer,
)
from accounts.models.profile import Profile
from accounts.models.user import MyUser
from .permissions import IsOwnerOrReadOnly


User = get_user_model()

# قابلیت تغییر و اضافه کردن و مشاهده کردن پروفایل کاربر
class ProfileViewSet(ModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [
        IsOwnerOrReadOnly,
    ]
    queryset = Profile.objects.all()
    http_method_names = ("get", "post", "put", "patch", "head")


# خروجی شخصی سازی شده بدون اینکه صرفا توکن به کاربر برگرده
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# حذف توکن کاربر
class CustomDiscardAuthToken(APIView):
    permission_classes = [IsAuthenticated,]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# تغییر پسورد کاربر
class ChangePasswordAPIView(generics.UpdateAPIView):
    model = User
    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = ChangePasswordSerializer

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        # دو کد زیر مشابه همدیگه هستند
        # serializer = self.get_serializer(data=request.data)
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            # بررسی پسورد وارد شده
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": "wrong password!"}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response({"detail": "password changed"},status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# فعال کردن حساب کاربری با ایمیل 😎✌
class VerificationEmail(generics.GenericAPIView):
    throttle_scope = "email"
    permission_classes = [IsAuthenticated,]

    def get(self, request, *args, **kwargs):
        # اول بررسی کنیم کاربر از قبل احراز هویت نشده باشد
        if request.user.is_verified:
            return Response(
                {"detail": "your account is already verified"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        self.user_obj = self.request.user
        tokens = self.get_tokens_for_user(self.user_obj)
        # ! ست کردیم مطابقت داشته باشد urls.py با اونی که داخل url  دقت کنید که باید 
        # ! درخواست ارسال کند UserVerificationViewSet زیر قراره به کلاس url در حقیقت
        mail_txt = f"verify your account:\n\n \
            http://localhost:8000/accounts/api/v1/verify/confirm/{tokens['access']}/"

        send_mail(
            "ایمیل احراز هویت",
            mail_txt,
            "from@example.com",
            [self.user_obj.email],
            fail_silently=False,
        )
        return Response(f"email sent {request.method}")

    # ساخت توکن جدید در صورت نیاز
    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)

        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }

# کنیم verified کلیک کرد با کمک کلاس زیر سعی می کنیم کاربر را url بعد که کاربر روی اون
class UserVerificationViewSet(APIView):

    def get(self, request, token, *args, **kwargs):
        try:
            token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.exceptions.ExpiredSignatureError:
            return Response(
                {"detail": "token expired!"}, status=status.HTTP_400_BAD_REQUEST
            )
        except jwt.exceptions.InvalidSignatureError:
            return Response(
                {"detail": "signature is invalid"}, status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.get(id=token["user_id"])
        if user.is_verified:
            return Response({"detail": "user is already verified."})
        user.is_verified = True
        user.save()
        return Response(
            {"detail": "user account verification completed"},
            status=status.HTTP_202_ACCEPTED,
        )

