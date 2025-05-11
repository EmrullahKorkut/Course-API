from urllib import response
from django.forms import ValidationError
from rest_framework import generics, viewsets, mixins, permissions, status
from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from rest_framework.decorators import action

from django.shortcuts import get_object_or_404


from courses.api.permissions import IsAdminOrReadOnly, IsAdminOrTeacherOrReadOnly, IsStudentOrReadOnly


from courses.api.serializers import (
    RegisterSerializer, 
    CategorySerializer, 
    CourseSerializer, 
    LessonSerializer, 
    EnrollSerializer, 
    CartSerializer, 
    PaymentSerializer, 
    ReviewSerializer, 
    LikeSerializer, 
    FavouriteSerializer,
    UserSerializer
    )
from courses.models import User, Category, Course, Lesson, Enroll, Cart, Payment, Review, ReviewLike, Favourite



# from rest_framework.viewsets import GenericViewSet
# from rest_framework import mixins


class RegisterView(generics.CreateAPIView):  #yazdığımız user modeline kayıt işlemi
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]  

#---------------------------------------------------deneme için listeleme views, crud işlemlerine geçilecek routerlar, urller ayarlanacak---------------------------
#--------------------------------------------------------------------------------------------
class UserListView(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):                                #USER LİSTELEMESİ VE DETAYLARI
        return self.list(request, *args, **kwargs)                                          
    
class UserDetailView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
#-----------------------------------------------------------------------------------------------

class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()                                   #CATEGORY VİEW. NOT SAFE METODLAR SADECE ADMİN İÇİNDİR. LİST RETRİEVE AUTH USERS İÇİN
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


#------------------------------------------------------------------------------------------------

class CourseViewset(viewsets.ModelViewSet):
    queryset = Course.objects.all()                                     #ADMİN TEACHER EDİTLER KALANLAR SADECE LİST EDER
    serializer_class = CourseSerializer
    permission_classes = [IsAdminOrTeacherOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)

#------------------------------------------------------------------------------------------------


class LessonListCreateView(generics.ListCreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = []

    def get_queryset(self):
        course_id = self.kwargs['pk']
        course = get_object_or_404(Course, pk=course_id)
        return Lesson.objects.filter(course=course)
    

class LessonDetailView(generics.RetrieveAPIView):                           #
    serializer_class = LessonSerializer

    def get_object(self):   
        course_id = self.kwargs['pk']
        lesson_id = self.kwargs['lesson_id']
        course = get_object_or_404(Course, pk=course_id)
        lesson = get_object_or_404(Lesson, pk=lesson_id, course=course)
        return lesson


#-----------------------------------------------------------------------------------------------

class CartAddDeleteView(APIView):
    permission_classes = [IsStudentOrReadOnly]

    def post(self, request, pk):
        user = request.user
        cart = Cart.objects.get(student=user)
        course = get_object_or_404(Course, pk=pk)

        if course in cart.courses.all():
            return Response({"message": "You cant add the same course!!.."}, status=status.HTTP_200_OK)
        
        cart.courses.add(course)

        return Response({
            "message": f"The course '{course.title}' added to cart!! Pay the money and use the courses"
        }, 
        status=status.HTTP_200_OK)
    
    def delete(self, request, pk):
        user = request.user
        cart = get_object_or_404(Cart, student=user)
        course = get_object_or_404(Course, pk=pk)

        if course not in cart.courses.all():
            return Response({"message": "Course not in your cart you can add the course"}, status=status.HTTP_404_NOT_FOUND)

        cart.courses.remove(course)
        return Response({"message": f"'{course.title} removed from cart!!"}, status=status.HTTP_200_OK)


class CartDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsStudentOrReadOnly]

    def get_object(self):
        username = self.request.user
        try:
            cart = Cart.objects.get(student=username)
        except Cart.DoesNotExist:
            raise NotFound('There is no a cart for you.please add a course to the card')

        return cart
    

#-----------------------------------------------------------------------------------------------

# class CartContentListView(generics.ListAPIView):
#     queryset = CartContent.objects.all()
#     serializer_class = CartContentSerializer
#     permission_classes = []

#-----------------------------------------------------------------------------------------------

class PaymentView(APIView):
    permission_classes = []

    def get(self, request):
        cart = get_object_or_404(Cart, student=request.user)
        if not cart.courses.exists():
            return Response({"error":"Please add course to your card!!!"}, status=status.HTTP_400_BAD_REQUEST)

        course_list = cart.courses.all()
        courses = CourseSerializer(course_list, many=True)

        return Response({"message": "Courses ready for payment", "courses": courses.data})


    def post(self, request):
        cart = get_object_or_404(Cart, student=request.user)

        if not cart.courses.exists():
            return Response({"error":"Please add course to your card!!!"}, status=status.HTTP_400_BAD_REQUEST)
        
        payment_fee = 0
        for courses in cart.courses.all():
            payment_fee += courses.price
        
        Payment.amount = payment_fee
       
        enrolls = []

        for course in cart.courses.all():
            enroll_course = Enroll.objects.create(student=request.user, courses=course)
            enrolls.append(enroll_course)
                                  
        return Response({"message":f"Payment is successful..!{Payment.amount}TL"}, status=status.HTTP_200_OK)
    

#-----------------------------------------------------------------------------------------------

class EnrollListView(generics.ListAPIView):
    queryset = Enroll.objects.all()
    serializer_class = EnrollSerializer
    permission_classes = []


#-----------------------------------------------------------------------------------------------

class ReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = []

    def get_queryset(self):
        course = get_object_or_404(Course, pk=self.kwargs['pk'])
        reviews = Review.objects.filter(course=course)
        return reviews

    def perform_create(self, serializer):
        course = get_object_or_404(Course, pk=self.kwargs['pk'])
        serializer.save(student=self.request.user, course=course)


class ReviewGetDeleteView(generics.RetrieveDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = []
    

#-----------------------------------------------------------------------------------------------

class LikeListCreateView(generics.ListCreateAPIView):
    serializer_class = LikeSerializer
    permission_classes = []

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs['pk'])
        like = ReviewLike.objects.filter(review=review, student=self.request.user)
        return like

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs['pk'])
        serializer.save(student=self.request.user, review=review)


class LikeGetDeleteView(generics.RetrieveDestroyAPIView):
    serializer_class = LikeSerializer
    permission_classes = []

    def get_object(self):
        review = get_object_or_404(Review, pk=self.kwargs['pk'])
        like = get_object_or_404(ReviewLike, review=review, student=self.request.user)
        return like

#-----------------------------------------------------------------------------------------------

class FavouriteCreateView(generics.CreateAPIView):
    serializer_class = FavouriteSerializer
    permission_classes = []

    def perform_create(self, serializer):
        course = get_object_or_404(Course, pk=self.kwargs['pk'])
        serializer.save(student=self.request.user, course=course)



class FavouriteGetDeleteView(generics.RetrieveDestroyAPIView):
    serializer_class = FavouriteSerializer
    permission_classes = []

    def get_object(self):
        course = get_object_or_404(Course, pk=self.kwargs['pk'])
        fav = get_object_or_404(Favourite, course=course, student=self.request.user)
        return fav



class FavouriteListView(generics.ListAPIView):
    serializer_class = FavouriteSerializer
    permission_classes = []

    def get_queryset(self):
        favs =  Favourite.objects.filter(student=self.request.user)
        return favs
#-----------------------------------------------------------------------------------------------