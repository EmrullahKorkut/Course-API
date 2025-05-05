from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

from PIL import Image



class User(AbstractUser):
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=True)
    email = models.EmailField(blank=False, null=False, unique=True)

    def which_role(self):
        if self.is_superuser:
            return f'ADMIN'
        if self.is_teacher:
            return f'Teacher'
        if self.is_student:
            return f'Student'
        
    def __str__(self):
        return f'{self.username} {self.last_name} --> {self.which_role()}'
    


class Profile(models.Model):
    pass





class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}'
    


class Course(models.Model):
    category = models.ManyToManyField(Category, blank=True, related_name='courses')

    title = models.CharField(max_length=200)
    description = models.TextField(max_length=2000)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    crated_date = models.DateTimeField(auto_now_add=True)
    images = models.ImageField(null=True, blank=True, upload_to='course-images')

    def __str__(self):
        return f'{self.title}'



class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')

    title = models.CharField(max_length=200)
    images = models.ImageField(null=True, blank=True, upload_to='lesson-images')
    video = models.FileField(null=True, blank=True, upload_to='lesson-videos/')
    description = models.TextField(max_length=2000)


    def __str__(self):
        return f'{self.title} -> {self.course.title}'
    


class Enroll(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enroll_students')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enroll_courses')

    enroll_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f'{self.student.username} - {self.course.title}'
    


class Cart(models.Model):
    student = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_cart')
    
    def __str__(self):
        return f"{self.student.username}'s card: "
    


class CartContent(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_content')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='cart_course')
    
    class Meta:
        unique_together = ('cart', 'course')
    
    def __str__(self):
        return f"{self.course.title} is in the {self.cart.student.username}'s basket"
    


class Payment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    course = models.ManyToManyField(CartContent, related_name='courses', blank=False, null=False)

    amount = models.DecimalField(max_digits=8, decimal_places=2)


    def __str__(self):
        return f"{self.student.username} - for courses in cart {self.amount} TL"



class Review(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_owner')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='review_course')

    point = models.IntegerField()
    commet_header = models.CharField(max_length=50)
    comment = models.TextField(max_length=200)
    review_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'({self.student.username}) commented.'
    


class ReviewLike(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='like_owner')
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='liked_review')

    class Meta:
        unique_together = ['review', 'student']

    def __str__(self):
        return f'{self.student.username} liked this review ({self.review.commet_header})'



class Favourite(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fav_user')
    course = models.ManyToManyField(Course, related_name='fav_course')

    def __str__(self):
        return f'{self.student.username} add ({self.course.title}) favorite'
    
