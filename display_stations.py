import os

# clearing screen by detecting underlying operating system
def clear_screen() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')

def combine_lines(mrt_struct: dict) -> list:
    index = 1
    combined_lines: list = []
    for line_code, line_struct in mrt_struct.items():
        for i, station in enumerate(line_struct['path']):
            combined_lines.append(f"[{index}] {station} {line_code+str(i+line_struct['start_index'])}")
            index += 1
    
    return combined_lines

def display(combined_lines: list):
    midpoint: int = (len(combined_lines)+1) // 2
    #print(midpoint)
    col1: list = combined_lines[:midpoint]
    col2: list = combined_lines[midpoint:]
    
    if len(col2) < len(col1):
        col2.append("")
    
    for left, right in zip(col1,col2):
        print(f"{left:<35} {right}")


def prompt(stations_d: dict, c_stations_l: list) -> str: # this function returns tuple of station codes

    while True:
        clear_screen()
        display(c_stations_l)            # Displaying a list of stations along with station codes
        start = prompt_question(stations_d, c_stations_l, True)
        end = prompt_question(stations_d, c_stations_l, False)
        if start != '-1' and end != '-1':
            break 
    return (start, end)

def prompt_question(mrt_struct: dict, c_stations_l: list, starting: bool = True) -> str: # returns station code
    
    response_code: str = ''
    
    if starting:
        travel_status = "starting"
    else:
        travel_status = "ending"

    user_input = input(f"Enter your {travel_status} station : ").strip()
    c_stations_l = [s.upper() for s in c_stations_l]
    user_input = user_input.upper()
    #print(user_input)

    # Understanding the user input and Returning the correct station code
    if user_input.isdigit(): # for index number
        try:
            user_input = c_stations_l[int(user_input) - 1].split()[1:-1] 
            user_input = ' '.join(user_input)
            #print(user_input) # station name in string

            for line, line_struct in mrt_struct.items():
                path = [ s.upper() for s in line_struct['path'] ]
                #print(path)
                if user_input in path:
                    start_index = line_struct['start_index']
                    response_code = f"{line}{path.index(user_input)+start_index}"
        except:
            return '-1'

    elif user_input[:2].isalpha() and user_input[2:].isdigit(): # for station code
        for line_struct in mrt_struct.values():
            if user_input in line_struct['codes']:
                response_code = user_input
                return response_code
        return '-1'

    else: # for string
        user_input = " ".join(user_input.split())  # formatting string for extra spaces 
        for line, line_struct in mrt_struct.items():
            path = [ s.upper() for s in line_struct['path'] ]
            #print(path)
            if user_input in path:
                response_code = f"{line}{path.index(user_input)+line_struct['start_index']}"
                return response_code
        return '-1'

    #print(response_code)
    return response_code # response code for error is '-1'

if __name__ == '__main__':
    stations = {
            'EW': {
                'start_index': 1, 
                'path': ['Pasir Ris', 'Tampines', 'Simei', 'Tanah Merah', 'Bedok', 'Kembangan', 'Eunos', 'Paya Lebar', 'Aljunied', 'Kallang', 'Lavender', 'Bugis', 'City Hall', 'Raffles Place', 'Tanjong Pagar', 'Outram Park', 'Tiong Bahru', 'Redhill', 'Queenstown', 'Commonwealth', 'Buona Vista', 'Dover', 'Clementi', 'Jurong East', 'Chinese Garden', 'Lakeside', 'Boon Lay', 'Pioneer', 'Joo Koon', 'Gul Circle', 'Tuas Crescent', 'Tuas West Road', 'Tuas Link']
                   },
            'NS': {
                'start_index': 1,
                'path' : ['Jurong East', 'Bukit Batok', 'Bukit Gombak', 'Choa Chu Kang', 'Yew Tee', 'Kranji', 'Marsiling', 'Woodlands', 'Admiralty', 'Sembawang', 'Canberra', 'Yishun', 'Khatib', 'Yio Chu Kang', 'Ang Mo Kio', 'Bishan', 'Braddell', 'Toa Payoh', 'Novena', 'Newton', 'Orchard', 'Somerset', 'Dhoby Ghaut', 'City Hall', 'Raffles Place', 'Marina Bay', 'Marina South Pier']
                },
            'CC': {
                'start_index': 1,
                'path' : ['Dhoby Ghaut', 'Bras Basah', 'Esplanade', 'Promenade', 'Nicoll Highway', 'Stadium', 'Mountbatten', 'Dakota', 'Paya Lebar', 'MacPherson', 'Tai Seng', 'Bartley', 'Serangoon', 'Lorong Chuan', 'Bishan', 'Marymount', 'Caldecott', 'Botanic Gardens', 'Farrer Road', 'Holland Village', 'Buona Vista', 'one-north', 'Kent Ridge', 'Haw Par Villa', 'Pasir Panjang', 'Labrador Park', 'Telok Blangah', 'HarbourFront']
                }
        }

    start_index = {
            'EW': 1,
            'NS': 1,
            'CG': 0
        }

    display(combine_lines(stations, start_index))
    #combine_lines(stations)

