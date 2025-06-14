import os

ew_file: str = "EW.txt"
ns_file: str = "NS.txt"

ew_stations: list = [] # Green Line EW33 to EW1
ns_stations: list = [] # Red Line   NS1  to NS28
ew_ns_intchgs_lst: list = [] # list of interchanges across EW and NS lines
ew_ns_intchgs: dict = {} # record of interchanges across EW and NS lines

# clearing screen by detecting underlying operating system
def clear_screen() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')

def read_file() -> None: # read files and fill up our lists (ew_stations, ns_stations, ew_ns_intchgs)

    # declaring global variables to avoid creating local variables with the same name
    global ew_stations
    global ns_stations
    global ew_ns_intchgs_lst
    global ew_ns_intchgs

    # reading the stations and assigning them into `ew_stations`
    with open(ew_file, "r") as ew_f:
        ew_stations = [f.strip() for f in ew_f.readlines() if f != '\n']

    # reading the stations and assigning them into `ns_stations`
    with open(ns_file, "r") as ns_f:
        ns_stations = [f.strip() for f in ns_f.readlines() if f != '\n']

    # find interchanges between two lines
    ew_ns_intchgs_lst = list(set(ns_stations) & set(ew_stations))
    print(ew_ns_intchgs_lst)
    for station in ew_ns_intchgs_lst:
        ew_index = ew_stations.index(station)+1
        ns_index = ns_stations.index(station)+1
        ew_code = f"EW{ew_index}"
        ns_code = f"NS{ns_index}"
        ew_ns_intchgs[station] = (ew_code, ns_code)
    print(ew_ns_intchgs)

def prompt_stations(stations: list, line: str = "EW") -> str: # this function returns station code as a string

    # initializing the return value as empty string
    result: str = ''

    # Displaying a list of stations along with station codes
    for station_i in range(len(stations)):
        print(f"[{line}{station_i + 1}]:{stations[station_i]}")

    # getting user input and validating
    stations = [s.lower() for s in stations]
    user_input = input("Enter station name or number to choose('b' for back) : ").strip()
    user_input = user_input.lower()
    print(user_input)
    
    if user_input.isdigit(): # for index number
        print("Digit")
        result = line + user_input
    elif user_input[:2].isalpha() and user_input[2:].isdigit(): # for station code
        print("Station Code")    
        result = user_input[2:]
    elif user_input == 'b' or user_input == 'back':
        pass # letting the return value remain zero(0).
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
    interchange: bool = False;

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

def main():
    clear_screen()
    read_file()

    start_station_code: str = prompt(True) # starting prompt
    end_station_code: str = prompt(False)  # ending prompt

    start_station_index, start_station_line, _, start_station_name = get_station(start_station_code)
    end_station_index, end_station_line, _, end_station_name = get_station(end_station_code)

    print(f"Starting station : {start_station_name}")
    print(f"Ending station : {end_station_name}")

if __name__ == '__main__':
    main()
