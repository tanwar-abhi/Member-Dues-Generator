from flask import Flask, render_template, request


# Run the web application (flask)
app = Flask(__name__)

# Run the rout of the web page (python decorator)
@app.route("/", methods = ["GET", "POST"])
def index():

    if request.method == "GET":
        return render_template("index.html")

    if request.method == "POST":
        return render_template("dataCheck.html", FlatNo=request.form.get("FlatNo"))


