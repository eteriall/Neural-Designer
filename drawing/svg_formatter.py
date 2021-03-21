from os import listdir
from os.path import isfile, join

ELEMENTS = [join('elements', f) for f in listdir('elements') if isfile(join('elements', f))]

for fname in ELEMENTS:
    with open(fname) as f:
        data = f.read()
        data = data.replace('fill="none"', 'fill="white" fill-opacity=".0"')

    with open(fname, mode="w") as f:
        f.write(data)
