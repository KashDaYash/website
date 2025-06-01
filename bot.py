from flask import Flask, render_template
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join("static", "uploads")
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route("/")
def index():
    folder = app.config['UPLOAD_FOLDER']
    files = os.listdir(folder)
    video_files = [f for f in files if f.lower().endswith((".mp4", ".mkv", ".webm"))]
    print("📁 Current files:", video_files)  # Debug
    return render_template("index.html", files=video_files)

@app.route("/watch/<filename>")
def watch(filename):
    if ".." in filename or filename.startswith("/"):
        return "Invalid filename", 400
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(video_path):
        return "File not found", 404
    return render_template("watch.html", filename=filename)

if __name__ == "__main__":
    app.run(debug=True)
