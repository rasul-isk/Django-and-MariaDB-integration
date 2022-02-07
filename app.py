from flask import Flask, request, render_template, jsonify
from datetime import datetime


app = Flask(__name__)

# Importing settings
import DBcm
from appconfig import config

# Importing Pages


@app.get("/")  # HTTP request:   GET  /
def index():
    return render_template("index.html")


@app.get("/aboutme")
def aboutme():
    """
    Retrieve the aboutme.html file from the hard disk, and send it to the
    browser.
    """
    return render_template("aboutme.html")


@app.get("/CV")
def CV():
    """
    Retrieve the CV.html file from the hard disk, and send it to the
    browser.
    """
    return render_template("CV.html")


@app.get("/hobbies")
def hobbies():
    """
    Retrieve the hobbies.html file from the hard disk, and send it to the
    browser.
    """
    return render_template("hobbies.html")


@app.get("/feedback")
def feedback():
    """
    Retrieve the feedback.html file from the hard disk, and send it to the
    browser.
    """
    return render_template("feedback.html")


@app.get("/computing")
def computing():
    """
    Retrieve the computing.html file from the hard disk, and send it to the
    browser.
    """
    return render_template("computing.html")


@app.get("/computing/softdev")
def softdev():
    """
    Retrieve the softdev.html file from the hard disk, and send it to the
    browser.
    """
    return render_template("softdev.html")


@app.get("/computing/VR")
def VR():
    """
    Retrieve the VR.html file from the hard disk, and send it to the
    browser.
    """
    return render_template("VR.html")


@app.get("/computing/IT")
def IT():
    """
    Retrieve the IT.html file from the hard disk, and send it to the
    browser.
    """
    return render_template("IT.html")


# Submitting Form
@app.route("/savedata", methods=["POST"])  # This is the same as @app.post in Flask 2.
def save_the_data():
    # grab the data from the HTML form and extract each piece.
    thename = request.form["name"]
    theemail = request.form["email"]
    themessage = request.form["message"]

    # gather current exact time
    now = datetime.now()
    # fromat it like "dd/mm/YY H:M:S"
    thetime = now.strftime("%d/%m/%Y %H:%M:%S")

    # save the pieces of data to the database table.
    with DBcm.UseDatabase(config) as db:
        SQL = """
            insert into feedbacks
            (name, email, message, time)
            values
            ( %s, %s, %s, %s)
        """
        db.execute(SQL, (thename, theemail, themessage, thetime))
    return render_template(
        "thanks.html",
        title="Thanks for your information",
        who=thename,
        what=themessage,
    )


@app.get("/recent")
def grab_latest_data():
    with DBcm.UseDatabase(config) as db:
        SQL = """
            select name, email, message, time
            from feedbacks
            order by id desc
        """
        db.execute(SQL)
        data = db.fetchall()
    return render_template("recent.html", title="The most recent feedbacks.", data=data)


if __name__ == "__main__":
    app.run(debug=True)  # pragma: no cover
