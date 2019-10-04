from django.urls import path
from .views import *

app_name = 'schedule'

urlpatterns = [
    path('', MakeMonthly.as_view()),
    path('<int:year>/<int:month>/<int:day>/', MakeMonthly.as_view(), name='monthly'),
    path('daily/', MakeDailyListView.as_view(), name='create_schedule'),
    path('create_schedule/', CreateScheduleView.as_view(), name='create_schedule'),
]