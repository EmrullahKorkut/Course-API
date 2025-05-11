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


    path('courses/<int:pk>/lessons/', views.LessonListCreateView.as_view(), name='course-lessons'),
    path('courses/<int:pk>/lessons/<int:lesson_id>/', views.LessonDetailView.as_view(), name='lesson-detail'),


    path('courses/<int:pk>/card/', views.CartAddDeleteView.as_view(), name='add-card'),
    path('my-card/', views.CartDetailView.as_view(), name='user-card-detail'),


    path('my-card/pay', views.PaymentView.as_view(), name='payment'),
    
    
    # path('cart-contents/', views..as_view(), name='cart-contents'),


    path('my-courses/', views.EnrollListView.as_view(), name='enroll'),
    
    
    path('courses/<int:pk>/review/', views.ReviewListCreateView.as_view(), name='review'),
    path('courses/<int:pk>/review/<int:review_id>/', views.ReviewGetDeleteView.as_view(), name='review-detail'),

    
    path('review/<int:pk>/like/', views.LikeListCreateView.as_view(), name='like'),
    path('review/<int:pk>/unlike/', views.LikeGetDeleteView.as_view(), name='unlike'),
    
    
    path('courses/<int:pk>/fav/', views.FavouriteCreateView.as_view(), name='favourite'),
    path('courses/<int:pk>/unfav/', views.FavouriteGetDeleteView.as_view(), name='unfavourite'),
    path('fav-courses/', views.FavouriteListView.as_view(), name='favourite'),


    
    
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # giriş
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # yenileme
]
