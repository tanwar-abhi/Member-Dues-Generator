import sys, os
sys.path.append("..")


import src.Functions as fn



if __name__ == "__main__":
    # get the current working directory
    print("## Current PWD = ", os.getcwd())

    dbFile = os.getcwd().replace("test","database/appData.db")
    print("## DBfile path = ", dbFile)


    reply = fn.userDetailsNotInDB(dbFile, "Orey", "orey@kya.com")
    print("Value in reply = ", reply)

    print("Main test file")


