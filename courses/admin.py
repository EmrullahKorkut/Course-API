from django.contrib import admin

# Register your models here.

from courses import models

admin.site.register(models.User)