from django.contrib import admin
from .models import  Courses, University, UniversityCourses, Application,Category
# Register your models here.
admin.site.register((Courses,University,UniversityCourses,Application,Category))