from django.shortcuts import render
from django.utils import timezone
from django.views import View
import json

from rest_framework.views import APIView
from rest_framework.response import Response

import calendar
from datetime import datetime

from schedule.serializers import ScheduleSerializer, DailyScheduleSerializer
from .models import Schedule


class MakeDailyListView(View):
    def get(self, *args, **kwargs):

        today_year = datetime.today().year
        today_month = datetime.today().month
        today_day = datetime.today().day

        today_midnight = timezone.make_aware(datetime(today_year, today_month, today_day, 23, 59, 59))

        if today_day == 1 and today_month == 1:
            yester_day_midnight = timezone.make_aware(datetime(today_year-1, 12, 31, 23, 59, 59))
        else:
            yester_day_midnight = timezone.make_aware(datetime(today_year, today_month, today_day, 23, 59, 59))

        queryset = Schedule.objects.filter(end_date_time__gt=yester_day_midnight, start_date_time__lt=today_midnight)
        schedules = json.dumps(DailyScheduleSerializer(queryset, many=True).data)
        context = {'schedules': schedules}
        return render(self.request, 'schedule/schedule_daily.html', context)


class CreateScheduleView(APIView):
    def post(self, *args, **kwargs):
        title = self.request.data.get('schedule_name')
        description = self.request.data.get('schedule_description')
        start_date_time = self.make_date_time_obj('start')
        end_date_time = self.make_date_time_obj('end')
        is_all_day = True if self.request.data.get('is_all_day') == 'checked' else False
        monthly_repeat = True if self.request.data.get('monthly_repeat') == 'checked' else False

        schedule_obj = Schedule.objects.create(title=title, description=description, start_date_time=start_date_time,
                                               end_date_time=end_date_time, is_all_day=is_all_day,
                                               is_repeated=monthly_repeat)
        return Response({})

    def make_date_time_obj(self, status):
        date = [i for i in map(int, self.request.data.get(f'{status}_date').split('/'))]
        str_time, check_morning = self.request.data.get(f'{status}_time').split(' ')
        hour, minute = map(int, (str_time.split(':')))
        if check_morning == 'PM':
            hour += 12

        datetime_obj = timezone.make_aware(datetime(date[2], date[0], date[1], hour, minute))

        return datetime_obj


class MakeMonthly(View):
    def get(self, request, *args, year=datetime.today().year, month=datetime.today().month, day=datetime.today().day):

        week_list = self.make_weeks(year, month)
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
        first_day_of_week, last_day = calendar.monthrange(year, month)
        start_day_of_month_idx = 0 if first_day_of_week == 6 else first_day_of_week + 1

        temp_month = month
        temp_idx = start_day_of_month_idx
        temp_day = 1
        what_week = 0

        while what_week != 6:
            weeks[what_week][temp_idx] = [temp_month, temp_day]
            temp_idx += 1
            temp_day += 1
            if temp_day > last_day:
                temp_day = 1
                temp_month += 1
            if temp_idx == 7:
                what_week += 1
                temp_idx = 0

        if start_day_of_month_idx:
            last_month = 12 if month == 1 else month - 1
            last_month_range = calendar.monthrange(year - 1, last_month) if last_month == 12 else calendar.monthrange(
                year, last_month)
            temp_idx = start_day_of_month_idx - 1
            temp_day = last_month_range[1]

            while temp_idx >= 0:
                weeks[0][temp_idx] = [last_month, temp_day]
                temp_idx -= 1
                temp_day -= 1
        return weeks
