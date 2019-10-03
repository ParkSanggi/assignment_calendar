from rest_framework import serializers

from .models import Schedule


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ('title', 'description', 'is_all_day')

    def to_representation(self, instance):
        serializers_data = super().to_representation(instance)
        week_list = self.context['week_list']
        cur_year = self.context['year']
        cur_month = self.context['month']
        schedule_length = (instance.end_date_time - instance.start_date_time).days + 1

        start_year = instance.start_date_time.year
        start_month = instance.start_date_time.month
        start_day = instance.start_date_time.day
        start_hour = instance.start_date_time.hour
        start_minute = instance.start_date_time.minute

        end_year = instance.end_date_time.year
        end_month = instance.end_date_time.month
        end_day = instance.end_date_time.day
        end_hour = instance.end_date_time.hour
        end_minute = instance.end_date_time.minute

        start_point = 0
        if start_month < cur_month and start_day < week_list[0][0][1]:
            pass

        else:
            for week in week_list:
                for day in week:
                    if day == [start_month, start_day]:
                        break
                    else:
                        start_point += 1
                if day == [start_month, start_day]:
                    break

        serializers_data['start_points'] = [start_point]

        if instance.is_repeated:
            kind_of_event = 'event-repeated'
        elif schedule_length >= 2:
            kind_of_event = 'event-consecutive'
        else:
            kind_of_event = ''

        serializers_data['schedule_bars'] = []

        remaining_spaces = 6 - (start_point % 7)
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
            <div class="title"><h7 class="reservation">{instance.description}</div>'>{instance.title}</div>""")

                temp_schedule_length -= remaining_spaces

                if temp_schedule_length <= 0:
                    break

                remaining_spaces = 7

                if temp_schedule_length >= remaining_spaces:
                    length_to_apply = remaining_spaces
                else:
                    length_to_apply = temp_schedule_length

                temp_start_point += remaining_spaces + 1
                serializers_data['start_points'].append(temp_start_point)

        return serializers_data

        # serializers_data['start'] = {}
        # serializers_data['start']['year'] = instance.start_date_time.year
        # serializers_data['start']['month'] = instance.start_date_time.month
        # serializers_data['start']['day'] = instance.start_date_time.day
        # serializers_data['start']['hour'] = instance.start_date_time.hour
        # serializers_data['start']['minute'] = instance.start_date_time.minute
        #
        # serializers_data['end'] = {}
        # serializers_data['end']['year'] = instance.end_date_time.year
        # serializers_data['end']['month'] = instance.end_date_time.month
        # serializers_data['end']['day'] = instance.end_date_time.day
        # serializers_data['end']['hour'] = instance.end_date_time.hour
        # serializers_data['end']['minute'] = instance.end_date_time.minute
