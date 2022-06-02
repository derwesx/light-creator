from django.http import JsonResponse

import tstdb.light_processor as lp


def set_cof_dim(new_cof):
    lp.cofDim = int(new_cof) / 100


functions = dict()
functions['groupOn'] = lp.on_group
functions['groupOff'] = lp.off_group
functions['start'] = lp.activate
functions['tap'] = lp.spawn_scene
functions['sceneRand'] = lp.generate_scene
functions['light_power'] = set_cof_dim

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
