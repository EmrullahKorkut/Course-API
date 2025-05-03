from django.urls import path, include

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from courses.api import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'), #kayıt
    path('user-list/', views.UserListView.as_view(), name='user-list'),
    
    
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # giriş
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # yenileme
]
