from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render
from django.utils import timezone


def passcard_info_view(request, passcode):
    passcard = Passcard.objects.get(passcode=passcode)
    visits = Visit.objects.filter(passcard=passcard)
    this_passcard_visits = []
    for visit in visits:
        entered_at = timezone.localtime(visit.entered_at)
        time_in_storage = visit.get_duration()
        durations = visit.format_duration(time_in_storage)
        is_strange = visit.is_visit_long(time_in_storage)
        this_passcard_visits.append(
            {
                "entered_at": entered_at,
                "duration": durations,
                "is_strange": is_strange
            })
    context = {
        "passcard": passcard,
        "this_passcard_visits": this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)
