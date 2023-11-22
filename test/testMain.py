import sys, os
sys.path.append("..")


import src.Functions as fn



if __name__ == "__main__":
    # get the current working directory
    print("## Current PWD = ", os.getcwd())

    dbFile = os.getcwd().replace("test","database/appData.db")
    print("## DBfile path = ", dbFile)


    reply = fn.userDetailsInDB(dbFile, "Oey", "orey@kya.com", "register")
    print("Value in register reply = ", reply)

    reply = fn.userDetailsInDB(dbFile, "Orey", "orey@kya.com", "login", "chjore")
    print("Value in login reply = ", reply)



