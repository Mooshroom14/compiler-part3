from CodeGen import SymbolTable as st

file = ""
filename = ""
def FileSetup(outFile, fileIn):
    global filename
    global file
    filename = fileIn
    file = outFile

    genMeta()

def genMeta():
    global file
    global filename
    file.write(f".source {filename}\n")

def genVarDef():
    pass

def genFuncDef():
    pass