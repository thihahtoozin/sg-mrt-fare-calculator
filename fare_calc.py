#import datetime

def load_prices(filename: str):
    with open(filename, 'r') as f:
        lines = [ lines.strip() for lines in f.readlines() if lines != "\n" ]
        print(lines)
        for line in lines:
            print(line)

def fare_calc(distance: float) -> float: # calculate normal fare (without any discount applied)
   return cent

def discount_calc(): # take discount conditions (day and time) (do not mutually exclusive)
    pass


if __name__ == '__main__':
    filename = 'config/fare.conf'
    load_prices(filename)


'''
config/lines
'''
'''
config/fare.conf

[range(kg)] [fare($)]
-0.32       0.52
3.3-4.2     0.57
4.3-5.2     0.63
5.3-6.2     0.68
6.3-7.2     0.71
7.2-        0.74
'''

'''
separate file for api key
Include how to add api key on README.md
'''


'''
features show routes and stations in order 
'''
