import os

BASE = os.path.expanduser("~/github/clariah/pure3d")
dataDir = f"{BASE}/data"
editionDir = f"{dataDir}/editions"


def editionsList():  # to get enumeration of top level directories
    numbers = []
    with os.scandir(editionDir) as ed:
        for entry in ed:
            if entry.is_dir():
                name = entry.name
                if name.isdigit():
                    numbers.append(int(name))
    return sorted(numbers)


editionNumbers = editionsList()

for i in editionNumbers:
    modelDir = f"{editionDir}/{i}/3d"
    #print(modelDir)  #/home/sohinim/github/clariah/pure3d/data/editions/1/3d
    
    for dir in os.listdir(modelDir):
        if os.path.isdir(modelDir):
            print(dir)
            #print('Directory Name: ', modelDir)
            #print('File List: ', dir)
            