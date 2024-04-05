from datetime import date
from CodeGen import Templates as temp
from CodeGen import SymbolTable as st

def genJasmin(ast, outFile, filename):
    outFile.write(f"; Generated Jasmin File on {date.today()}\n")
    temp.FileSetup(outFile,filename)
    pass