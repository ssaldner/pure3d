import os

BASE = os.path.expanduser("~/github/clariah/pure3d")
dataDir = f"{BASE}/data"
editionDir = f"{dataDir}/editions"

numbers = []
with os.scandir(editionDir) as ed:
    for entry in ed:
        if entry.is_dir():
            name = entry.name
            #print(name)
            if name.isdigit():
                numbers.append(int(name))
                print(numbers)
                    