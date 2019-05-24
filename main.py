from os import listdir, makedirs, rename, path
from os.path import isfile, join
import json
import actions
from functools import reduce

pathIn = '/opt/data/queue/new'
pathProcess = '/opt/data/queue/process'
pathOut = '/opt/data/queue/old'


def checkPath(path):
    try:
        makedirs(path)
    except OSError as e:
        pass


def checkPaths():
    for p in [pathIn, pathProcess, pathOut]:
        checkPath(p)


def listFiles(path):
    files = [f for f in listdir(path) if isfile(join(path, f))]
    return files


def processFile(fileName):
    rename(path.join(pathIn, fileName),
           path.join(pathProcess, fileName))
    print('Process:', fileName)
    res = True
    with open(path.join(pathProcess, fileName), 'r') as f:
        res = reduce(lambda x,y: x and y, [(processMessage(line) != False) for line in f])
        
    if res:
        rename(path.join(pathProcess, fileName),
           path.join(pathOut, fileName))
        print('Done:', fileName)
    else:
        print('Fail:', fileName)


def processFiles(files):
    for fileName in files:
        processFile(fileName)


def getTableAction(table):
    return actions.getAction(table)


def processMessage(text):
    print('Line:', text)
    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        print('Error', e)
        return

    action = getTableAction(data['table'])
    if action != None:
        print('Action', action)
        res = action(data)
        return res is not None

    return


if __name__ == "__main__":
    checkPaths()
    processFiles(listFiles(pathIn))
