from django import template
from jalali_date import date2jalali, datetime2jalali

register = template.Library()

@register.filter(name='j_time')
def jalali_time(value):
    return datetime2jalali(value)

@register.filter(name='j_date')
def jalali_date(value):
    return date2jalali(value)

@register.filter(name='j_day')
def jalali_day(value):
    jalali_date = date2jalali(value)
    return jalali_date.day

@register.filter(name='j_month')
def jalali_month_name_farsi(value):
    jalali_date = date2jalali(value)
    month_names = ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند']
    return month_names[jalali_date.month - 1]

@register.filter(name='j_year')
def jalali_year(value):
    jalali_date = date2jalali(value)
    return jalali_date.year

@register.filter(name='digits')
def digits(value):
    return "{:,}".format(value)
