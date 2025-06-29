
def colorize_line(text: str, line: str):
    colors = {
        'NS': '\033[91m',  # Red
        'EW': '\033[92m',  # Green
        'CC': '\033[93m',  # Yellow
        'DT': '\033[94m',  # Blue
        'NE': '\033[95m',  # Magenta
        'TE': '\033[38;5;94m',  # Brown-ish
        'CG': '\033[90m',  # Grey
        'N/A': '\033[97m', # White
    }
    reset = '\033[0m'
    color = colors.get(line, '\033[97m')  # Default to white
    return f"{color}{text}{reset}"


def annotate_path(path: list, station_lines: dict):
    annotated: str = ''
    for i in range(1, len(path)):
        s1, s2 = path[i - 1], path[i]

        shared = set(station_lines.get(s1, [])) & set(station_lines.get(s2, []))
        line = list(shared)[0] if shared else 'N/A'

        if i == len(path) - 1:
            colored_station = colorize_line(s1, line) + " > " + colorize_line(s2, line) 
        else:
            colored_station = colorize_line(s1, line) 
        if i > 1:
            annotated += " > "
        annotated += colored_station

    return annotated

