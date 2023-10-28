from flask import Flask, render_template, request
import Functions as fn
import os, sqlite3

# Run the web application (flask)
app = Flask(__name__)

# Run the rout of the web page (python decorator)
# @app.route("/", methods = ["GET", "POST"])
@app.route("/", methods = ["POST"])
def index():
    if os.path.isdir("database") == False:
        os.mkdir("database")

    if os.path.is_file("database/appData.db") == False:
        conn = sqlite3.connect("appData.db")
        txn = conn.cursor()
        txn.execute('''CREATE TABLE user (id INT PRIMARY KEY NOT NULL,
                        name TEXT NOT NULL,
                        password TEXT NOT NULL ); ''' )


    return render_template("login.html")
    # return render_template("index.html")




@app.route("/query", methods=["POST"])

def getQueryInputs():

    flatNo = request.form.get("FlatNo")
    memberNumber = request.form.get("MemberNumber")


    # membersDF, intrestDF = fn.getData(dataFileName)

    return render_template("queryData.html", FlatNo=request.form.get("FlatNo"))


