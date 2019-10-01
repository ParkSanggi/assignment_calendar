from django import template

register = template.Library()


@register.filter
def convert_next_year(target):
    if target[1] == 12:
        return target[0] + 1
    return target[0]


@register.filter
def convert_next_month(target):
    if target[1] == 12:
        return 1
    else:
        return target[1] + 1


@register.filter
def convert_pre_year(target):
    if target[1] == 1:
        return target[0] - 1
    return target[0]


@register.filter
def convert_pre_month(target):
    if target[1] == 1:
        return 12
    else:
        return target[1] - 1
