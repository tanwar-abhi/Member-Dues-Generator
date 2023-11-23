from flask import Flask, render_template, request, redirect, session
from flask_session import Session
import src.Functions as fn
# import os, sqlite3

# Run the web application (flask)
app = Flask(__name__)


# Configuring sessions
# Saving sessions on servers itslef
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Running app in debug mode
# app.run(debug=True)

@app.route("/")
def index():
    if not session.get("name"):
        return redirect ("/login")
    return render_template("postLogin.html", userName=session["name"])






@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        session["name"] = request.form.get("userName")
        return redirect("/")
    return render_template("login.html")





# 
# # Run the rout of the web page (python decorator)
# # @app.route("/", methods = ["GET", "POST"])
# @app.route("/", methods = ["POST"])
# def index():
#     if os.path.isdir("database") == False:
#         os.mkdir("database")

#     if os.path.is_file("database/appData.db") == False:
#         conn = sqlite3.connect("appData.db")
#         txn = conn.cursor()
#         txn.execute('''CREATE TABLE user (id INT PRIMARY KEY NOT NULL,
#                         name TEXT NOT NULL,
#                         password TEXT NOT NULL,
#                         email TEXT NOT NULL); ''' )
#         conn.close()

#     return render_template("login.html")
#     # return render_template("index.html")
# 


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

    # if request.method == "POST":
    #     # if request.form["queryType"] == "newQuery":
    #     if "newQuery" in request.form:
    #         flatNo = request.form.get("FlatNo")

    #         if not flatNo:
    #             memberNumber = request.form.get("MemberNumber")

    #         # membersDF, intrestDF = fn.getData(dataFileName)
    #         return render_template("queryData.html", FlatNo=request.form.get("FlatNo"))


    if request.method == "GET":
        if request.args.get("selection") == "logout":
            return redirect("/logout")

        elif request.args.get("selection") == "defaulter":
            return render_template("defaulterQuery.html")

    return render_template("queryData.html")


