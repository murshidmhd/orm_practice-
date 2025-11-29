from django.http import JsonResponse
from django.db.models import Count, Avg, Max, Min
from practice.models import Student


def test_annotate(request):
    qs = Student.objects.aggregate(
        total=Count("id"), avg=Avg("score"), max=Max("score"), min=Min("score")
    )

    return JsonResponse(list(qs), safe=False)
