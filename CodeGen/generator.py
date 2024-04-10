from datetime import date
from CodeGen import Templates as temp
from CodeGen import SymbolTable as st
import sys

main = False

def genJasmin(ast, outFile, filename):
    # File Setup
    outFile.write(f"; Generated Jasmin File on {date.today()}\n")
    temp.FileSetup(outFile,filename)

    # Go through AST generating code via templates
    print(f"{len(ast)}")
    for item in ast:
        print(f"{item[0][1]}")
        if item[0][0] == "varDef":
            print("Vardef")
        elif item[0][0] == "funcDef":
            if item[0][2] == "main":
                global main
                main = True
            st.addVar(item[0][2], item[0][1], item[0][3][0])
            print(f"{item[0][3][0]}")
    if not main:
        print("ERROR: No main function in program")
        sys.exit()
    else:
        print("[CODE GEN] JVM code successfully generated")