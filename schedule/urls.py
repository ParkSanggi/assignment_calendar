from django.urls import path
from .views import *

app_name = 'schedule'

urlpatterns = [
    path('monthly/', MakeMonthly.as_view(),),
    path('monthly/<int:year>/<int:month>/<int:day>/', MakeMonthly.as_view(), name='monthly'),

]