from django.urls import path
from .views import LoginAPIView, MyTokenObtainPairView, BannerView, UserProfileView, ProfilePictureView, UserSignUp, CompanyView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from rest_framework_simplejwt.views import TokenVerifyView
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', LoginAPIView.as_view()),
    path('sign-up', UserSignUp.as_view(), name="sign-up"),
    path('banner', BannerView.as_view(), name="banner"),
    path('pfp', ProfilePictureView.as_view(), name="pfp"),

    path('company', CompanyView.as_view(), name="company"),
    path('user-profile', UserProfileView.as_view(), name='user-profile'),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
