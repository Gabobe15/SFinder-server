from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


LEVEL_CHOICES = [
        ("diploma", "Diploma"),
        ("degree", "Degree"),
    ]

STATUS_CHOICES = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    ]


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    requirement_file = models.FileField(upload_to='files/pdf/', blank=True, null=True)
   
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name


class Courses(models.Model):
    course = models.CharField(max_length=200, blank=True, null=True)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='diploma')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='courses')
    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"
    
    def __str__(self):
        return f"{self.course} ({self.level})"



class UniversityCourses(models.Model):
    university = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        limit_choices_to={"role":"university"}, related_name="university_courses"
    )

    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    available_slots = models.IntegerField(default=0)
    deadline = models.DateField(blank=True, null=True)
    
    class Meta:
        verbose_name = "University course"
        verbose_name_plural = "University courses"
    
    def __str__(self):
        return f"{self.university.fullname} {self.course.course}"
    
    

# Create your models here.
class Application(models.Model):
    student = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        limit_choices_to={'role':'student'}, 
        related_name='student_applications'
    )

    university = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        limit_choices_to={'role': 'university'},
        related_name='university_applications'
    )

    course = models.ForeignKey(Courses, on_delete=models.CASCADE, related_name='course_applications')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    # personal info
    fullname = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField()
    sex = models.CharField(max_length=10, blank=True, null=True)
    phone = models.CharField(max_length=200)
    address = models.TextField(blank=True, null=True)
    county = models.CharField(max_length=100, blank=True, null=True)
    national_id = models.CharField(max_length=100, blank=True, null=True)
    passport_photo = models.FileField(upload_to="images/passport_photos/", blank=True, null=True)
    
    # academic requirements 
    qualification =  models.TextField(blank=True, null=True)
    academic_transcript = models.FileField(upload_to='files/pdf/', blank=True, null=True)
    education_level = models.CharField(max_length=100, blank=True, null=True)
    personal_statement = models.FileField(upload_to='files/pdf/', blank=True, null=True)
    recommendation = models.FileField(upload_to='files/pdf/', blank=True, null=True)
    
    
    class Meta:
        verbose_name = "Application"
        verbose_name_plural = "Applications"
    
    def __str__(self):
        return f"{self.student.email} → {self.university.email}"
    
    
    


