from flask import Flask, render_template, request
import os

app = Flask(__name__)

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static/uploads")

@app.route("/")
def index():
    files = os.listdir(UPLOAD_FOLDER)
    print("Current files:", files)  # 👈 Add this
    video_files = [f for f in files if f.lower().endswith((".mp4", ".mkv", ".webm"))]
    return render_template("index.html", files=video_files)


@app.route("/watch/<filename>")
def watch(filename):
    print(f"Requested video: {filename}")
    video_path = os.path.join(UPLOAD_FOLDER, filename)
    print(f"Full video path: {video_path}")
    
    if ".." in filename or filename.startswith("/"):
        return "Invalid filename", 400

    if not os.path.exists(video_path):
        print("File not found!")
        return "File not found", 404

    return render_template("watch.html", filename=filename)
if __name__ == "__main__":
    app.run(debug=True)
