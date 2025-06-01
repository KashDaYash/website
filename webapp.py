from flask import Flask, render_template, request
import os

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"

@app.route("/")
def index():
    # static/uploads folder me jitni bhi video files hain, unki list lo
    files = os.listdir(UPLOAD_FOLDER)
    # sirf video files (mp4, mkv, etc) filter karo agar chaho
    video_files = [f for f in files if f.endswith((".mp4", ".mkv", ".webm"))]
    return render_template("index.html", files=video_files)

@app.route("/watch/<filename>")
def watch(filename):
    # Security check - only serve files from uploads folder
    if ".." in filename or filename.startswith("/"):
        return "Invalid filename", 400

    video_path = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(video_path):
        return "File not found", 404

    return render_template("watch.html", filename=filename)

if __name__ == "__main__":
    app.run(debug=True)
