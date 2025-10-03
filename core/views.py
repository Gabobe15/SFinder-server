from django.shortcuts import render
from rest_framework import generics, permissions, status  
from .models import *
from .serializers import *
from rest_framework.exceptions import PermissionDenied, ValidationError
from knox.auth import TokenAuthentication
from rest_framework.response import Response



# Create your views here.
# category 
class CategoryListCreateView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    
class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
   
# course 
class CourseListCreateView(generics.ListCreateAPIView):
    queryset = Courses.objects.all()
    serializer_class = CourseSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Courses.objects.all()
    serializer_class = CourseSerializer
  
    

# university courses 
class UniversityCoursesListCreateView(generics.ListCreateAPIView):
    queryset = UniversityCourses.objects.all().order_by('-id')
    serializer_class = UniversityCoursesSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    
    def perform_create(self, serializer):
        user = self.request.user 
        if user.role != 'university':
            raise PermissionDenied("Only university can add course")
        serializer.save(university=user)
    
    
class UniversityCoursesDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UniversityCourses.objects.all()
    serializer_class = UniversityCoursesSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'university':
            return UniversityCourses.objects.filter(university=user)
        return UniversityCourses.objects.none()
    
#Applications
class ApplicationListCreateView(generics.ListCreateAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            return Application.objects.filter(student=user)
        elif user.role == 'university':
            return Application.objects.filter(university=user)
        elif user.role == "admin":
            return Application.objects.all()
        return Application.objects.none()
    
    def perform_create(self, serializer):
        serializer.save(student=self.request.user)

class ApplicationDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]


    def get_queryset(self):
        user = self.request.user

        if user.role == 'student':
            return Application.objects.filter(student=user).order_by('-id')

        if user.role == 'university':
            return Application.objects.filter(university=user).order_by('-id')

        if user.role == 'admin':
            return Application.objects.all().order_by('-id')

        return Application.objects.none()  # restricts access for unknown roles

    
class ApplicationStatusUpdateView(generics.UpdateAPIView):
    serializer_class = ApplicationStatusSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Application.objects.all()


    def patch(self, request, *args, **kwargs):
        application = self.get_object()
        status_choice = request.data.get("status")

        if status_choice not in ["pending","accepted","rejected"]:
            return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)
        
        application.status = status_choice
        application.save()
        return Response({"status": "success", "application_status": application.status})
        
