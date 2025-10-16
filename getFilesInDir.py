from os import listdir

def getFilesInDir(mypath):
    f = []
    f = ['\\'.join([mypath,file]) for file in listdir(mypath)]
    if len(f):
        return f
    else:
        raise FileNotFoundError(f"Failed to find font files in directory {mypath}")

