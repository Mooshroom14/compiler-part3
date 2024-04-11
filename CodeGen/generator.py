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
            genFuncDef(item)
    if not main:
        print("ERROR: No main function in program")
        sys.exit()
    else:
        print("[CODE GEN] JVM code successfully generated")

def genVarDef(varTree):
    pass

def genFuncDef(funcTree):
    if funcTree[0][2] == "main":
        global main
        main = True
    st.addVar(funcTree[0][2], funcTree[0][1], ['proc', len(funcTree[0][3][0])])
    st.incScope()
    for x in funcTree[0][3][0]:
        st.addVar(x[1], x[0], None)
    st.decScope()
    print(f"{funcTree[0][3][0]}")