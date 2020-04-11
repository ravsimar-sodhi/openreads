from django import template
register = template.Library()

@register.filter
def indx(indexable, i):
    return indexable[i]

def incr(i, j):
    return i+j