from django.http import HttpResponse
from django.shortcuts import render

import calendar
from datetime import datetime

from django.views import View

from .models import Schedule


class ScheduleListView(View):
    def post(self, request, *args, **kwargs):

        week_list = request.POST.get('week_list')
        year = request.POST.get('year')
        month = request.POST.get('month')

        if week_list[0][0] != 1:
            Schedule.objects.filter()



class MakeMonthly(View):
    def get(self, request, *args, year=datetime.today().year, month=datetime.today().month, day=datetime.today().day):

        week_list = self.make_weeks(year, month)

        context = {
            'week_list': week_list,
            'today': (year, month, day),
        }

        return render(self.request, 'schedule/schedule_monthly_list.html', context)

    def make_weeks(self, year, month):
        weeks = [[None for _ in range(7)] for _ in range(6)]
        month_range = calendar.monthrange(year, month)
        start_idx = 0 if month_range[0] == 6 else month_range[0] + 1

        i = start_idx
        n = 1
        w = 0

        while w != 6:
            weeks[w][i] = n
            i += 1
            n += 1
            if n > month_range[1]:
                n = 1
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
                weeks[0][i] = n
                i -= 1
                n -= 1
        return weeks
