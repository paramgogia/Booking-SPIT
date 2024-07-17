from django import template
from ..models import aTimeSlot
register = template.Library()

@register.filter
def get_timeslot( i, j):
    timeslots = aTimeSlot.objects.all()
    return timeslots.get(slot=str(i), room=str(j))
