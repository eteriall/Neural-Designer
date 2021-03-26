from os import listdir
from os.path import isfile, join

ELEMENTS = [join('../resources/elements', f) for f in listdir('../resources/elements') if isfile(join(
    '../resources/elements', f))]

for fname in ELEMENTS:
    with open(fname) as f:
        data = f.read()
        data = data.replace('fill="none"', 'fill="white" fill-opacity=".0"')

    with open(fname, mode="w") as f:
        f.write(data)
