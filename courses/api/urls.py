from django.urls import path, include

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from courses.api import views


from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'categories', views.CategoryViewset)
router.register(r'courses', views.CourseViewset)


#sadece list viewlarla komponentlerin testi-----------------------------------


urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'), #kayıt


    path('user-list/', views.UserListView.as_view(), name='user-list'),
    path('user-list/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),


    path('', include(router.urls)), #kategiriler, kurslar için
    #path('courses/', views.CourseListView.as_view(), name='courses'),


    path('courses/<int:pk>/lessons/', views.LessonListView.as_view(), name='course-lessons'),
    path('courses/<int:pk>/lessons/<int:lesson_id>', views.LessonDetailView.as_view(), name='lesson-detail'),


    # path('courses/<int:pk>/add-course/', views.CartAddView.as_view(), name='add-card'),
    # path('my-card/', views.CartListView.as_view(), name='user-card-detail'),
    # path('my-card/<int:course>/', views.CartListView.as_view(), name='user-card-detail'),

    
    
    # path('cart-contents/', views..as_view(), name='cart-contents'),
    
    
    path('payment/', views.PaymentListView.as_view(), name='payment'),


    path('course/<int:pk>/enroll', views.EnrollListView.as_view(), name='enroll'),
    
    
    path('review/', views.ReviewListView.as_view(), name='review'),
    
    
    path('like/', views.LikeListView.as_view(), name='like'),
    
    
    path('favourite/', views.FavouriteListView.as_view(), name='favourite'),

    
    
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # giriş
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # yenileme
]
