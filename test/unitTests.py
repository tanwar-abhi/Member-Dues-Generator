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

    userName = ["Kakashi", "Naruto" ]
    userEmailID = ["copyNinja@konoha.com", "datebayo@konoha.com"]
    userPWD = ["whiteFang", "futureHokage"]
    dictSession["name"] = userName[0]


    userID, usrType, result = db.addNewUserInDB(dictSession["dbPath"], userName[0], userEmailID[0], userPWD[0])
    dictSession["userID"] = userID
    dictSession["userType"] = usrType
    print("## New user create? : ", result)

    # try:
    #     result = db.addNewUserInDB(dictSession, userName, "cooldude@doda.com", "oreya")
    #     print("## New user create? : ", result)
    # except Exception as err:
    #     print(err)
    # else:
    #     db.printAllData(folderPath)

    db.printAllData(folderPath)
    print("## session = ", dictSession)

    userID,_,_ = db.getUseridFromDB(dictSession["dbPath"], userName[1], userEmailID[1])
    print("For nnewUser {} , UserId = {}".format(userName[1], userID))
    print("\n## session = ", dictSession)

    userID, usrType, result = db.addNewUserInDB(dictSession["dbPath"], userName[1], userEmailID[1], userPWD[1])
    print("\n## New User added\n")
    print("\n All data in DB after adding new user = {}".format(userName[1]))
    db.printAllData(dictSession["dbPath"])


    print("\n#### Tring to add same user '({})' again".format(userName[0]))
    result = db.addNewUserInDB(dictSession["dbPath"], userName[0], userEmailID[0], userPWD[0])
    db.printAllData(folderPath)


    # shutil.rmtree(folderPath)



