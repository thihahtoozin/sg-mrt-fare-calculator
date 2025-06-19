from datetime import datetime

filename = 'config/fare.conf'

def load_prices(filename: str) -> list:
    ranges = [] # list of tuples (float, float, float)
    with open(filename, 'r') as f:
        lines = [ lines.strip() for lines in f.readlines() if lines != "\n" ]
        for line in lines:
            range_part, price = line.split()
            low, high = range_part.split('-')

            # Typecasting
            price = float(price)
            low = float(low) if low != '' else 0
            high = float(high) if high != '' else float('inf')

            ranges.append((low,high,price))
    
    return ranges

def fare_calc(ranges:list, distance: float, discount_percent: float) -> float: # calculate normal fare (without any discount applied)
    for low, high, price in ranges:
        if low <= round(distance,1) <= high:
            return price * (1 - discount_percent)
    return None

def discount_calc() -> float: # take discount conditions (day and time) (do not mutually exclusive)
    discount_percent: float = 0.0
    now = datetime.now()
    weekday = now.weekday() # 0-5 weekdays 5,6 weekends
    hour = now.hour
    minute = now.minute
    time_in_mins = hour * 60 + minute
    # discount on Weekdays 0:5
    if 0 <= weekday < 5:
        if time_in_mins < (7 * 60 + 45):   # early morning before 7:45
            discount_percent += 0.15 # 15%
        elif (9 * 60 + 30) < time_in_mins < (17*60): # morning after peak hour(off-peak hour discount) 9:30 - 17:30
            discount_percent += 0.10 # 10%
        elif time_in_mins > (20 * 60 + 0): # end of the day discount after 20:00
            discount_percent += 0.10 # 10%
        else:
            pass
    else: # no discount on Weekends
        pass

    return discount_percent

if __name__ == '__main__':
    ranges = load_prices(filename)
    distance = float(input("Enter distance : ").strip()) 
    discount_percent = discount_calc()
    print(f"Discount : {discount_percent * 100}%")
    price = fare_calc(ranges, distance, discount_percent)
    print(f"Distance : {distance}")
    print(f"Price : {price}")

