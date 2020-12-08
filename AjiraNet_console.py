ajira_net = {}

def dfs(source,visited,target,remaining_strength,route):
    if source == target:
        return route
    else:
        if remaining_strength == 0:
            return []
        visited.add(source)
        routes = []
        for i in ajira_net[source]['connections']:
            if i not in visited:
                if ajira_net[i]['type'] == 'REPEATER':
                    t = dfs(i,visited,target,remaining_strength*2-1,route+[i])
                elif ajira_net[i]['type'] == 'BRIDGE':
                    t = dfs(i,visited,target,remaining_strength-2,route+[i])
                else:
                    t = dfs(i,visited,target,remaining_strength-1,route+[i])
                if len(t) > 0:
                    routes.append([len(t),t])
        visited.remove(source)
        if len(routes) > 0:
            t = min(routes)
            return t[1]
        else:
            return []

def add(device_type,device_name):
    # print('add',device_type,device_name)
    if device_name not in ajira_net:
        if device_type == 'COMPUTER':
            ajira_net[device_name] = {'type' : device_type, 'strength' : 5, 'connections' : set()}
        else:
            ajira_net[device_name] = {'type' : device_type, 'connections' : set()}
        return 'Successfully added '+device_name+'.'
    else:
        return 'Error: That name already exists.'

def connect(source,destination):
    # print('connect',source,destination)
    if source == destination:
        return 'Error: Cannot connect device to itself.'
    else:
        if source in ajira_net and destination in ajira_net:
            if source not in ajira_net[destination]['connections']:
                ajira_net[destination]['connections'].add(source)
                ajira_net[source]['connections'].add(destination)
                return 'Successfully connected.'
            else:
                return 'Error: Devices are already connected.'
        else:
            return 'Error: Node not found.'

def info_route(source,destination):
    # print('info_route')
    if source in ajira_net and destination in ajira_net:
        if ajira_net[source]['type'] == 'COMPUTER' and ajira_net[destination]['type'] == 'COMPUTER':
            visited = set()
            route = dfs(source,visited,destination,ajira_net[source]['strength'],[source])
            n = len(route)
            if n == 0:
                return 'Error: Route not found!'
            elif n == 1:
                return route[0] + ' -> ' + route[0]
            else:
                response = route[0]
                for i in range(1,n):
                    response += ' -> ' + route[i]
                return response
        else:
            return 'Error: Route cannot be calculated with a repeater or bridge.'
    else:
        return 'Error: Node not found.'

def set_device_strength(device_name,strength):
    # print('set_device_strength',device_name,strength)
    if strength < 0:
        return 'Error: Strength cannot be negetive.'
    if device_name in ajira_net:
        if ajira_net[device_name]['type'] != 'REPEATER':
            ajira_net[device_name]['strength'] = strength
            return 'Successfully defined strength.'
        else:
            return 'Error: Strength cannot be defined for REPEATER.'
    else:
        return 'Error: Node not found.'

def add_bridge(bridge_name,bridge_operation):
    # print('add_bridge',bridge_name,bridge_operation)
    if bridge_name not in ajira_net:
        ajira_net[bridge_name] = {'type' : 'BRIDGE', 'operation' : bridge_operation, 'connections' : set()}
        return 'Successfully added '+bridge_name+'.'
    else:
        return 'Error: That name already exists.'

def send_message(source,destination,message):
    if source in ajira_net and destination in ajira_net:
        if ajira_net[source]['type'] == 'COMPUTER' and ajira_net[destination]['type'] == 'COMPUTER':
            visited = set()
            route = dfs(source,visited,destination,ajira_net[source]['strength'],[source])
            n = len(route)
            if n == 0:
                return 'Error: Route not found!'
            else:
                operation = ''
                for i in route:
                    if ajira_net[i]['type'] == 'BRIDGE':
                        operation = ajira_net[i]['operation']
                if operation == 'UPPER':
                    return message.upper()
                elif  operation == 'LOWER':
                    return message.lower()
                else:
                    return message
        else:
            return 'Error: Route cannot be calculated with a repeater or bridge.'
    else:
        return 'Error: Node not found.'


if __name__ == '__main__':
    keep_running = True
    while keep_running:
        command = input().split()
        # print(command)
        response = ''
        if len(command) == 0:
            response = 'Error: Invalid command syntax.'
        elif command[0] == 'ADD' and len(command) == 3 and (command[1] == 'COMPUTER' or command[1] == 'REPEATER') and any(ch.isalpha() for ch in command[2]):
            response = add(command[1],command[2])
        elif command[0] == 'ADD' and len(command) == 4 and command[1] =='BRIDGE' and any(ch.isalpha() for ch in command[2]) and command[3] in {'UPPER','LOWER'}:
            response = add_bridge(command[2],command[3])
        elif command[0] == 'CONNECT' and len(command) == 3:
            response = connect(command[1],command[2])
        elif command[0] == 'INFO_ROUTE'  and len(command) == 3:
            response = info_route(command[1],command[2])
        elif command[0] == 'SET_DEVICE_STRENGTH' and len(command) == 3:
            try:
                response = set_device_strength(command[1],int(command[2]))
            except ValueError:
                response = 'Error: Invalid command syntax.'
        elif command[0] == 'SEND'  and len(command) > 3:
            response = send_message(command[1],command[2],''.join(command[3:]))
        # elif command[0] == 'print':
        #     for k in ajira_net.keys():
        #         print(k,ajira_net[k])
        else:
            response = 'Error: Invalid command syntax.'
        print(response)
