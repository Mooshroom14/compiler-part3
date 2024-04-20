from datetime import date
from CodeGen import Writer as writer
from CodeGen import SymbolTable as st
import sys

main = False
expressList = []
stateList = []
messageOn = True

def genJasmin(ast, outFile, filename, debug):
    global messageOn
    # File Setup
    outFile.write(f"; Generated Jasmin File on {date.today()}\n")
    writer.FileSetup(outFile,filename)

    # Go through AST generating code via templates
    if debug == 3 or debug == 0:
        messageOn = True
    #print(f"{len(ast)}")
    for item in ast:
        #print(f"{item[0][1]}")
        if item[0][0] == "varDef":
            genVarDef(item[0])
        elif item[0][0] == "funcDef":
            genFuncDef(item)
    if not main:
        print("ERROR: No main function in program")
        sys.exit()
    else:
        if messageOn:
            print("[CODE GEN] JVM code successfully generated")

def genVarDef(varTree):
    st.addVar(varTree[2], varTree[1], None)

def genFuncDef(funcTree):
    if funcTree[0][2] == "main":
        global main
        main = True
    st.addVar(funcTree[0][2], funcTree[0][1], ['proc', len(funcTree[0][3][0])])
    st.incScope()
    for x in funcTree[0][3][0]:
        st.addVar(x[1], x[0], None)
    print(f"Number of Statements in function: {len(funcTree[0][3][1])}")
    for statement in funcTree[0][3][1]:
        genStatement(statement)
    st.decScope()
    #print(f"{funcTree[0][3][0]}")

def genStatement(stateTree):
    global expressList
    global stateList
    statement = stateTree[0]
    match(statement):
        case "ifState()":
            print("Found if state!")
            hasElse = False
            #print(f"{stateTree[1][0]}")
            genExpression(stateTree[1][0])
            print(expressList)
            expressList = []
            genStatement(stateTree[1][1])
            if stateTree[1][2] != None:
                print("Has an else")
                hasElse = True
                genStatement(stateTree[1][2])
            writer.writeIf(expressList, hasElse, stateList)
        case "breakState()":
            pass
        case "newLineState()":
            print("Found newline state!")
        case "nullState()":
            pass
        case "blockState()":
            st.incScope()
            for item in stateTree[1]:
                genStatement(item)
            st.decScope()
        case "returnState()":
            print("Found return state!")
        case "whileState()":
            st.incScope()
            print("Found while state!")
            genExpression(stateTree[1][0])
            print(expressList)
            expressList = []
            #print(stateTree[1][1])
            genStatement(stateTree[1][1])
            st.decScope()
        case "writeState()":
            print("Found write state!")
        case "readState()":
            print("Found read state!")
        case "exprState()":
            print("Found expression state!")
            genExpression(stateTree[1])
            print(expressList)
            if len(expressList[0]) == 2:
                if expressList[0][0] == "ID":
                    st.checkForVar(expressList[0][1])
            expressList = []
        case "varDef":
            genVarDef(stateTree)
    #print(stateTree)

def genExpression(exprTree):
    global messageOn
    global expressList
    if exprTree[0] == "expr()":
        #print(len(exprTree[1]))
        if len(exprTree[1]) == 3:
            for item in exprTree[1]:
                genExpression(item)
        else:
           genExpression(exprTree[1])
    elif exprTree[0] == "ID":
        if not st.checkForVar(exprTree[1]):
            print(f"ID {exprTree[1]} not found!")
            sys.exit()
        else:
            expressList.append([exprTree[0], exprTree[1]])
            if messageOn:
                print("[CODE GEN] Found var!")
    elif exprTree[0] == "Number":
        expressList.append(exprTree[1])
        if messageOn:
            print("[CODE GEN] Found a Number!")
    elif exprTree[0] == "Operator":
        expressList.append(exprTree[1])
        if messageOn:
            print("[CODE GEN] Found an Operator!")
    else:
        genExpression(exprTree[0])

    #print(expressList)
    return expressList
