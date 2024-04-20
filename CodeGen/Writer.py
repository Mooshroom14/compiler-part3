from CodeGen import SymbolTable as st

file = ""
filename = ""
def FileSetup(outFile, fileIn):
    global filename
    global file
    filename = fileIn
    file = outFile

    writeMeta()

def writeMeta():
    global file
    global filename
    file.write(f".source {filename}\n")
    file.write(f".")

def writeIf(condtion, hasElse, statements):
    pass

def writeWhile(condition, statments):
    pass

def writeMethod(name, type, statements):
    file.write(f".method {name}(){type}")