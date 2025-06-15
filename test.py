import os

files = os.listdir('config/')[:2]
files = [ f.split('.')[0] for f in files ]

print(files)

