def combine_lines(lines: dict) -> list:
    index = 1
    combined_lines: list = []
    for line_code, stations in lines.items():
        for i, station in enumerate(stations):
            combined_lines.append(f"[{index}] {station} {line_code+str(i+1)}")
            index += 1
    #for i in range(len(line1)):
    #    combined_lines.append(f'[{i+1}] ' + line1[i] + f' ({line_code1}{i+1})')
    #for j in range(len(line2)):
    #    combined_lines.append(f'[{len(line1)+j+1}] ' + line2[j] + f' ({line_code2}{j+1})')
    
    print(combined_lines)
    return combined_lines

def display(combined_lines: list):
    midpoint: int = (len(combined_lines)+1) // 2
    print(midpoint)
    col1: list = combined_lines[:midpoint]
    col2: list = combined_lines[midpoint:]
    
    if len(col2) < len(col1):
        col2.append("")
    
    for left, right in zip(col1,col2):
        print(f"{left:<35} {right}")


def prompt(stations_d: dict, c_stations_l: list) -> str: # this function returns tuple of station codes

    # Displaying a list of stations along with station codes
    display(c_stations_l)
    result1 = prompt_question(stations_d, c_stations_l, True)
    result2 = prompt_question(stations_d, c_stations_l, False)
    
    return (result1, result2)

def prompt_question(stations_d: dict, c_stations_l: list, starting: bool = True) -> str: # returns station code
    
    response_code: str = ''
    
    if starting:
        travel_status = "starting"
    else:
        travel_status = "ending"

    user_input = input(f"Enter your {travel_status} station : ").strip()
    c_stations_l = [s.upper() for s in c_stations_l]
    user_input = user_input.upper()
    #print(user_input)

    # User input Validation and Understanding the user input and Returning the correct station code
    if user_input.isdigit(): # for index number
        print("Digit")
        # station name in string
        user_input = c_stations_l[int(user_input) - 1].split()[1:-1] 
        user_input = ' '.join(user_input)
        #print(user_input)

        for line, stations in stations_d.items():
            line = line.upper()
            stations_line = [ l.upper() for l in stations_d[line] ]
            #print(stations_line)
            if user_input in stations_line:
                response_code = f"{line}{stations.index(user_input)+1}"
                break

    elif user_input[:2].isalpha() and user_input[2:].isdigit(): # for station code
        print("Station Code")    
        response_code = user_input

    else: # for string
        print("String")
        for line, stations in stations_d.items():
            line = line.upper()
            stations_line = [ l.upper() for l in stations_d[line] ]
            #print(stations_line)
            if user_input in stations_line:
                response_code = f"{line}{stations.index(user_input)+1}"
                break

    print(response_code)
    return response_code

if __name__ == '__main__':
    stations = {
        'EW': ['Pasir Ris', 'Tampines', 'Simei', 'Tanah Merah', 'Bedok', 'Kembangan', 'Eunos', 'Paya Lebar', 'Aljunied', 'Kallang', 'Lavender', 'Bugis', 'City Hall', 'Raffles Place', 'Tanjong Pagar', 'Outram Park', 'Tiong Bahru', 'Redhill', 'Queenstown', 'Commonwealth', 'Buona Vista', 'Dover', 'Clementi', 'Jurong East', 'Chinese Garden', 'Lakeside', 'Boon Lay', 'Pioneer', 'Joo Koon', 'Gul Circle', 'Tuas Crescent', 'Tuas West Road', 'Tuas Link'],
        'NS': ['Jurong East', 'Bukit Batok', 'Bukit Gombak', 'Choa Chu Kang', 'Yew Tee', 'Kranji', 'Marsiling', 'Woodlands', 'Admiralty', 'Sembawang', 'Canberra', 'Yishun', 'Khatib', 'Yio Chu Kang', 'Ang Mo Kio', 'Bishan', 'Braddell', 'Toa Payoh', 'Novena', 'Newton', 'Orchard', 'Somerset', 'Dhoby Ghaut', 'City Hall', 'Raffles Place', 'Marina Bay', 'Marina South Pier'],
        'CC': ['Dhoby Ghaut', 'Bras Basah', 'Esplanade', 'Promenade', 'Nicoll Highway', 'Stadium', 'Mountbatten', 'Dakota', 'Paya Lebar', 'MacPherson', 'Tai Seng', 'Bartley', 'Serangoon', 'Lorong Chuan', 'Bishan', 'Marymount', 'Caldecott', 'Botanic Gardens', 'Farrer Road', 'Holland Village', 'Buona Vista', 'one-north', 'Kent Ridge', 'Haw Par Villa', 'Pasir Panjang', 'Labrador Park', 'Telok Blangah', 'HarbourFront']
        }

    display(combine_lines(stations))
    #combine_lines(stations)

