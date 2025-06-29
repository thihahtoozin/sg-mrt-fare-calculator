from datetime import datetime

def arrival_time_calc(duration: float, format_print: bool): # takes duration in minutes
    now = datetime.now()
    weekday = now.weekday()
    hour = now.hour
    minute = now.minute
    now_in_mins = hour * 60 + minute

    arrival_time = now_in_mins + duration
    if format_print:
        time_now = f"{hour}:{minute % 60:02d}"
        arrival_time = f"{int(arrival_time / 60)}:{int(arrival_time % 60):02d}"

    return (time_now, arrival_time)

if __name__ == '__main__':
    time_now, arrival_time = arrival_time_calc(30, True)
    print(time_now)
    print(arrival_time)
