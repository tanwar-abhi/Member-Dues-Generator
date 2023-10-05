from flask import Flask, render_template, request
import Functions as fn

# Run the web application (flask)
app = Flask(__name__)

# Run the rout of the web page (python decorator)
# @app.route("/", methods = ["GET", "POST"])
@app.route("/", methods = ["POST"])
def index():
    return render_template("index.html")




@app.route("/query", methods=["POST"])

def getQueryInputs():

    flatNo = request.form.get("FlatNo")
    memberNumber = request.form.get("MemberNumber")


    # membersDF, intrestDF = fn.getData(dataFileName)

    return render_template("queryData.html", FlatNo=request.form.get("FlatNo"))


