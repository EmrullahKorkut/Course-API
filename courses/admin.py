from django.contrib import admin

# Register your models here.

from courses import models

admin.site.register(models.User)
admin.site.register(models.Category)
admin.site.register(models.Course)
admin.site.register(models.Lesson)
admin.site.register(models.Enroll)
admin.site.register(models.Cart)
admin.site.register(models.CartContent)
admin.site.register(models.Payment)
admin.site.register(models.Review)
admin.site.register(models.ReviewLike)
admin.site.register(models.Favourite)
