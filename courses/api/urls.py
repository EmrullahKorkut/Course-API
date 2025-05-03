from django.urls import path, include

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from courses.api import views


#sadece list viewlarla komponentlerin testi-----------------------------------


urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'), #kayıt

    path('user-list/', views.UserListView.as_view(), name='user-list'),

    path('categories/', views.CategoryListView.as_view(), name='categories'),
    path('courses/', views.CourseListView.as_view(), name='courses'),
    path('lessons/', views.LessonListView.as_view(), name='course-lessons'),
    path('enrolls/', views.EnrollListView.as_view(), name='enrolls'),
    path('carts/', views.CartListView.as_view(), name='carts'),
    path('cart-contents/', views.CartContentListView.as_view(), name='cart-contents'),
    path('payment/', views.PaymentListView.as_view(), name='payment'),
    path('review/', views.ReviewListView.as_view(), name='review'),
    path('like/', views.LikeListView.as_view(), name='like'),
    path('favourite/', views.FavouriteListView.as_view(), name='favourite'),

    
    
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # giriş
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # yenileme
]
