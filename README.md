# 🎬 YouTube Playlist Downloader (Desktop App)

A lightweight Python desktop application that allows you to download entire YouTube playlists at your preferred quality (480p, 720p, or 1080p) with just a few clicks. Now bundled with `ffmpeg.exe` for seamless audio/video merging!

---

## 🚀 Features

- 📥 Download entire YouTube playlists
- 🎚 Select video quality: 480p, 720p, or 1080p
- 🧾 Real-time download log
- 🎛 GUI built with Tkinter
- ⚡ Includes `ffmpeg.exe` so no external installation required
- 🧵 Downloads handled in separate thread for smooth UI
- ⛔ Cancel button to stop ongoing download

---

## 📦 Requirements

- Python 3.8+
- Works on Windows (Tested on Windows 10/11)

> ⚠️ If you're using the `.exe` version, you don't need Python installed.

---

## 🛠 How to Run from Source

1. **Clone or download** this repository.
2. Place `ffmpeg.exe` in the same folder as the script (if building manually).
3. Install dependencies:

```bash
pip install yt-dlp
```

## 🖥️ How to Build the .exe

This bundles everything (including `ffmpeg.exe`) into a single file for easy sharing.

### Install PyInstaller:

```bash
pip install pyinstaller
```

### Build the .exe with ffmpeg included:

```bash
pyinstaller --onefile --add-binary "ffmpeg.exe;." gui.py
```

Your `.exe` file will be in the `dist/` folder.

✅ You can now share this `.exe` with friends. No need to install Python or `ffmpeg` separately.

## 📸 App Preview

Simple interface with real-time progress updates.

```
+---------------------------------------------------+
| Playlist URL: [_______________________________]   |
| [ Browse ] [ Quality Dropdown ] [Download Now]    |
|                                                   |
| ── Progress Bar Here ───────────────────────────  |
|                                                   |
| Download Log:                                     |
| [ Text Log Area ]                                 |
+---------------------------------------------------+
```

## ❗ Common Issues

⚠️ **Error: "ffmpeg is not installed"**

Make sure you're using the version of the app that includes `ffmpeg.exe`, or build it yourself using the command below:

```bash
pyinstaller --onefile --add-binary "ffmpeg.exe;." gui.py
```

🛑 **Antivirus blocks the file**

Since it's a custom `.exe`, some antivirus programs may flag it as suspicious. You can either:

- Mark it as safe manually.
- Or rebuild the application yourself using the source code and PyInstaller.

📱 **Mobile Support?**

This app is currently built for desktop only.

For mobile YouTube playlist downloads, consider using:

- NewPipe (Android)

Or stay tuned — mobile support may be added in the future!

## 🙌 Credits

- Built using `yt-dlp`
- GUI built with `tkinter`
- Video merging powered by `ffmpeg`