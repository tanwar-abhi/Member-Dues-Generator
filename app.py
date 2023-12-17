from flask import Flask, render_template, request, redirect, session
# from fileinput import filename
from flask_session import Session
import src.Functions as fn
import os, sqlite3
from werkzeug.utils import secure_filename
from datetime import date

# Run the web application (flask)
app = Flask(__name__)


# Configuring sessions
# Saving sessions on servers itself
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Create some variables in session to be used accross whole code.
session["databaseName"] = "appData.db"
session["dbPath"] = os.getcwd() + "/database/appData.db"
session = fn.getUseridFromDB(session)


# File upload path and configurations
UPLOAD_FOLDER = os.getcwd() + "/database/fileUploaded/"
ALLOWED_EXTENSIONS_DATA = {"xls", "xlsx", "xlsm", "xlsb", "pdf", "txt"}
ALLOWED_EXTENSIONS_TEMP = {"doc", "docx"}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER




@app.route("/")
def index():
    if os.path.isdir("database") == False:
        os.mkdir("database")
        fn.createDB("database/appData.db")
    else:
        if os.path.isfile("database/appData.db") == False:
            fn.createDB("database/appData.db")


    if not session.get("name"):
        return redirect ("/login")
    # return render_template("postLogin.html", userName=session["name"])
    return render_template("postLogin.html")




@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        session["name"] = request.form.get("userName")
        return redirect("/")
    return render_template("login.html")




@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        userName = request.form.get("uName")
        email = request.form.get("userEmail")
        pwd = request.form.get("userPwd")

        fn.addNewUserInDB(session["dbPath"], userName, email, "register", )

    return render_template("register.html")




@app.route("/logout", methods=["GET", "POST"])
def logout():
    session["name"] = None
    return redirect("/")




@app.route("/query", methods=["GET","POST"])
def getQueryInputs():

    if request.method == "POST":
        print("## Inside ROUTe=/query ; request type is POST deteected")
        if os.path.isdir(UPLOAD_FOLDER) == False:
            os.mkdir(UPLOAD_FOLDER)
            print("## Created Upload Folder and filepath")


        uploadedDataFile = request.files["datafile"]
        uploadedTempFile = request.files["tempfile"]
        # print("\n")
        # print("@@ resquest.files  = ", request.files)
        # print("\n")
        # print("@@ request  = ", request)
        # print("\n")
        # print("@@ Session = ", session)
        # print("\n")


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
            return render_template("failed.html", failedFileType="Template")


        if session["allowedDataFile"] and session["allowedTempFile"]:
            # Generate Doc requests
            dataFileName = UPLOAD_FOLDER + securedDataFileName
            templateFile = UPLOAD_FOLDER + securedTempFileName

            FlatNo = request.form.get("FlatNo")
            memberNo = request.form.get("membershipNo")
            print("## Recieived data FlatNo = ", FlatNo)
            print("## Recieived data MemberNo = ", memberNo)
            nextMC = 0
            folderName = "Maintenance_Demand_" + date.today().strftime("%m-%Y") + "/"
            fn.main(dataFileName, FlatNo, memberNo, nextMC, templateFile, folderName)

            return render_template("success.html", fName=securedDataFileName, fPath=UPLOAD_FOLDER)

        else:
            session["allowedDataFile"] = False
            # uploadStatus = {'uploadSuccess': False}
            # uploadStatus = False
            return render_template("failed.html", failedFileType="Data")



    # if request.method == "GET":
    else:
        print("## request type is GET deteected")
        if request.args.get("selection") == "logout":
            return redirect("/logout")

        elif request.args.get("selection") == "defaulter":
            return render_template("defaulterQuery.html")

    return render_template("queryData.html")


