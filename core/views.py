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
    permission_classes = [permissions.AllowAny]
    
class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Courses.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.AllowAny]
    
    

# university 
class UniversityListCreateView(generics.ListCreateAPIView):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer
    permission_classes = [permissions.AllowAny]
    
class UniversityDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer
    permission_classes = [permissions.AllowAny]
    

# university courses 
class UniversityCoursesListCreateView(generics.ListCreateAPIView):
    queryset = UniversityCourses.objects.all()
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
        user = self.request.user 
        if user.role != 'student':
            raise PermissionDenied("Only students can create applications")

        if self.request.user.role == 'student':
            serializer.save(student=self.request.user)
        else:
            return PermissionDenied("Only student can create applications")
        
        # course = serializer.validated_data.get('course')
        # if Application.objects.filter(student=user, course=course).exists():
        #     raise ValidationError("You have already applied for this course.")
        # serializer.save(student=user)
    

class ApplicationDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]


    def get_queryset(self):
        user = self.request.user

        if user.role == 'student':
            return Application.objects.filter(student=user)

        if user.role == 'university':
            return Application.objects.filter(university=user)

        if user.role == 'admin':
            return Application.objects.all()

        return Application.objects.none()  # restricts access for unknown roles


# class ApplicationDetailView(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = ApplicationSerializer
#     permission_classes = [permissions.IsAuthenticated]
    
#     def get_queryset(self):
#         user = self.request.user
#         if user.role == 'student':
#             return Application.objects.filter(student=user)
#         elif user.role == 'university':
#             return Application.objects.filter(university=user.university)
#         elif user.role == 'admin':
#             return Application.objects.all()
#         return Application.objects.all()
    
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
        


    
    # def get_queryset(self):
    #     user = self.request.user
    #     if user.role == 'university':
    #         return Application.objects.filter(university=user)
    #     elif user.role == 'admin':
    #         return Application.objects.all()
    #     return Application.objects.none()
    
    # def perform_update(self, serializer):
    #     user = self.request.user 

    #     if user.role in ["university", "admin"]:
    #         serializer.save()
    #     elif user.role == "student":
    #         if "status" in serializer.validated_data:
    #             raise PermissionDenied("Student can not change status")
    #         serializer.save()
    #     else:
    #         PermissionDenied("Not allowed to update this application")