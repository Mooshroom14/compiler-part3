from CodeGen import SymbolTable as st
from CodeGen import generator as gen
import sys

file = ""
filename = ""
varCount = 0
localVals = []
labelCt = 0

def writeLoad(var):
    varNum = grabLocalVal(var)
    file.write(f"   iload_{varNum}\n")

def grabLocalVal(var):
    for item in localVals:
        if var == item[0]:
            return item[1]
        else:
            return None

def FileSetup(outFile, fileIn):
    global filename
    global file
    filename = fileIn
    file = outFile

    writeMeta()
    writeClass()
    writeMain()

def writeMeta():
    global file
    global filename
    file.write(f".source {filename}\n")
    filename = filename.removeprefix("Test/")
    filename = filename.removesuffix(".j")
    file.write(f".class public {filename}\n")
    file.write(f".super java/lang/Object\n\n")

def writeClass():
    file.write(f".method public <init>()V\n")
    file.write(f"   .limit stack 1\n")
    file.write(f"   .limit locals 1\n")
    file.write(f"   aload_0\n")
    file.write(f"   invokespecial java/lang/Object/<init>()V\n")
    file.write(f"   return\n")
    file.write(f".end method\n\n")

def writeMain():
    file.write(f".method public static main([Ljava/lang/String;)V\n")
    file.write(f"   .limit stack 100\n")
    file.write(f"   .limit locals 100\n")
    #file.write(f"   invokestatic {filename}/main1()I\n")
    #file.write(f".end method\n\n")

def writeIf(condition, hasElse, statements):
    #print(len(statements))
    condOps = ["==","<","<=",">=",">","||","&&","!="]
    #print(condition)
    file.write(f"; If Statement\n")
    if condition[1] in condOps:
        #print("Condition is relational!")
        if type(condition[0]) is list:
            #print("Expression 1")
            writeExpression(condition[0][0],condition[0][2],condition[0][1])
        else:
            file.write(f"   ldc {condition[0]}\n")

        if type(condition[2]) is list:
            #print("Expression 2")
            writeExpression(condition[0][0],condition[0][2],condition[0][1])
        else:
            file.write(f"   ldc {condition[2]}\n")

        writeExpression(None, None, condition[1])
        file.write(f"   ifeq label_True\n")
        file.write(f"   goto label_Else\n")
        file.write(f"label_True:\n")
        #print(statements[0])
        gen.genStatement(statements[0])
        file.write(f"label_Else:\n")
        #print(statements[1])
        if hasElse:
            #print("Has else")
            gen.genStatement(statements[1])

    else:
        print("NO")

    

def writeWhile(condition, statements):
    global labelCt
    file.write(f"; While Loop\n")
    if len(condition) == 3:
        file.write(f"label_While:\n")
        writeExpression(condition[0], condition[2], condition[1])
        file.write("   ifne label_endWhile\n")
        gen.genStatement(statements)

    file.write(f"   goto label_While\n")
    file.write(f"label_endWhile:\n")

def writeVarAssignment(var, value):
    global varCount
    global localVals
    if type(value) is list and len(value) == 3:
        writeExpression(value[0],value[2],value[1])
    else:
        file.write(f"   ldc {value}\n")
    if grabLocalVal(var) != None:
        file.write(f"   istore_{grabLocalVal(var)}\n")
    else:
        file.write(f"   istore_{varCount}\n")
        localVals.append([var, varCount])
        varCount += 1

#def writeBeginMethod(name, type):
    #t = ""
    #if type == "int":
    #    t = "I"
    #else:
    #    print("ERROR: Illegal Type! Ints only!")
    #    sys.exit()
    #file.write(f".method {name}1(){t}\n")
    #file.write("   .limit stack 100\n")
    #file.write("   .limit locals 100\n")

def writeEndMethod():
    file.write(".end method\n")

def writeReturn():
    file.write(f"; Return\n")
    file.write(f"   iconst_0\n")
    file.write(f"   ireturn\n")

def writeNewLine():
    file.write(f"; Newline\n")
    file.write(f"   getstatic java/lang/System/out Ljava/io/PrintStream;\n")
    file.write(f"   ldc \"\\n\"\n")
    file.write(f"   invokevirtual java/io/PrintStream/print(Ljava/lang/String;)V\n")

def writeExpression(num1, num2, op):
    if op == "=":
        if num2 is list:
            writeExpression(num2[0],num2[2],num2[1])
        else:
            writeVarAssignment(num1,num2)
    elif num1 != None and len(num1) == 3:
        writeExpression(num1[0],num1[2],num1[2])            
    else:
        if type(num1) is list:
            if num1[0] == "ID":
                writeLoad(num1)
            else:
                print("Writing sub expression")
                writeExpression(num1[0],num1[2],num1[1])
        elif num1 != None:
            file.write(f"   ldc {num1}\n")

        if type(num2) is list:
            if num2[0] == "ID":
                writeLoad(num2)
            else:
                print("Writing sub expression")
                writeExpression(num2[0],num2[2],num2[1])
        elif num2 != None:
            file.write(f"   ldc {num2}\n")
        
        match(op):
            case "%":
                file.write(f"   irem\n")
            case "+":
                file.write(f"   iadd\n")
            case "-":
                file.write(f"   isub\n")
            case "/":
                if num2 == 0:
                    print("ERROR: Dividing by 0 is undefined!")
                    sys.exit()
                else:
                    file.write(f"   idiv\n")
            case "*":
                file.write(f"   imul\n")
            case "||":
                file.write(f"   ior\n")
            case "&&":
                file.write(f"   iand\n")
            case "<=":
                writeComp("if_icmple")
            case "<":
                writeComp("if_icmplt")
            case ">=":
                writeComp("if_icmpge")
            case ">":
                writeComp("if_icmpgt")
            case "!=":
                writeComp("if_icmpne")
            case "==":
                writeComp("if_icmpeq")

def writeComp(oper):
    global labelCt
    file.write(f"   {oper} label_{labelCt}\n")
    file.write(f"   iconst_1\n")
    file.write(f"   goto label_{labelCt + 1}\n")
    file.write(f"label_{labelCt}:\n")
    file.write(f"   iconst_0\n")
    file.write(f"label_{labelCt+1}:\n")
    labelCt += 2

def writeWrite(expr):
    global localVals
    file.write(f"   getstatic java/lang/System/out Ljava/io/PrintStream;\n")
    expr = gen.genExpression(expr)
    if type(expr) is list and expr[0] == "ID":
        st.checkForVar(expr[1])
        item = grabLocalVal(expr)
        if item != None:
            file.write(f"   iload_{item}\n")
    else:
        file.write(f"   ldc {expr}\n")
    file.write(f"   invokevirtual java/io/PrintStream/print(Ljava/lang/String;)V\n")

def writeRead(expr):
    global varCount
    global localVals
    file.write(f"; Read\n")
    file.write(f"   new java/util/Scanner\n")
    file.write(f"   dup\n")
    file.write(f"   getstatic java/lang/System/in Ljava/io/InputStream;\n")
    file.write(f"   invokespecial java/util/Scanner/<init>(Ljava/io/InputStream;)V\n")
    file.write(f"   astore_{varCount}\n")
    scannerStore = varCount
    varCount += 1
    #print(expr)
    for item in expr:
        file.write(f"   aload_{scannerStore}\n")
        file.write(f"   invokevirtual java/util/Scanner/nextInt()I\n")
        file.write(f"   istore_{varCount}\n")
        localVals.append([item[1], varCount])
        varCount += 1
        