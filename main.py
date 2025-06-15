import os
from pprint import pprint
from display_stations import combine_lines, display
from api_request import calc_distance_mrt

#ew_file: str = "config/EW.txt"
#ns_file: str = "config/NS.txt"

stations: dict = {}
intchgs: dict = {}
combined_lines: list = []
lines: list = []

#ew_stations: list = [] # Green Line EW33 to EW1
#ns_stations: list = [] # Red Line   NS1  to NS28
#ew_ns_display: list = [] # Combined List of Green Line and Red Line

#ew_ns_intchgs_lst: list = [] # list of interchanges across EW and NS lines
#ew_ns_intchgs: dict = {} # record of interchanges across EW and NS lines

# clearing screen by detecting underlying operating system
def clear_screen() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')

def read_files() -> None: # read files and fill up our dicts `stations` and `intchgs` ,and list `combined_lines` and `lines`

    # declaring global variables to avoid creating local variables with the same name
    global stations
    global intchgs
    global combined_lines
    global lines
    #global ew_ns_intchgs_lst
    #global ew_ns_intchgs

    files = os.listdir('config/')[:2] # [:2] limits to two files
    lines = [ l.split('.')[0] for l in files ]
    #print(lines)
    for file in files:
        line = file.split('.')[0].upper()
        with open(file, "r") as ew_f:
            stations[line] = [f.strip() for f in ew_f.readlines() if f != '\n']

    intchgs_lst = list(set(stations[lines[0]]) & set(stations[lines[1]])) # interchanges between 2 lines (only works with two lines)
    for intchg in intchgs_lst:
        first_index = stations[lines[0]].index(intchg)+1
        second_index = stations[lines[1]].index(intchg)+1
        first_code = f"{lines[0]}{first_index}"
        second_code = f"{lines[1]}{second_index}"
        intchgs[intchg] = (first_code, second_code)

    combined_lines = combine_lines(lines[0], stations[lines[0]], lines[1], stations[lines[1]])

    #print(intchgs_lst)
    #print(intchgs)
    # intchgs = { 'City Hall': (EW13, NS10), 'Raffle Place': (EW14,NS9) }

def prompt_stations(stations: list, line: str = 'EW') -> str: # this function returns station code as a string

    # initializing the return value as empty string
    result: str = ''

    # Displaying a list of stations along with station codes
    display(stations)
    #for station_i in range(len(stations)):
    #    print(f"[{line}{station_i + 1}]:{stations[station_i]}")

    # getting user input and validating
    stations = [s.lower() for s in stations]
    user_input = input("Enter station name or number to choose : ").strip()
    user_input = user_input.lower()
    print(user_input)
    
    if user_input.isdigit(): # for index number
        print("Digit")
        #result = line + user_input
        #get the name on the combined list using the index number
        #search for both lists on the stations dict
        #if find on stations[line[0]] => {line[0]}{user_input}, if find on red, if find on both, if find on none
    elif user_input[:2].isalpha() and user_input[2:].isdigit(): # for station code
        print("Station Code")    
        result = user_input[2:]
    #elif user_input == 'b' or user_input == 'back':
    #    pass # letting the return value remain zero(0).
    else: # for string
        print("String")
        result = line + str(stations.index(user_input.lower()) + 1)

    clear_screen()
    return result

def prompt(starting: bool = True) -> int:
    global ew_stations
    global ns_stations
    
    if starting:
        travel_status = "starting"
    else:
        travel_status = "ending"

    prompt_done: bool = False
    while not prompt_done:
        user_input = input(f"Is your {travel_status} Station in Green line or Red line(g/r) : ").strip()
        user_input = user_input.lower()
        if user_input in ['g', 'r', "green", "red"]:
            if user_input == 'g' or user_input == "green":
                print("green")
                result = prompt_stations(ew_stations, "EW")
                if result == '': # back
                    continue
            elif user_input == 'r' or user_input == "red":
                print("red")
                result = prompt_stations(ns_stations, "NS")
                if result == '': # back
                    continue
            else:
                print("Internal Error")
                continue
            prompt_done = True
            print(result)
            print("success")
        else:
            input("Invlid Input. Press enter to continue ...")
            clear_screen()
            continue
        
        return result

def get_station(station: str, line='EW') -> tuple:
    global ew_stations
    global ns_stations

    station_index: int = 0;
    station_line: str = '';
    station_code: str = '';
    station_name: str = '';

    if station.isdigit(): # index number
        # find `station_name` and `station_code`
        station_index = int(station)
        if line.upper() == 'NS':
            station_name = ns_stations[station_index - 1]
            station_code = "NS" + str(station_index)
        elif line.upper() == 'EW': 
            station_name = ew_stations[station_index - 1]
            station_code = "EW" + str(station_index)
        else:
            print("Invalid line keyword argument")
    elif station[:2].isalpha() and station[2:].isdigit(): # for station code
        # find `station_name` and `statin_index`
        station_index = int(station[2:])
        station_line: str = station[:2]
        if station_line == 'EW':
            station_name = ew_stations[station_index-1]
        elif station_line == 'NS':
            station_name = ns_stations[station_index-1]
        else:
            print("error in `station_line`");
    else: # for string
        # find `station_code` and `station_index`
        if station_name in ew_stations:
            station_index = ew_stations.index(station_name)
            station_line = 'EW'
            station_code = station_line + station_index
        elif station_name in ns_stations:
            station_index = ns_stations.index(station_name)
            station_line = 'NS'
            station_code = station_line + station_index

    return (station_index, station_line, station_code, station_name)

def calc_num_hops(start_station: str, end_station: str) -> int: # calculate and returns number of hops between the two stations
    global ew_ns_intchgs
    num_hops: int = 0
    start_station_index: int = int(start_station[2:])
    end_station_index: int = int(end_station[2:])
    possible_hops: list = []

    if start_station[:2] == end_station[:2]: # if the start and destination stations are on the same line
        num_hops = abs(start_station_index - end_station_index)
    else: # on different line
        start_station_name = get_station(start_station)[-1]
        end_station_name = get_station(end_station)[-1]
        
        start_line = 0 if start_station[:2] == 'EW' else 1 # 0 for EW line, 1 for NS line
        for intchg in ew_ns_intchgs_lst:
            x = abs(int(ew_ns_intchgs[intchg][start_line][2:]) - int(start_station[2:]))
            y = abs(int(ew_ns_intchgs[intchg][int(not start_line)][2:]) - int(end_station[2:]))
            possible_hops.append(x+y)
        num_hops = min(possible_hops)
        
    return num_hops

def main():
    clear_screen()
    read_files()

    start_station_code: str = prompt(True) # starting prompt
    end_station_code: str = prompt(False)  # ending prompt

    start_station_index, start_station_line, _, start_station_name = get_station(start_station_code)
    end_station_index, end_station_line, _, end_station_name = get_station(end_station_code)

    print(f"Starting station : {start_station_name}")
    print(f"Ending station : {end_station_name}")
    num_h = calc_num_hops(start_station_code, end_station_code)
    print(f"Num hops : {num_h}")
    distance, duration = calc_distance_mrt(start_station_name, end_station_name)
    print(f"Distance : {distance:.2f}")
    print(f"Duration : {duration:.2f}")

if __name__ == '__main__':
    main()
