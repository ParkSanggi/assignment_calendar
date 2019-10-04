import pickle

from django.core.serializers import serialize
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views import View
import json

from rest_framework.views import APIView
from rest_framework.response import Response

import calendar
from datetime import datetime

from schedule.serializers import ScheduleSerializer
from .models import Schedule


class CreateScheduleView(APIView):
    def post(self, *args, **kwargs):
        print(self.request.data)

        # is_all_day = models.BooleanField()
        # is_repeated = models.BooleanField()

        title = self.request.data.get('schedule_name')
        description = self.request.data.get('schedule_description')

        start_date = [i for i in map(int, self.request.data.get('start_date').split('/'))]
        str_start_time, check_morning = self.request.data.get('start_time').split(' ')
        start_hour, start_minute = map(int, (str_start_time.split(':')))
        if check_morning == 'PM':
            start_hour += 12

        start_date_time = timezone.make_aware(
            datetime(start_date[2], start_date[0], start_date[1], start_hour, start_minute))

        end_date = [i for i in map(int, self.request.data.get('end_date').split('/'))]
        str_end_time, check_morning = self.request.data.get('end_time').split(' ')
        end_hour, end_minute = map(int, (str_end_time.split(':')))
        end_hour, end_minute = map(int, (str_start_time.split(':')))

        end_date_time = timezone.make_aware(
            datetime(end_date[2], end_date[0], end_date[1], end_hour, end_minute))

        if check_morning == 'PM':
            start_hour += 12

        schedule_obj = Schedule.objects.create_or_404(title=title, description=description,
                                                      start_date_time=start_date_time,
                                                      end_date_time=end_date_time, is_all_day=False, is_repeated=False)
        return Response({})


class MakeMonthly(View):
    def get(self, request, *args, year=datetime.today().year, month=datetime.today().month, day=datetime.today().day):

        week_list = self.make_weeks(year, month)
        print(week_list)

        first_day = self.find_first_day_detail(year, month, week_list)
        last_day = self.find_last_day_detail(year, month, week_list)

        queryset = Schedule.objects.filter(end_date_time__gte=first_day, start_date_time__lte=last_day)
        monthly_schedules = json.dumps(ScheduleSerializer(queryset, many=True,
                                                          context={'week_list': week_list, 'year': year,
                                                                   'month': month}).data)

        context = {
            'week_list': week_list,
            'today': (year, month, day),
            'monthly_schedule': monthly_schedules,
        }

        return render(self.request, 'schedule/schedule_monthly_list.html', context)

    def find_first_day_detail(self, year, month, week_list):
        if week_list[0][0] != 1:
            if month == 1:
                pre_year = year - 1
                pre_month = 12
            else:
                pre_year = year
                pre_month = month - 1
            return timezone.make_aware(datetime(pre_year, pre_month, week_list[0][0][1]))
        else:
            return timezone.make_aware(datetime(year, month, 1))

    def find_last_day_detail(self, year, month, week_list):
        if month == 12:
            return timezone.make_aware(datetime(year + 1, 1, week_list[5][6][1]))
        else:
            return timezone.make_aware(datetime(year, month + 1, week_list[5][6][1]))

    def make_weeks(self, year, month):
        weeks = [[None for _ in range(7)] for _ in range(6)]
        month_range = calendar.monthrange(year, month)
        start_idx = 0 if month_range[0] == 6 else month_range[0] + 1

        temp_month = month
        i = start_idx
        n = 1
        w = 0

        while w != 6:
            weeks[w][i] = [temp_month, n]
            i += 1
            n += 1
            if n > month_range[1]:
                n = 1
                temp_month += 1
            if i == 7:
                w += 1
                i = 0

        if start_idx:
            last_month = 12 if month == 1 else month - 1
            last_month_range = calendar.monthrange(year - 1, last_month) if last_month == 12 else calendar.monthrange(
                year, last_month)
            i = start_idx - 1
            n = last_month_range[1]

            while i >= 0:
                weeks[0][i] = [last_month, n]
                i -= 1
                n -= 1
        return weeks
