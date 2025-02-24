from django import template
from jalali_date import date2jalali, datetime2jalali

register = template.Library()

@register.filter(name='j_time')
def jalali_time(value):
    return datetime2jalali(value)

@register.filter(name='j_date')
def jalali_date(value):
    return date2jalali(value)

@register.filter(name='digits')
def digits(value):
    return "{:,}".format(value)