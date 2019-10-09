from django.urls import path
from .views import *

app_name = 'schedule'

urlpatterns = [
    path('', MakeMonthly.as_view(), name='monthly_basic'),
    path('<int:year>/<int:month>/<int:day>/', MakeMonthly.as_view(), name='monthly'),
    path('daily/', MakeDailyListView.as_view(), name='daily_basic'),
    path('daily/<int:month>/<int:day>/<int:year>/', MakeDailyListView.as_view(), name='daily'),
    path('create_schedule/', CreateScheduleView.as_view(), name='create_schedule'),
]