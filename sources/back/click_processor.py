from django.http import JsonResponse

import sources.back.light_controller as lp


def process_click(request):
    data = request.POST
    session_key = request.session.session_key
    lp.catchRequest(data)
    return JsonResponse(data)
