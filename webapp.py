
from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def index():
    files = os.listdir("static/uploads")
    return render_template("index.html", files=files)

@app.route('/watch/<filename>')
def watch(filename):
    return render_template("watch.html", filename=filename)

@app.route('/static/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory("static/uploads", filename)
