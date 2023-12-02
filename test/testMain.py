import sys, os, shutil
sys.path.append("..")


import src.Functions as fn



if __name__ == "__main__":
    # get the current working directory
    print("## Current PWD = ", os.getcwd())

    folderPath = "tempTestDir"
    os.mkdir(folderPath)

    folderPath += "/testAppData.db"
    fn.createDB(folderPath)

    dbFile = os.getcwd().replace("test","database/appData.db")

    # dbFile = os.getcwd()
    # dbFile += folderPath
    print("## DBfile path = ", dbFile)


    reply = fn.userDetailsInDB(dbFile, "Oey", "orey@kya.com", "register")
    print("Value for register reply = ", reply)

    reply = fn.userDetailsInDB(dbFile, "Orey", "orey@kya.com", "login", "chjore")
    print("Value for login reply = ", reply)

    shutil.rmtree(folderPath)



