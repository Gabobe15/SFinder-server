from rest_framework import serializers
from .models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'general_requirements','requirement_file']


class CourseSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category', write_only=True, allow_null=True)
    
    
    class Meta:
        model = Courses
        fields = ['id', 'course', 'level', 'category', 'category_id', "deadline"]
    
class UniversityCoursesSerializer(serializers.ModelSerializer):
    university = serializers.CharField(source='university.fullname', read_only=True)
    course = serializers.CharField(source='course.course', read_only=True)

    course_id = serializers.PrimaryKeyRelatedField(
        queryset=Courses.objects.all(),
        source="course"
    )

    class Meta:
        model = UniversityCourses
        # fields = "__all__"
        fields = [
            "id",
            "university",
            "course",
            "course_id",
            "available_slots",
            "requirements",
            "deadline",
        ]
        read_only_fields = ["university"]

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        if hasattr(user, "university"):
            validated_data['university'] = user.university
        return super().create(validated_data)

  
class UniversitySerializer(serializers.ModelSerializer):
    courses_info = UniversityCoursesSerializer(source="universitycourses_set", many=True, read_only=True)
    address = serializers.CharField(source="user.address", read_only=True)
    class Meta:
        model = University 
        fields = ['id', 'name', 'address', 'courses_info', 'user']


class ApplicationSerializer(serializers.ModelSerializer):
    # course_name = serializers.CharField(source='course.course', read_only=True)
    # category_name = serializers.CharField(source='course.category.name', read_only=True)
    # university_name = serializers.CharField(source='university.name', read_only=True)
    university_name = serializers.SerializerMethodField()
    course_name = serializers.SerializerMethodField()

    class Meta:
        model = Application
        fields = '__all__'
        read_only_fields = ["student","status", "created_at"]
        
    def get_university_name(self, obj):
        return obj.university.fullname if obj.university else None  # or another field

    def get_course_name(self, obj):
        return obj.course.course if obj.course else None
        

class ApplicationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Application
        fields = ['id', 'status']