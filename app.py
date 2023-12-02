from flask import Flask, render_template, request, redirect, session
from flask_session import Session
import src.Functions as fn
import os, sqlite3
from werkzeug.utils import secure_filename


# Run the web application (flask)
app = Flask(__name__)


# Configuring sessions
# Saving sessions on servers itslef
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# File upload path and configurations
UPLOAD_FOLDER = "database/fileUploaded"
ALLOWED_EXTENSIONS = {"xls", "xlsx", "xlsm", "xlsb", "pdf", "txt"}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER




@app.route("/")
def index():
    if os.path.isdir("database") == False:
        os.mkdir("database")
        fn.createDB("database/appData.db")
    else:
        if os.path.isfile("database/appData.db") == False:
            fn.createDB("database/appData.db")
        else:
            print("## Database already exist in filesystem.")

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

    return render_template("register.html")




@app.route("/logout", methods=["GET", "POST"])
def logout():
    session["name"] = None
    return redirect("/")




@app.route("/query", methods=["GET","POST"])
def getQueryInputs():

    print("## Inside /query")

    if request.method == "POST":
        print("## request type is POST deteected")
        if os.path.isdir(UPLOAD_FOLDER) == False:
            os.mkdir(UPLOAD_FOLDER)
            print("## Created Upload Folder and filepath")

        uploadedFile = request.files["dataFile"]
        # Checking if uploadedFile in post request
        # print("## Filename = ", uploadedFile.filename)
        securedFileName = secure_filename(uploadedFile.filename)
        print("## Secured file name")
        uploadedFile.save(securedFileName)
        print("## File saved successfully in folder = ", UPLOAD_FOLDER)

        if uploadedFile:
            print("## get the uploaded file from request object")
        if fn.isAllowed(uploadedFile.filename, EXTENSIONS=ALLOWED_EXTENSIONS):
            print("## file extension checked")


        if uploadedFile and fn.isAllowed(uploadedFile.filename, EXTENSIONS=ALLOWED_EXTENSIONS):
            print("## uploaded a File in query page.\n## Extension of file exist in allowed extensions")
            securedFileName = secure_filename(uploadedFile.filename)
            uploadedFile.save(os.path.join(app.config['UPLOAD_FOLDER'], securedFileName))
        return render_template("success.html", fName=securedFileName, fPath=UPLOAD_FOLDER)

    # if request.method == "GET":
    else:
        print("## request type is GET deteected")
        if request.args.get("selection") == "logout":
            return redirect("/logout")

        elif request.args.get("selection") == "defaulter":
            return render_template("defaulterQuery.html")

    return render_template("queryData.html")


