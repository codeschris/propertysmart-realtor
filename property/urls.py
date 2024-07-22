from django.urls import path
from .views import register, login_view, VerifyTokenView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('verify-token/', VerifyTokenView.as_view(), name='verify-token'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
