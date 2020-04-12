from django import template
register = template.Library()

@register.filter
def indx(indexable, i):
    return indexable[i]

@register.filter
def times(count):
    return range(int(count))

@register.filter
def negate(value):
    return -value
