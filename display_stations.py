x = ['Pasir Ris', 'Tampines', 'Simei', 'Tanah Merah', 'Bedok', 'Kembangan', 'Eunos', 'Paya Lebar', 'Aljunied', 'K\
allang', 'Lavender', 'Bugis', 'City Hall', 'Raffles Place', 'Tanjong Pagar', 'Outram Park', 'Tiong Bahru', 'Redhill',\
 'Queenstown', 'Commonwealth', 'Buona Vista', 'Dover', 'Clementi', 'Jurong East', 'Chinese Garden', 'Lakeside', 'Boon\
 Lay', 'Pioneer', 'Joo Koon', 'Gul Circle', 'Tuas Crescent', 'Tuas West Road', 'Tuas Link']

y = ['Jurong East', 'Bukit Batok', 'Bukit Gombak', 'Choa Chu Kang', 'Yew Tee', 'Kranji', 'Marsiling', 'Woodlands'\
, 'Admiralty', 'Sembawang', 'Canberra', 'Yishun', 'Khatib', 'Yio Chu Kang', 'Ang Mo Kio', 'Bishan', 'Braddell', 'Toa \
Payoh', 'Novena', 'Newton', 'Orchard', 'Somerset', 'Dhoby Ghaut', 'City Hall', 'Raffles Place', 'Marina Bay', 'Marina\
 South Pier']


def combine_lines(line_code1: str, line1: list, line_code2: str, line2: list) -> list:
    combined_lines: list = []
    for i in range(len(line1)):
        combined_lines.append(f'[{i+1}] ' + line1[i] + f' ({line_code1}{i+1})')
    for j in range(len(line2)):
        combined_lines.append(f'[{len(line1)+j+1}] ' + line2[j] + f' ({line_code2}{j+1})')
    
    #print(ew_ns_display)
    return combined_lines

def display(combined_lines: list):
    midpoint: int = (len(combined_lines)+1) // 2
    col1: list = combined_lines[:midpoint]
    col2: list = combined_lines[midpoint:]
    
    if len(col2) < len(col1):
        col2.append("")
    
    for left, right in zip(col1,col2):
        print(f"{left:<35} {right}")

if __name__ == '__main__':
    display(combine_lines('EW', x, 'NS', y))

