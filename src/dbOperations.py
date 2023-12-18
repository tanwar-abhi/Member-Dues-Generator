
# SQlite3 for executing SQL queries on database.
import sqlite3


# class databaseOps():

#     def __init__(self, webSession, connection):
#         self.webSession = webSession
#         self.connection = connection


#     def connectDB(self):
#         self.connection = sqlite3.connect(self.webSession["dbPath"])
#         return
    
#     def disconnectDB(self):
#         self.connection.close
#         return



#     def createDB(self):
#         # conn = sqlite3.connect(self.webSession["dbPath"])
#         txn = self.connection.cursor()
#         txn.execute('''CREATE TABLE appUsers (userid INT PRIMARY KEY NOT NULL,
#                     name TEXT NOT NULL,
#                     email TEXT NOT NULL,
#                     password TEXT NOT NULL); ''' )
#         print("## New Database created ##")
#         print("Database Name = database/appData.db")
#         print("Table Name = appData.appUsers\n")
#         return



#     def addNewUserInDB(self, newName, newEmail, newPswd):
#         result = False
#         newUserInDB = self.userDetailsInDB(self, newName, newEmail, "register")
#         if newUserInDB:
#             raise Exception("User Already exist in database, name = " + newName)
#         else:
#             # connect = sqlite3.connect(self.webSession["dbPath"])
#             # print("Connected to SQL Database")

#             sqlQuery = """INSERT INTO appUsers(userid, name, email, password) VALUES(?,?,?,?)"""
#             txn = self.connection.cursor()
#             txn.execute(sqlQuery, (self.webSession["userid"], newName, newEmail, newPswd))
#             self.connection.commit()
#             self.webSession[""]
#             result = True
#         return result



#     def userDetailsInDB(self, userName, userEmail="", querySender="login", userPwd=""):

#         userEmail = userEmail.upper()
#         txn = self.connection.cursor()

#         sqlQuery = """SELECT * FROM appUsers WHERE name=?"""
#         txn.execute(sqlQuery, (userName,))

#         # Return data as a list of tuple i.e. <list(tuple)>
#         data = txn.fetchall()
#         result = True

#         if len(data) == 0:
#             return False
#         elif len(data) > 1:
#             raise Exception("Database has multiple entries for user = " + userName)
#         else:
#             for row in data:
#                 if row[2] != userEmail:
#                     result = False
#                 elif querySender == "login":
#                     if row[3] != userPwd:
#                         result = False
#         return result



#     def getUseridFromDB(self, userName):
#         """
#         Function to get and store userID from database table into session. In case the user does't exist 
#         i.e. new user then get the last userID in table so that new userid can be created and appended.
#         """
#         userID = 0
#         isUserInDB = self.userDetailsInDB(userName)
#         print("is user in database? : ", isUserInDB)
#         self.webSession["userType"] = "existing-user"

#         # connect = sqlite3.connect(currentSession["dbPath"])
#         txn = self.connection.cursor()

#         if isUserInDB:
#             sqlQuery = """SELECT userid FROM appUsers WHERE name=?"""
#             txn.execute(sqlQuery, (userName,))
#             data = txn.fetchall()
#             self.webSession["userid"] = data[0][0]

#         # If userName string is empty it signifies new member, hence get last entries userId
#         else:
#             sqlQuery = """SELECT * FROM appUsers ORDER BY userid DESC LIMIT 1"""
#             txn.execute(sqlQuery)
#             data = txn.fetchall()
#             # print("data fetched = ", data)
#             if len(data) > 0:
#                 userID = data[0][0]
#             self.webSession["userid"] = userID + 1
#             self.webSession["userType"] = "new-user"

#         return self.webSession














def createDB(dbPath):
    conn = sqlite3.connect(dbPath)
    txn = conn.cursor()
    txn.execute('''CREATE TABLE appUsers (userid INT PRIMARY KEY NOT NULL,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    password TEXT NOT NULL); ''' )
    conn.close()
    print("## New Database created ##")
    print("Database Name = database/appData.db")
    print("Table Name = appData.appUsers\n")
    return



def userDetailsInDB(dbFileName, userName, userEmail="", userPwd=""):

    userEmail = userEmail.upper()

    connect = sqlite3.connect(dbFileName)
    txn = connect.cursor()
    print("Connected to SQL Database from fn:userDetailsInDB ")

    sqlQuery = """SELECT * FROM appUsers WHERE name=?"""
    txn.execute(sqlQuery, (userName,))

    # Return data as a list of tuple i.e. <list(tuple)>
    data = txn.fetchall()

    result = True

    if len(data) == 0:
        return False
    # elif len(data) > 1:
        # raise Exception("Database has multiple entries for user = " + userName)
    else:
        for row in data:
            if row[2].upper() != userEmail:
                result = False
            elif len(userPwd) != 0:
                if row[3] != userPwd:
                    result = False

    return result




def addNewUserInDB(currentSession, newName, newEmail, newPswd):
    result = False
    # newUserInDB = userDetailsInDB(currentSession["dbPath"], newName, newEmail, "register")
    currentSession, isNewUserInDB = getUseridFromDB(currentSession, newName, newEmail)
    print("\n#### Print after getUseridFromDB currentSession = {}\nisnewUserInDB = {}".format(currentSession, isNewUserInDB) )

    if isNewUserInDB:
        raise Exception("User Already exist in database, name = " + newName)
    else:
        connect = sqlite3.connect(currentSession["dbPath"])
        print("Connected to SQL Database, from fn:addNewUserInDB")

        sqlQuery = """INSERT INTO appUsers(userid, name, email, password) VALUES(?,?,?,?)"""
        txn = connect.cursor()
        txn.execute(sqlQuery, (currentSession["userid"], newName, newEmail, newPswd))
        connect.commit()
        result = True

    return result




def getUseridFromDB(currentSession, userName, userEmail):
    """
    Function to get and store userID from database table into session. In case the user does't exist 
    i.e. new user then get the last userID in table so that new userid can be created and appended.
    """
    userID = 0
    isUserInDB = userDetailsInDB(currentSession["dbPath"], userName,userEmail)
    print("is user in database? : ", isUserInDB)

    connect = sqlite3.connect(currentSession["dbPath"])
    txn = connect.cursor()

    if isUserInDB:
        sqlQuery = """SELECT userid FROM appUsers WHERE name=?"""
        txn.execute(sqlQuery, (userName,))
        data = txn.fetchall()
        currentSession["userid"] = data[0][0]
        currentSession["userType"] = "existing-user"
    # If userName string is empty it signifies new member, hence get last entries userId
    else:
        sqlQuery = """SELECT * FROM appUsers ORDER BY userid DESC LIMIT 1"""
        txn.execute(sqlQuery)
        data = txn.fetchall()
        # print("data fetched = ", data)
        if len(data) > 0:
            userID = data[0][0]
        currentSession["userid"] = userID + 1
        currentSession["userType"] = "new-user"

    return currentSession, isUserInDB






def printAllData(dbFileName):

    connect = sqlite3.connect(dbFileName)
    txn = connect.cursor()
    sqlQuery = """SELECT * FROM appUsers"""
    txn.execute(sqlQuery)
    data = txn.fetchall()

    print("Data in database = ", data)

    return





