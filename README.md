# 📽️ Telegram Video Uploader & Netflix-Style Web Player

Upload videos from your Telegram bot and stream them directly on a web app using a Netflix-style interface.

---

## 🚀 Features

- Upload videos using `/upload` command in Telegram
- Bot auto-generates permanent streaming link (Telegram CDN)
- Netflix-style grid UI for browsing videos
- Fullscreen HTML5 video player
- Mobile responsive design
- Works on Heroku or any Python-compatible host

---

## ⚙️ Tech Stack

- Python
- Flask
- Pyrogram (Telegram bot)
- HTML + CSS (Netflix-style UI)
- Telegram CDN for video playback

---

## 📁 Folder Structure

/ ├── app.py                 # Flask web app ├── bot.py                 # Telegram bot logic ├── templates/ │   ├── index.html         # Homepage (video grid) │   └── watch.html         # Player page ├── static/ │   └── style.css          # UI styles (optional) ├── videos.json            # Stored video links ├── requirements.txt ├── Procfile └── README.md

---

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/telegram-video-player.git
cd telegram-video-player

2. Install Requirements

pip install -r requirements.txt

3. Set Environment Variables

Create .env file or set directly in bot.py:

API_ID = "YOUR_API_ID"
API_HASH = "YOUR_API_HASH"
BOT_TOKEN = "YOUR_BOT_TOKEN"


---

▶️ Run Locally

python bot.py
python app.py

Now visit: http://localhost:5000


---

🤖 How It Works

1. Send video to bot with /upload


2. Bot fetches Telegram CDN link for video


3. Link and metadata are saved in videos.json


4. Web app reads the JSON and shows videos in Netflix-style grid


5. Clicking any video opens it in a full-screen HTML5 player




---

🛰️ Deploy to Heroku

1. Create App

heroku create your-app-name

2. Push Code

git add .
git commit -m "Deploy"
git push heroku main

3. Set Config Vars

On Heroku dashboard:

API_ID

API_HASH

BOT_TOKEN


4. Open App

heroku open


---

📷 Screenshots

🏠 Home Page

Netflix-style video grid.

🎬 Video Player

Responsive fullscreen video playback.


---

⚠️ Note on Heroku

Heroku does not store uploaded files permanently, so this project uses Telegram CDN to stream videos directly without saving them on Heroku.


---

💡 Sample CDN Code (Python)

file = await bot.get_file(file_id)
cdn_link = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file.file_path}"


---

✅ To-Do

[ ] Add pagination

[ ] Add video titles/descriptions

[ ] Add search & filters

[ ] Add database (SQLite/PostgreSQL)

[ ] Add user authentication (optional)



---

👨‍💻 Author

Made with ❤️ by [KashDaYash]
Telegram: @KashDaYash

---

Isme aap `KashDaYash`, `your-app-name`, aur bot ke credentials ko apne according replace kar lena. Agar aap chaho to `videos.json` ko `SQLite` database se bhi replace kar sakte ho — mujhe batana agar wo bhi chahiye.

