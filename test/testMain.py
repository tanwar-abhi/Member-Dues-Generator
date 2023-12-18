import sys, os, shutil
sys.path.append("..")


# import src.Functions as fn
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


    if os.path.isfile(folderPath) == False:
        db.createDB(folderPath)

    userName = "Janto"
    dictSession["name"] = userName


    result = db.addNewUserInDB(dictSession, userName, "cooldude@doda.com", "oreya")
    print("## New user create? : ", result)
    db.printAllData(folderPath)


    print("\n#### Tring to add same user '({})' again".format(userName))
    result = db.addNewUserInDB(dictSession, userName, "cooldude@doda.com", "oreya")
    db.printAllData(folderPath)




    # shutil.rmtree(folderPath)



