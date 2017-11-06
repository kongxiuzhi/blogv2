from django.template.Library import filter

@register.filter
def cutstr(value,arg):
    return value[-arg:]