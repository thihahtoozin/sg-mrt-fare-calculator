import os

ew_file: str = "EW.txt"
ns_file: str = "NS.txt"

ew_stations: list = [] # Green Line EW33 to EW1
ns_stations: list = [] # Red Line   NS1  to NS28

def read_file():
    global ew_stations
    global ns_stations
    # reading the stations and assigning them into each related list
    with open(ew_file, "r") as ew_f:
        ew_stations = [f.strip() for f in ew_f.readlines() if f != '\n']
    with open(ns_file, "r") as ns_f:
        ns_stations = [f.strip() for f in ns_f.readlines() if f != '\n']

def prompt_stations(stations: list, line: str = "EW") -> int:
    result: int = 0
    for station_i in range(len(stations)):
        print(f"[{line}{station_i + 1}]:{stations[station_i]}")
    stations = [s.lower() for s in stations]
    user_input = input("Enter station name or number to choose('b' for back) : ").strip()
    user_input = user_input.lower()
    print(user_input)
    
    if user_input.isdigit(): # for index number
        print("Digit")
        result: int = int(user_input)
    elif user_input[:2].isalpha() and user_input[2:].isdigit(): # for station code
        print("Station Code")    
        result: int = int(user_input[2:])
    elif user_input == 'b' or user_input == 'back':
        pass
    else: # for string
        print("String")
        result: int = stations.index(user_input.lower()) + 1

    os.system('cls')
    return result

def prompt():
    global ew_stations
    global ns_stations
    
    print("Please select one of the following starting stations")
    prompt_done: bool = True
    while prompt_done:
        user_input = input("Is your Starting Stations Green line or Red line(g/r) : ").strip()
        user_input = user_input.lower()
        if user_input in ['g', 'r', "green", "red"]:
            if user_input == 'g' or user_input == "green":
                print("green")
                result = prompt_stations(ew_stations, "EW")
                if result == 0: # back
                    continue
            elif user_input == 'r' or user_input == "red":
                print("red")
                result = prompt_stations(ns_stations, "NS")
                if result == 0: # back
                    continue
            else:
                print("Internal Error")
                continue
            prompt_done = False
            print(result)
            print("success")
        else:
            input("Invlid Input. Press enter to continue ...")
            os.system("cls")
            continue

def main():
    os.system('cls')
    read_file()
    prompt()

if __name__ == '__main__':
    main()