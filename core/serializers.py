from rest_framework import serializers
from .models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name','requirement_file']


class CourseSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category', write_only=True, allow_null=True)
    
    
    class Meta:
        model = Courses
        fields = ['id', 'course', 'level', 'category', 'category_id']
    
class UniversityCoursesSerializer(serializers.ModelSerializer):
    university = serializers.CharField(source='university.fullname', read_only=True)
    university_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role='university'),
        source="university",
    )


    course = serializers.CharField(source='course.course', read_only=True)
    level = serializers.CharField(source='course.level', read_only=True)
    requirement_file = serializers.CharField(source='course.category.requirement_file', read_only=True)
    course_id = serializers.PrimaryKeyRelatedField(
        queryset=Courses.objects.all(),
        source="course"
    )

    formatted_deadline = serializers.SerializerMethodField()

    
    # Add these fields for frontend
    has_applied = serializers.SerializerMethodField()
    is_past_deadline = serializers.SerializerMethodField()
    is_available = serializers.SerializerMethodField()

    class Meta:
        model = UniversityCourses
        fields = [
            "id",
            "university",
            "university_id",
            "course",
            "course_id",
            "available_slots",
            "deadline",
            'formatted_deadline',
            "has_applied",
            "is_past_deadline",
            "is_available",
            'requirement_file',
            'level'
        ]
        read_only_fields = ["university", "has_applied", "is_past_deadline", "is_available", 'requirement_file',
            'level']
        

    def create(self, validated_data):
        return super().create(validated_data)
    
    def get_formatted_deadline(self, obj):
        if obj.deadline:
            return obj.deadline.strftime("%b %d, %Y")  # "Jan 01, 2026" format
        return None
    
    def get_has_applied(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated and request.user.role == 'student':
            return Application.objects.filter(
                student=request.user, 
                course=obj.course,
                university=obj.university
            ).exists()
        return False
    
    def get_is_past_deadline(self, obj):
        if obj.deadline:
            from django.utils import timezone
            return obj.deadline < timezone.now().date()
        return False
    
    def get_is_available(self, obj):
        # Course is available if:
        # 1. Has available slots
        # 2. Deadline hasn't passed
        # 3. Deadline is set (not null)
        return (obj.available_slots > 0 and 
                not self.get_is_past_deadline(obj) and 
                obj.deadline is not None)


class ApplicationSerializer(serializers.ModelSerializer):
    university_name = serializers.SerializerMethodField(source="university.fullname", read_only=True)
    course_name = serializers.SerializerMethodField(source="course.course", read_only=True)
    student_id = serializers.IntegerField(source='student.id', read_only=True)  # Add this

    class Meta:
        model = Application
        fields = '__all__'
        read_only_fields = ["student","status", "created_at"]
        
    def get_university_name(self, obj):
        return obj.university.fullname if obj.university else None

    def get_course_name(self, obj):
        return obj.course.course if obj.course else None

class ApplicationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Application
        fields = ['id', 'status']




