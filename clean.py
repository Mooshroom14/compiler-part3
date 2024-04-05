import os
import shutil

def main():
    shutil.rmtree("./Test")
    os.mkdir("./Test")

if __name__ == "__main__":
    main()