from django.http import JsonResponse

from tstdb.light_processor import on_group, activate, turn_all_onf

functions = dict()
functions['group'] = on_group
functions['start'] = activate
functions['effect1'] = turn_all_onf


def process_click(request):
    result = dict()
    data = request.POST
    if not (functions.__contains__(data['methodId'])):
        result['method'] = 'no action for the button'
        return JsonResponse(result)

    session_key = request.session.session_key

    if len(data['params']) == 0:
        functions[data['methodId']]()
    else:
        functions[data['methodId']](*data['params'].split(','))

    result['method'] = functions[data['methodId']].__name__
    return JsonResponse(result)
