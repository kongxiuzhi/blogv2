from django import template

register = template.Library()

@register.filter
def mycut(value,arg=4):
    return value[-arg:]