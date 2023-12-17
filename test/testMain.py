import sys, os, shutil
sys.path.append("..")

import src.Functions as fn

import src.dbOperations as db



if __name__ == "__main__":

    # get the current working directory
    print("## Current PWD = ", os.getcwd())

    folderPath = "tempTestDir"
    if os.path.isdir(folderPath) == False:
        os.mkdir(folderPath)

    folderPath += "/testAppData.db"

    dictSession = {"dbPath" : folderPath}
    # dbOBJ = db.databaseOps(dictSession, "")
    # dbOBJ.connectDB()


    # if os.path.isfile(folderPath) == False:
    #     fn.createDB(folderPath)
    #     dbOBJ.createDB()

    # userName = "Janto"
    # reply = fn.userDetailsInDB(dictSession["dbPath"], userName)
    # print("User details are in DB? : ", reply)

    # dictSession = dbOBJ.getUseridFromDB(userName)
    # print("updated session with new details \n", dictSession)


    userName = "Janto"
    dictSession["name"] = userName
    reply = fn.userDetailsInDB(dictSession["dbPath"], userName)
    print("User details are in DB? : ", reply)

    reply = fn.getUseridFromDB(dictSession, userName)
    print("## User id for newUser should be = ", reply)


    result = fn.addNewUserInDB(dictSession, userName, "cooldude@doda.com", "oreya")
    print("## New user create? : ", result)






    # To test existing app database
    # dbFile = os.getcwd().replace("test","database/appData.db")


    # reply = fn.userDetailsInDB(dbFile, "Oey", "orey@kya.com", "register")
    # print("Value for register reply = ", reply)

    # reply = fn.userDetailsInDB(dbFile, "Orey", "orey@kya.com", "login", "chjore")
    # print("Value for login reply = ", reply)




    # reply = fn.getUseridFromDB(dictSess, "Oey")
    # print("UserId = ", reply)

    # reply = fn.getUseridFromDB(dictSess)
    # print("NewUserID = ", reply)

    # shutil.rmtree(folderPath)



