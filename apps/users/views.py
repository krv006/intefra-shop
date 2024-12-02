from random import randint

from django.core.cache import cache
from drf_spectacular.utils import extend_schema
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from users.models import User
from users.serializers import RegisterModelSerializer, VerifyModelSerializer
from users.task import send_verification_email_task


@extend_schema(tags=['send-email'])
class SendEmailAPIView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterModelSerializer
    permission_classes = AllowAny,

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        code = randint(100000, 1000000)
        cache.set(email, code, timeout=120)
        send_verification_email_task.delay(email, code)
        return Response({"message": "Successfully sent code"})

    def get_queryset(self):
        return self.request.user


@extend_schema(tags=['send-email'])
class VerifyEmailAPIView(GenericAPIView):
    serializer_class = VerifyModelSerializer
    permission_classes = AllowAny,

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"message": "OK"})
