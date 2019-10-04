from datetime import datetime
from django.utils import timezone

from rest_framework import serializers

from .models import Schedule


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'

    def to_representation(self, instance):
        serializers_data = super().to_representation(instance)
        week_list = self.context['week_list']
        cur_year = self.context['year']
        cur_month = self.context['month']
        schedule_length = (instance.end_date_time - instance.start_date_time).days + 1

        start_year = instance.start_date_time.year
        start_month = instance.start_date_time.month
        start_day = instance.start_date_time.day

        end_month = instance.end_date_time.month
        end_day = instance.end_date_time.day

        start_point = 0

        if cur_month == 1:
            cur_month = 13
            cur_year -= 1

        if start_month < cur_month and start_day < week_list[0][0][1]:
            schedule_length = (instance.end_date_time - timezone.make_aware(
                datetime(cur_year, week_list[0][0][0], week_list[0][0][1]))).days + 1

        else:
            for week in week_list:
                for day in week:
                    if day == [start_month, start_day]:
                        break
                    else:
                        start_point += 1
                if day == [start_month, start_day]:
                    break

        if start_point == 42:
            start_point = 0
            schedule_length = (instance.end_date_time - timezone.make_aware(
                datetime(cur_year, week_list[0][0][0], week_list[0][0][1]))).days + 1

        serializers_data['start_points'] = [start_point]

        if instance.is_repeated:
            kind_of_event = 'event-repeated'
        elif schedule_length >= 2:
            kind_of_event = 'event-consecutive'
        else:
            kind_of_event = ''

        serializers_data['schedule_bars'] = []

        remaining_spaces = 7 if start_point == 0 else 7 - (start_point % 7)
        length_to_apply = remaining_spaces
        temp_schedule_length = schedule_length
        temp_start_point = start_point

        while True:

            if temp_schedule_length > remaining_spaces:

                serializers_data['schedule_bars'].append(
                    f"""<div class="event {kind_of_event} event-start event-end" data-span="{length_to_apply}"
                 data-toggle="popover" data-html="true" data-content='<div class="content-line">
                 <div class="event-consecutive-marking"></div><div class="title">
                 <h5>{instance.title}</h5><h7 class="reservation">{start_year}년 {start_month}월 {start_day}일 – 
                {end_month}월 {end_day}일</h7></div><div class="content-line"><i class="material-icons">notes</i>
                <div class="title"><h7 class="reservation">{instance.description}</h7></div></div>'>{instance.title}</div>""")

                temp_schedule_length -= remaining_spaces

                if temp_schedule_length <= 0:
                    break

                temp_start_point += remaining_spaces
                remaining_spaces = 7

                if temp_schedule_length >= remaining_spaces:
                    length_to_apply = remaining_spaces
                else:
                    length_to_apply = temp_schedule_length

                serializers_data['start_points'].append(temp_start_point)

            else:
                serializers_data['schedule_bars'].append(
                    f"""<div class="event {kind_of_event} event-start event-end" data-span="{temp_schedule_length}"
             data-toggle="popover" data-html="true" data-content='<div class="content-line">
             <div class="event-consecutive-marking"></div><div class="title">
             <h5>{instance.title}</h5><h7 class="reservation">{start_year}년 {start_month}월 {start_day}일 – 
            {end_month}월 {end_day}일</h7></div><div class="content-line"><i class="material-icons">notes</i>
            <div class="title"><h7 class="reservation">{instance.description}</h7></div></div>'>{instance.title}</div>""")
                break

        return serializers_data
