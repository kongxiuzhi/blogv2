from django import template

register = template.Library()

@register.filter
def mycut(value,arg=4):
    if value:
        return value[-arg:]
    else:
        return 0
