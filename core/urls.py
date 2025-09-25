from django.urls import path
from .views import *


urlpatterns = [
    # category
    path('categories', CategoryListCreateView.as_view(), name='category-list'),
    path('categories/<int:pk>', CategoryDetailView.as_view(), name='category-detail'),
    
    # courses 
    path('courses/', CourseListCreateView.as_view(), name='course-list'),
    path('courses/<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
    
    # univerisities
    path('universities', UniversityListCreateView.as_view(), name='university-list'),
    path('universities/<int:pk>', UniversityDetailView.as_view(), name='university-detail'),
    
    # universitycourse 
    path('university-courses/', UniversityCoursesListCreateView.as_view(), name='universitycourses-list'),
    path('university-courses/<int:pk>', UniversityCoursesDetailView.as_view(), name='universitycourses-detail'),
    
    # application
    path('applications/', ApplicationListCreateView.as_view(), name='application-list'),
    path('applications/<int:pk>/', ApplicationDetailView.as_view(), name='application-detail'),
    path('applications/<int:pk>/status/', ApplicationStatusUpdateView.as_view(), name='application-status'),
]
