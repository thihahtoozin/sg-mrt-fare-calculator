import os
from pprint import pprint
from display_stations import *
from api_request import calc_distance_mrt
from fare_calc import *
from find_paths import *
from display_path import *

# static variables
config_dir: str = 'config/mrt_lines/'
price_scheme: str = 'config/fare.conf'

# dynamic variables (these variables are dynamically updated by data read under `config/` directory)
mrt_struct: dict = {}           # stores station informations 
# = {
#    'EW': {
#           'path': ['Tampines','Simei',...]
#           'codes': ['EW1', 'EW2', ...]
#           'start_index': 1,
#          }
#     'NS': {
#           'path': []
#           'codes': ['NS1', 'NS2', ...]
#           'start_index': 1,
#          }
#    }
combined_lines: list = []       # stores combined list of all stations registered under `config/`
mrt_lines: list = []            # stores a list of all registered mrt lines

def read_files() -> None: # read files and fill up our dict `mrt_struct`, list `combined_lines` and `mrt_lines`

    # declaring global variables to avoid creating local variables with the same name
    global mrt_struct
    global combined_lines
    global mrt_lines
    global config_dir
    global start_index

    files = os.listdir(config_dir)
    #mrt_lines = [ file.split('.')[0].upper() for file in files ]
    #print(mrt_lines) # ['EW', 'NS', 'CG']
    for file in files:
        line = file.split('.')[0].upper()
        mrt_struct[line] = {}                # e.g. {'EW': {}}
        mrt_lines.append(line)
        file_path = config_dir+file
        with open(file_path, "r") as f_handle:
            read_lines = [f.strip().upper() for f in f_handle.readlines() if f != '\n'] 
            mrt_struct[line]['start_index'] = int(read_lines[0]) # take the first line as starting index
            mrt_struct[line]['path'] = read_lines[1:] # `[1:]` excludes the first line in the file
            mrt_struct[line]['codes'] = [f"{line}{i + mrt_struct[line]['start_index']}" for i in range(len(mrt_struct[line]['path']))]
    #pprint(mrt_struct)
    #print(mrt_lines)

    combined_lines = combine_lines(mrt_struct)
    #print(combined_lines)

def get_station(station: str) -> tuple: # station can be station code or station name 

    global mrt_struct
    station_name: str = ''
    station_code: str = ''
    station_line: str = ''
    station_index: int = 0

    if station[:2].isalpha() and station[2:].isdigit(): # for station code
        station_code = station.upper()  # e.g. EW3
        station_line = station_code[:2] # e.g. EW
        base_station_index = mrt_struct[station_line]['start_index']
        station_index = int(station_code[2:])

        station_name = mrt_struct[station_line]['path'][station_index-base_station_index]

    else: # for string
        station_name = station.upper()
        for line, line_struct in mrt_struct.items():
            if station in [ s.upper() for s in line_struct['path'] ]: # making sure `stations` is in upper case
                base_station_index = line_struct['start_index']
                station_code = f"{line}{line_struct['path'].index(station)+base_station_index}"
                station_line = line

    return (station_line, station_code, station_name)

def main():
        
    global combined_lines

    clear_screen()
    read_files()

    start_station_code, end_station_code = prompt(mrt_struct, combined_lines)

    start_station_line, _, start_station_name = get_station(start_station_code)
    end_station_line, _, end_station_name = get_station(end_station_code)

    print(f"Starting station : '{start_station_name}':{start_station_line}:{start_station_code}")
    print(f"Ending station : '{end_station_name}':{end_station_line}:{end_station_code}")

    # building the `graph` to calculate 
    graph: dict = build_graph([struct['path'] for struct in mrt_struct.values()])
    # building the `station_lines`
    station_lines: dict = build_station_lines(mrt_struct)

    # finding the best path
    paths = bfs_top_shortest_paths(5, graph, start_station_name, end_station_name)
    min_changes = float('inf')
    best_path = []
    for path in paths:
        changes = count_line_changes(path, station_lines)
        if changes < min_changes:
            min_changes = changes
            best_path = path
    print(best_path)
    print(f"Line change(s) : {min_changes}")

    #print(f"Ending station : {end_station_name}")
    num_h = len(best_path)-1
    print(f"Num hops : {num_h}")
    distance, duration = calc_distance_mrt(start_station_name, end_station_name)
    distance = round(distance,1)

    discount_percent = discount_calc()
    price_ranges: list = load_prices(price_scheme)
    price = fare_calc(price_ranges, distance, discount_percent)

    annotated_path = annotate_path(best_path, station_lines)

    print(f"Distance : {distance:.2f}")
    print(f"Duration : {duration:.2f}")
    print(f"Discount : {discount_percent * 100}%")
    print(f"Price : {price:.2f}")

    print(annotated_path)

if __name__ == '__main__':
    main()
