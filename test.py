import yt_dlp
import os

# === USER INPUT ===
playlist_url = input("Enter the YouTube playlist URL: ").strip()
download_path = input("Enter the download path (e.g., D:/YouTubeDownloads): ").strip()

# === CREATE FOLDER IF NEEDED ===
os.makedirs(download_path, exist_ok=True)

# === CONFIG FOR BEST VIDEO+AUDIO COMBO ===
ydl_opts = {
    "outtmpl": os.path.join(download_path, "%(playlist_index)s - %(title)s.%(ext)s"),
    "format": "bestvideo[height<=720]+bestaudio/best[height<=720]",
    "merge_output_format": "mp4",
    "noplaylist": False,
    "quiet": False,
    "no_warnings": True,
}

# === DOWNLOAD PLAYLIST ===
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([playlist_url])

print("\n✅ Download complete.")
