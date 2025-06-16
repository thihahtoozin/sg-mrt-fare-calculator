import os
from pprint import pprint
from display_stations import *
from api_request import calc_distance_mrt

stations: dict = {}
intchgs: dict = {}
combined_lines: list = []
lines: list = []
config_dir: str = 'config/'

# clearing screen by detecting underlying operating system
def clear_screen() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')

def read_files() -> None: # read files and fill up our dicts `stations` and `intchgs` ,and list `combined_lines` and `lines`

    # declaring global variables to avoid creating local variables with the same name
    global stations
    global intchgs
    global combined_lines
    global lines
    global config_dir

    files = os.listdir(config_dir)
    lines = [ l.split('.')[0] for l in files ]
    #print(lines)
    for file in files:
        line = file.split('.')[0].upper()
        file_path = config_dir+file
        with open(file_path, "r") as f_handle:
            stations[line] = [f.strip().upper() for f in f_handle.readlines() if f != '\n']
    #print(stations)

    intchgs_lst = list(set(stations[lines[0]]) & set(stations[lines[1]])) # interchanges between 2 lines (only works with two lines)
    for intchg in intchgs_lst:
        first_index = stations[lines[0]].index(intchg)+1
        second_index = stations[lines[1]].index(intchg)+1
        first_code = f"{lines[0]}{first_index}"
        second_code = f"{lines[1]}{second_index}"
        intchgs[intchg] = (first_code, second_code)

    #combined_lines = combine_lines(lines[0], stations[lines[0]], lines[1], stations[lines[1]])
    combined_lines = combine_lines(stations)
    #print(combined_lines)

    #print(intchgs)
    # {'JURONG EAST': ('NS1', 'EW24'), 'RAFFLES PLACE': ('NS25', 'EW14'), 'CITY HALL': ('NS24', 'EW13')}

def get_station(station: str) -> tuple: # station can be station code or station name 

    global stations
    station_name: str = ''
    station_code: str = ''
    station_line: str = ''
    #station_index: int = 0

    if station[:2].isalpha() and station[2:].isdigit(): # for station code
        station_code = station.upper()
        station_line = station_code[:2]
        station_index = int(station_code[2:])

        station_name = stations[station_line][station_index-1]

    else: # for string
        station_name = station.upper()
        for line, stations in stations.items():
            line = line.upper()
            #stations_line = [ l.upper() for l in stations_d[line] ]
            if user_input in [ l.upper() for l in stations_d[line] ]:
                station_code = f"{line}{stations.index(user_input)+1}"
                break

    return (station_line, station_code, station_name)

def calc_num_hops(start_station_code: str, end_station_code: str) -> int: # calculate and returns number of hops between the two stations
    global intchgs

    num_hops: int = 0
    start_station_index: int = int(start_station_code[2:])
    end_station_index: int = int(end_station_code[2:])
    possible_hops: list = []

    #if start_station[:2] == end_station[:2]: # if the start and destination stations are on the same line
    #    num_hops = abs(start_station_index - end_station_index)
    #else: # on different line
    #    start_station_name = get_station(start_station)[-1]
    #    end_station_name = get_station(end_station)[-1]
    #    
    #    start_line = 0 if start_station[:2] == 'EW' else 1 # 0 for EW line, 1 for NS line
    #    for intchg in ew_ns_intchgs_lst:
    #        x = abs(int(ew_ns_intchgs[intchg][start_line][2:]) - int(start_station[2:]))
    #        y = abs(int(ew_ns_intchgs[intchg][int(not start_line)][2:]) - int(end_station[2:]))
    #        possible_hops.append(x+y)
    #    num_hops = min(possible_hops)
    #
    # if there is any interchange for 
        
    return num_hops

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

def bfs_shortest_path(graph: dict, start_station: str ,end_station: str) -> list:
    start_station = start_station.upper()
    end_station = end_station.upper()
    queue: list = [[start_station]] # list of path
    visited: list  = []
    path: list = []
    while queue:
        #print(f"Queue : {queue}")
        path = queue.pop(0)
        #print(f"Path : {path}")
        last_station = path[-1]
        if last_station == end_station:
            return path
        if last_station not in visited:
            visited.append(last_station)

            for neighbour in graph[last_station]:
                if neighbour not in visited:
                    new_path = path + [neighbour]
                    queue.append(new_path)
    return None

def main():
    global combined_lines

    clear_screen()
    read_files()


    start_station_code, end_station_code = prompt(stations, combined_lines)

    start_station_line, _, start_station_name = get_station(start_station_code)
    end_station_line, _, end_station_name = get_station(end_station_code)

    print(f"Starting station : {start_station_name} {start_station_line} {start_station_code}")
    print(f"Ending station : {end_station_name} {end_station_line} {end_station_code}")

    graph = build_graph([station_lists for station_lists in stations.values()])
    #pprint(graph)
    path = bfs_shortest_path(graph, start_station_name, end_station_name)
    print(path)

    #print(f"Ending station : {end_station_name}")
    #num_h = calc_num_hops(start_station_code, end_station_code)
    #print(f"Num hops : {num_h}")
    #distance, duration = calc_distance_mrt(start_station_name, end_station_name)
    #print(f"Distance : {distance:.2f}")
    #print(f"Duration : {duration:.2f}")

if __name__ == '__main__':
    main()
