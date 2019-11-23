import os
from os import listdir
from os.path import isfile, join
from PIL import Image
from sklearn.model_selection import train_test_split

def main(main, subs):
    avg_width = 0
    avg_height = 0
    no = 0

    filenames = {}
    for sub in subs:
        path = main+sub
        data = [f for f in listdir(path) if isfile(join(path, f))]
        data = [f for f in data if f.endswith('.jpg') or f.endswith('.png')or f.endswith('.jpeg')]
        no += len(data)
        filenames[sub] = data

    for i in filenames.keys():
        data = filenames[i]
        for filename in data:
            im = Image.open(main+i+filename)
            width, height = im.size
            avg_width += width
            avg_height += height
    impt = (round(avg_width/no), round(avg_height/no))
    print(impt)
    #resizing operations
    for i in filenames.keys():
        data = filenames[i]
        train, test = train_test_split(data,test_size=0.2, random_state=42)
        for x in train:
            im = Image.open(main+i+x)
            width, height = im.size
            im = im.resize(impt)
            newpath = "data/train/"+ i + x
            if not os.path.exists(os.path.dirname(newpath)):
                try:
                    os.makedirs(os.path.dirname(newpath))
                except OSError as exc: # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise
            im = im.convert("RGB")
            im.save(newpath)

        for y in test:
            im = Image.open(main+i+y)
            width, height = im.size
            im = im.resize(impt)
            newpath = "data/test/" + i + y
            if not os.path.exists(os.path.dirname(newpath)):
                try:
                    os.makedirs(os.path.dirname(newpath))
                except OSError as exc: # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise
            im = im.convert("RGB")
            im.save(newpath)

if __name__ == '__main__':
    main('healine/', ['firstdegburn/', 'minorcut/', 'contusion/', 'snakebite/', 'nosebleed/'])
