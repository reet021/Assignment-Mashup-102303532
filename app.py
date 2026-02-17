from flask import Flask, render_template, request
import subprocess
import zipfile
import os
import re

app = Flask(__name__)

def valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        singer = request.form["singer"]
        videos = request.form["videos"]
        duration = request.form["duration"]
        email = request.form["email"]

        if not valid_email(email):
            return "Invalid Email ID"

        output_file = "mashup.mp3"

        command = f'python 102303532.py "{singer}" {videos} {duration} {output_file}'
        subprocess.run(command, shell=True)

        zip_name = "mashup.zip"

        with zipfile.ZipFile(zip_name, 'w') as zipf:
            zipf.write(output_file)

        return "Mashup created successfully and zipped!"

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
