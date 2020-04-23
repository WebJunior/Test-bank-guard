from datacenter.models import Visit
from django.shortcuts import render
from django.utils import timezone


def storage_information_view(request):
    visitors = Visit.objects.filter(leaved_at__isnull=True)
    non_closed_visits = []
    for visitor in visitors:
      if visitor.passcard.is_active:
        entered_moscow_date = timezone.localtime(visitor.entered_at)
        time_in_storage = visitor.get_duration()
        durations = visitor.format_duration(time_in_storage)
        is_strange = visitor.is_visit_long(time_in_storage)
        non_closed_visits.append(
            {
              "who_entered": visitor.passcard.owner_name,
              "entered_at": entered_moscow_date,
              "duration": durations,
              "is_strange": is_strange
            })
    context = {
        "non_closed_visits": non_closed_visits,  
    }
    return render(request, 'storage_information.html', context)


  