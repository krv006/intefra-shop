from django.urls import path

from users.views import SendEmailAPIView, VerifyEmailAPIView

urlpatterns = [
    path('auth/send-email/', SendEmailAPIView.as_view(), name='send-email'),
    path('auth/verify-code/', VerifyEmailAPIView.as_view(), name='verify-email'),

]
