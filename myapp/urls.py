
from django.contrib import admin
from django.urls import path, include
from myapp.home import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('schedule.urls')),
]
