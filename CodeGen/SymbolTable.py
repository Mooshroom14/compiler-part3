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
    if not checkForVar(name):
        if not type == "int":
            print(f"ERROR: Variable type is not \"int\"!")
            sys.exit()
        table.insert(0, [name, type, attr, scope])
        print(f"[CODE GEN] Var {name} added to symbol table!")
    else: 
        print(f"ERROR: Variable {name} already exists!")
        sys.exit()

def checkForVar(var):  
    global table
    inTable = False
    for item in table:
        if item[0] == var:
            inTable = True
    return True if inTable else False

def printSymTable():
    global table
    for item in table:
        for x in item:
            print(f"{x} ", end="")
        print("\n")
