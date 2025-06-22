
def build_graph(lines: list) -> dict:
    graph: dict = {}
    for line in lines:
        for i in range(len(line)):
            station = line[i]
            if station not in graph:
                graph[station] = []
            if i > 0:
                prev_station = line[i - 1]
                if prev_station not in graph[station]:
                    graph[station].append(prev_station)
                if station not in graph[prev_station]:
                    graph[prev_station].append(station)

    return graph

def build_station_lines(mrt_struct: dict):
    station_lines: dict = {} # {'CITY HALL': ['EW',NS']}
    
    for line, struct in mrt_struct.items():
        for station in struct['path']:
            if station not in station_lines:
                station_lines[station] = [line]
            else:
                station_lines[station].append(line)
    
    return station_lines

def bfs_all_paths(graph: dict, start_station: str ,end_station: str) -> list: # list of list(paths)
    start_station = start_station.upper()
    end_station = end_station.upper()
    queue: list = [[start_station]] # list of path
    paths: list = [] # list of all possible paths
    path: list = []
    while queue:
        path = queue.pop(0)
        last_station = path[-1]

        if last_station == end_station:
            paths.append(path)
        else:
            for neighbour in graph[last_station]:
                if neighbour not in path:
                    new_path = path + [neighbour]
                    queue.append(new_path)
    return paths

def bfs_top_shortest_paths(top: int, graph: dict, start_station: str, end_station: str) -> list:
    start_station = start_station.upper()
    end_station = end_station.upper()
    
    queue = [[start_station]]
    shortest_paths = []
    shortest_len = None

    while queue:
        path = queue.pop(0)
        last_station = path[-1]

        if last_station == end_station:
            if len(shortest_paths) < top:
                shortest_paths.append(path)
            else:
                break
        else:
            for neighbor in graph[last_station]:
                if neighbor not in path:  # avoid cycles
                    new_path = path + [neighbor]
                    queue.append(new_path)

    return shortest_paths

def count_line_changes(path, station_lines):
    if len(path) < 2:
        return 0

    first_station, second_station = path[0], path[1]
    possible_lines = list(set(station_lines.get(first_station, [])) & set(station_lines.get(second_station, [])))

    if not possible_lines:      # if stations are not connected
        return float('inf')

    min_changes = float('inf')

    for initial_line in possible_lines:
        changes = 0
        current_line = initial_line

        for i in range(1, len(path)):
            prev = path[i - 1]
            curr = path[i]
            prev_lines = station_lines.get(prev, [])
            curr_lines = station_lines.get(curr, [])

            if current_line in prev_lines and current_line in curr_lines:
                continue  # No changes
            else:
                shared = set(prev_lines) & set(curr_lines) # This can have more common lines though we want to expect only one
                if shared:
                    current_line = list(shared)[0] # There is a problem here (not a good pratice for multiple common lines for interchanges with 3 for more lines)
                    changes += 1
                else:
                    return float('inf')  # Invalid switch

        min_changes = min(min_changes, changes)

    return min_changes

# THIS WOULD CALCULATE ALL POSSIBLE PATHS AND STORE IN A FILE
#paths = bfs_all_paths(graph, 'CITY HALL', 'TUAS LINK') # should return list of all possible paths
#with open('all_paths.txt', 'w') as f:
#    for path in paths:
#        f.write('->'.join(map(str, path)) + '\n')

if __name__ == '__main__':
    paths = bfs_top_shortest_paths(5, graph, 'LAVENDER', 'TUAS LINK') # should return list of all possible paths
    min_changes = float('inf')
    best_path = []

    for path in paths:
        changes = count_line_changes(path, station_lines)
        if changes < min_changes:
            min_changes = changes
            best_path = path

    print(best_path)
    print(f"Number for line changes {min_changes}")
