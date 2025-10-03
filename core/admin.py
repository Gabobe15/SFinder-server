from django.contrib import admin
from .models import  Courses, UniversityCourses, Application,Category
# Register your models here.
admin.site.register((Courses,UniversityCourses,Application,Category))