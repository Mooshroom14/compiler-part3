import sys
from enum import Enum

scope = 0
scopeLevel = 0
table = []

class attrType(Enum):
    var = 0
    proc = 1

def decScope():
    global scope
    scope -= 1

def incScope():
    global scope
    scope += 1

def addVar(name, type, attr):
    global scope
    checkForVar(name)
    table.insert(0, [name, type, attr, scope])

def checkForVar(var):  
    global table
    inTable = False
    for item in table:
        if item[0] == var:
            inTable = True
    if inTable:
        print(f"Variable {var} already exists!")
        sys.exit()

def printSymTable():
    global table
    for item in table:
        print("\n")
        for x in item:
            print(f"{x} ", end="")
