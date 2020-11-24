import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import logging

logger = logging.getLogger(__name__)

nw_graph = {}

def dfs(source,visited,target,remaining_strength,route):
    if source == target:
        return route
    else:
        if remaining_strength == 0:
            return []
        visited.add(source)
        for i in nw_graph[source]['edges']:
            if i not in visited:
                if nw_graph[i]['type'] == 'REPEATER':
                    t = dfs(i,visited,target,remaining_strength*2-1,route+[i])
                else:
                    t = dfs(i,visited,target,remaining_strength-1,route+[i])
                if len(t) > 0:
                    return t
        visited.remove(source)
        return []


@csrf_exempt
def process(request):
    try:
        if request.method == 'POST':
            body = request.body.splitlines()
            command = [i.decode('utf-8') for i in body[0].split()]

            if command[0] == 'CREATE' and command[1] == '/devices':
                req = json.loads(body[-1].decode('utf-8'))
                if req['type'] == 'COMPUTER':
                    nw_graph[req['name']] = {'type' : 'COMPUTER', 'strength' : 5, 'edges' : set()}
                elif req['type'] == 'REPEATER':
                    nw_graph[req['name']] = {'type' : 'REPEATER', 'strength' : 5, 'edges' : set()}
                logger.debug(nw_graph)
                return HttpResponse(str({'network':nw_graph}))

            elif command[0] == 'CREATE' and command[1] == '/connections':
                req = json.loads(body[-1].decode('utf-8'))
                if req['source'] in nw_graph:
                    for i in req['targets']:
                        if i in nw_graph:
                            if i not in nw_graph[req['source']]['edges']:
                                nw_graph[req['source']]['edges'].add(i)
                                nw_graph[i]['edges'].add(req['source'])
                logger.debug(nw_graph)
                return HttpResponse(str({'network':nw_graph}))

            elif command[0] == 'FETCH' and command[1] == '/devices':
                device_list = []
                for i in nw_graph.keys():
                    device_list += [i]
                logger.debug('fetch devices',device_list)
                return HttpResponse(str({'devices':device_list}))

            elif command[0] == 'FETCH':
                params = command[1].split('?')[-1].split('&')
                source = params[0].split('=')[-1]
                target = params[1].split('=')[-1]
                route = []
                if source in nw_graph and target in nw_graph:
                    visited = set()
                    route = dfs(source,visited,target,nw_graph[source]['strength'],[source])
                    logger.debug('fetch route')
                if len(route) == 0:
                    return HttpResponse('Error : No route found between source and target')
                else:
                    return HttpResponse(str({'route':route}))
                    
            elif command[0] == 'MODIFY':
                params = command[1].split('/')
                target = params[2]
                req = json.loads(body[-1].decode('utf-8'))
                if target in nw_graph:
                    nw_graph[target]['strength'] = req['value']
                logger.debug(nw_graph)
                return HttpResponse(str({'network':nw_graph}))        
    except:
        return HttpResponse('500 - Internal server error')