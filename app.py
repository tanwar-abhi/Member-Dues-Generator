from flask import Flask, render_template, request, redirect, session
# from fileinput import filename
from flask_session import Session
import os, sqlite3
from werkzeug.utils import secure_filename
from datetime import date

import src.Functions as fn
import src.dbOperations as db


# Run the web application (flask)
app = Flask(__name__)


# Configuring sessions
# Saving sessions on servers itself
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)




# File upload path and configurations
UPLOAD_FOLDER = os.getcwd() + "/database/fileUploaded/"
ALLOWED_EXTENSIONS_DATA = {"xls", "xlsx", "xlsm", "xlsb", "csv"}
ALLOWED_EXTENSIONS_TEMP = {"doc", "docx", "odt"}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER




@app.route("/")
def index():
    if os.path.isdir("database") == False:
        os.mkdir("database")
        db.createDB("database/appData.db")

    else:
        if os.path.isfile("database/appData.db") == False:
            db.createDB("database/appData.db")

    if not session.get("name"):
        return redirect ("/login")

    return render_template("postLogin.html")




@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        session["name"] = request.form.get("userName")
        session["databaseName"] = "appData.db"
        session["dbPath"] = os.getcwd() + "/database/appData.db"
        exportFolder = "Maintenance_Demand_" + date.today().strftime("%m-%Y") + "/"
        session["downloadFolder"] = exportFolder

        print("\n# Session = ", session)
        return redirect("/")
    return render_template("login.html")




@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        userName = request.form.get("uName")
        email = request.form.get("userEmail")
        pwd = request.form.get("userPwd")

        # Add new user to the database
        # db.addNewUserInDB(session, userName, email, pwd)

    return render_template("register.html")




# @app.route("/logout", methods=["GET", "POST"])
@app.route("/logout", methods=["GET"])
def logout():
    session["name"] = None
    return redirect("/")




@app.route("/query", methods=["GET","POST"])
def getQueryInputs():

    if request.method == "POST":
        print("## Inside ROUTe=/query ; request type is POST deteected")
        if os.path.isdir(UPLOAD_FOLDER) == False:
            os.mkdir(UPLOAD_FOLDER)
            print("## Created Upload Folder and filepath = {}".format(UPLOAD_FOLDER))


        uploadedDataFile = request.files["datafile"]
        uploadedTempFile = request.files["tempfile"]


        # Checking if uploaded data File in post request
        if uploadedDataFile and fn.isAllowed(uploadedDataFile.filename, EXTENSIONS=ALLOWED_EXTENSIONS_DATA):
            session["allowedDataFile"] = True
            print("## Data File uploaded successfully in query page.\n")
            securedDataFileName = secure_filename(uploadedDataFile.filename)
            uploadedDataFile.save(os.path.join(app.config['UPLOAD_FOLDER'], securedDataFileName))
        else:
            print("!!!! DF Error :: unable to upload data file")
            session["allowedDataFile"] = False

        # Checking if uploaded template File in post request
        if uploadedTempFile and fn.isAllowed(uploadedTempFile.filename, EXTENSIONS=ALLOWED_EXTENSIONS_TEMP):
            session["allowedTempFile"] = True
            print("## Template file uploaded sucssesfully in query page.\n")
            securedTempFileName = secure_filename(uploadedTempFile.filename)
            uploadedTempFile.save(os.path.join(app.config['UPLOAD_FOLDER'], securedTempFileName))
        else:
            session["allowedTempFile"] = False
            print("!!!! TF Error :: unable to upload Template file")



        if session["allowedDataFile"] and session["allowedTempFile"]:
            # Generate Doc requests
            dataFileName = UPLOAD_FOLDER + securedDataFileName
            templateFile = UPLOAD_FOLDER + securedTempFileName

            FlatNo = request.form.get("FlatNo")
            memberNo = request.form.get("membershipNo")
            print("\n################\n## Recieived data FlatNo = ", FlatNo)
            print("## Recieived data MemberNo = {}\n".format(memberNo))


            nextMC = 0
            exportFolder = session["downloadFolder"]
            # session["downloadFolder"] = exportFolder

            # Make folder to save all letters
            if os.path.isdir(exportFolder) == False:
                os.mkdir(exportFolder)

            FlatNo, nextMC = fn.processUserInputs(FlatNo, nextMC)

            try:
                fn.main(dataFileName, FlatNo, memberNo, nextMC, templateFile, exportFolder)
            except:
                print(" !!!! Error :: Exception caught, something when wrong in query main ")
                return render_template("failed.html", failedFileType="Error in main query function")

            return render_template("success.html", fName=securedDataFileName, fPath=UPLOAD_FOLDER)

        else:
            errorFrom = "Template"
            if session["allowedDataFile"] == False:
                errorFrom = "Data"
            return render_template("failed.html", failedFileType=errorFrom)


    # if request.method == "GET":
    else:
        print("## request type is GET deteected")
        if request.args.get("selection") == "logout":
            return redirect("/logout")

        elif request.args.get("selection") == "defaulter":
            return redirect("/defaulter")

    return render_template("queryData.html")





@app.route("/defaulter", methods=["GET", "POST"])
def defaulter():
    if  request.method == "POST":
        print("The method is post\n## Inside ROUTE = /defaulter")
        uploadedDataFile = request.files["datafile"]

        if uploadedDataFile:
            session["allowedDataFile"], securedFileName = fn.fileUploadCheck_Preprocess(uploadedDataFile.filename, 
                                                                        ALLOWED_EXTENSIONS_DATA, "Members Data")

        if session["allowedDataFile"]:

            uploadedDataFile.save(os.path.join(session["downloadFolder"] , securedFileName))
            print("Inside defaulter ROUTE \nSession = ")
            print(session)

            dataFileName = UPLOAD_FOLDER + securedFileName
            try:
                fn.mainDefaulter(dataFileName, session["downloadFolder"])
            except:
                print(" !!!! Error :: Exception caught, something when wrong in defaulter query request")
                return render_template("failed.html", failedFileType="Error in main defaulter query function")

        else:
            return render_template("defaulterQuery.html")



    else:
        return render_template("defaulterQuery.html")


