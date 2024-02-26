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

    # Create upload directory, where uploaded files will be saved
    if os.path.isdir(UPLOAD_FOLDER) == False:
        os.mkdir(UPLOAD_FOLDER)
        print("## Created Upload Folder and filepath = {}".format(UPLOAD_FOLDER))

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




@app.route("/logout", methods=["GET", "POST"])
def logout():
    session["name"] = None
    return redirect("/")




@app.route("/query", methods=["GET","POST"])
def getQuery():

    if request.method == "POST":
        print("## Inside ROUTe=/query ; request type is POST deteected")


        uploadedDataFile = request.files["datafile"]
        uploadedTempFile = request.files["tempfile"]


        if uploadedDataFile:
            session["allowedDataFile"], securedDataFileName = fn.fileUploadCheck_Preprocess(uploadedDataFile.filename, 
                                                                        ALLOWED_EXTENSIONS_DATA, "xls Members Data")

        if uploadedTempFile:
            session["allowedTempFile"], securedTempFileName = fn.fileUploadCheck_Preprocess(uploadedTempFile.filename, 
                                                                        ALLOWED_EXTENSIONS_TEMP, "docx Template file")


        # Checking if uploaded data, template File in post request
        if session["allowedDataFile"] and session["allowedTempFile"]:
            # Save the uploaded files to local directory
            uploadedDataFile.save(os.path.join(app.config['UPLOAD_FOLDER'], securedDataFileName))
            uploadedTempFile.save(os.path.join(app.config['UPLOAD_FOLDER'], securedTempFileName))


            # Generate Doc requests
            dataFileName = UPLOAD_FOLDER + securedDataFileName
            templateFile = UPLOAD_FOLDER + securedTempFileName

            FlatNo = request.form.get("FlatNo")
            memberNo = request.form.get("membershipNo")
            # print("\n################\n## Recieived data FlatNo = ", FlatNo)
            # print("## Recieived data MemberNo = {}\n".format(memberNo))

            nextMC = 0
            exportFolder = session["downloadFolder"]

            try:
                # Make folder to save all letters
                if os.path.isdir(exportFolder) == False:
                    os.mkdir(exportFolder)

                FlatNo, nextMC = fn.processUserInputs(FlatNo, nextMC)

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
                                                                        ALLOWED_EXTENSIONS_DATA, "Members Data in defaulter")

        if session["allowedDataFile"]:

            uploadedDataFile.save(os.path.join(app.config['UPLOAD_FOLDER'] , securedFileName))

            dataFileName = UPLOAD_FOLDER + securedFileName


            # Get user selected type of defaulter from webpage
            defaulterType = request.form.get("defaulterList")

            if defaulterType == "MDD":
                defaulterType = "1"
            elif defaulterType == "CCD":
                defaulterType = "2"
            else:
                defaulterType = "3"


            try:
                # Make folder to save the defaulter list
                if os.path.isdir(session["downloadFolder"]) == False:
                    os.mkdir(session["downloadFolder"])

                fn.mainDefaulter(dataFileName, session["downloadFolder"], defaulterType)
                return render_template("success.html", fName=securedFileName, fPath=session["downloadFolder"])
            except:
                print(" !!!! Error :: Exception caught, something when wrong in defaulter query request")
                return render_template("failed.html", failedFileType="Error in main defaulter query function")

        else:
            return render_template("defaulterQuery.html")


    else:
        return render_template("defaulterQuery.html")


