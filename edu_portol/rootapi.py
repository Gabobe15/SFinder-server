from django.urls import path, include

urlpatterns = [
    path('auth/', include('auth_app.urls')),
    path('admissions/', include('core.urls'))
]