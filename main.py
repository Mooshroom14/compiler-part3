import argparse 
from FileParser import productions
from AbstractSyntax import Trees
from CodeGen import generator as gen
from CodeGen.SymbolTable import printSymTable

def printHelp():
    print("Usage: python3 [classpath] parser.tc [options] toyc_source_file")
    print("\nwhere options include: ")
    print("\t-help             display this usage message")
    print("\t-output <file>    specifies target file name")
    #print("\t-class  <file>    specifies class file name")
    print("\t-debug <level>    display messages that aid in tracing the compilation process.")
    print("\t\t\t  If level is: ")
    print("\t\t\t      0 - all messages")
    print("\t\t\t      1 - scanner messages only")
    print("\t\t\t      2 - parser messages only")
    print("\t\t\t      3 - code generation messages only")
    print("\t-abstract         dump the abstract syntax tree")
    print("\t-symbol           dump the symbol table(s)")
    print("\t-code             dump the generated program")
    print("\t-verbose          display all information\n")
    print("\t-version          display the program version")

def main():
    # Parser Setup
    parser = argparse.ArgumentParser()
    #group = parser.add_mutually_exclusive_group()
    parser.add_argument("-debug", type=int, choices=[0,1,2,3],
                    help="increase output verbosity")
    parser.add_argument("-verbose", action="store_true",
                    help="displays all information")
    parser.add_argument("-help", action="store_true", help="shows usage information")
    parser.add_argument("filename", help = "file to be compiled")
    parser.add_argument("-output", type=str, help = "output filename")
    parser.add_argument("-abstract", action="store_true", help="dump the abstract syntax tree")
    parser.add_argument("-symbol", action="store_true", help="dump the symbol table(s)")
    parser.add_argument("-code", action="store_true", help="dump generated program")
    parser.add_argument("-version", action="store_true", help="display the program version")

    args = parser.parse_args()
    outFile = args.output

    print("part3: Nathan Germain")

    if args.version:
        print("Program Version: v1")

    if args.help:
        printHelp()
    else:
        codeFile = open(args.filename, "r")  

        if args.verbose:
            args.abstract = True
            args.debug = 0

        productions.setup(codeFile, args.debug)
        astProgram = productions.Program()
        if args.abstract:
            Trees.printAST(astProgram, args.filename)

        codeFile.close()

        if args.verbose:
            with open(args.filename, 'r') as file:
                lines = file.readlines()
            for line in lines:
                print(line.strip("\n"))  

        
        if outFile:
            print("file overridden")
            filename = f"Test/{args.output}.j"
        else:
            filename = (args.filename.removesuffix('.tc')) + ".j"

        outFile = open(f"{filename}", 'w')
        gen.genJasmin(astProgram, outFile, filename, args.debug)
        outFile.close()

        if args.code:
            print("\nOutput Code File ------------------------------")
            with open(filename, 'r') as file:
                lines = file.readlines()
            for line in lines:
                print(line.strip("\n"))

        if args.symbol:
            print("\nSymbol Table ----------------------------------")
            print("\n---Name -- Type -- Args/Var -- Scope-----------")
            printSymTable()

            

if __name__ == "__main__":
    main()

"""
    TODO Symbol Table generator
    TODO Templates
    TODO Combine

"""