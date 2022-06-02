from django.http import JsonResponse

import tstdb.light_processor as lp

functions = dict()
functions['group'] = lp.on_group
functions['start'] = lp.activate
functions['scene1'] = lp.spawn_scene
functions['sceneRand'] = lp.generate_scene
functions['effect1'] = lp.plav
#

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
