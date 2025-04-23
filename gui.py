import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import yt_dlp
import threading

# FFMPEG Path Handling
FFMPEG_PATH = os.path.join(os.path.dirname(__file__), "ffmpeg.exe")

# Flags
stop_download_flag = threading.Event()


def download_videos():
    stop_download_flag.clear()

    playlist_url = url_entry.get().strip()
    download_path = path_var.get()
    selected_quality = quality_var.get()

    if not playlist_url or not download_path:
        messagebox.showerror(
            "Error", "Please enter the playlist URL and select a download path."
        )
        return

    quality_format_map = {
        "480p": "bestvideo[height<=480]+bestaudio/best[height<=480]",
        "720p": "bestvideo[height<=720]+bestaudio/best[height<=720]",
        "1080p": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
    }

    ydl_opts = {
        "outtmpl": os.path.join(
            download_path, "%(playlist_index)s - %(title)s.%(ext)s"
        ),
        "format": quality_format_map.get(selected_quality, "bestvideo+bestaudio"),
        "merge_output_format": "mp4",
        "noplaylist": False,
        "quiet": True,
        "no_warnings": True,
        "ffmpeg_location": FFMPEG_PATH,
        "progress_hooks": [hook],
    }

    progress_bar.start()
    log_box.delete("1.0", tk.END)

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([playlist_url])
        if not stop_download_flag.is_set():
            append_log("✅ Download complete.")
    except Exception as e:
        append_log(f"❌ Error: {str(e)}")
        messagebox.showerror("Download Error", str(e))
    finally:
        progress_bar.stop()


# Download hook
def hook(d):
    if stop_download_flag.is_set():
        raise Exception("⛔ Download canceled by user.")
    if d["status"] == "downloading":
        filename = d.get("filename", "Unknown")
        percent = d.get("_percent_str", "").strip()
        append_log(f"📥 Downloading: {filename} — {percent}")
    elif d["status"] == "finished":
        append_log("✅ Finished downloading.")


# Cancel functionality
def cancel_download():
    stop_download_flag.set()
    append_log("⚠️ Cancel requested. Stopping download...")


# Thread wrapper
def threaded_download():
    t = threading.Thread(target=download_videos)
    t.start()


# UI Log
def append_log(message):
    log_box.insert(tk.END, f"{message}\n")
    log_box.see(tk.END)


# Folder browser
def browse_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        path_var.set(folder_selected)


# GUI SETUP
root = tk.Tk()
root.title("YouTube Playlist Downloader")
root.geometry("700x520")
root.resizable(False, False)

path_var = tk.StringVar()
quality_var = tk.StringVar(value="480p")

# Widgets
tk.Label(root, text="Playlist URL:", font=("Segoe UI", 10, "bold")).pack(pady=(15, 5))
url_entry = tk.Entry(root, width=80)
url_entry.pack(pady=(0, 10))

tk.Label(root, text="Download Path:", font=("Segoe UI", 10, "bold")).pack()
path_frame = tk.Frame(root)
path_frame.pack(pady=(5, 10))
tk.Entry(path_frame, textvariable=path_var, width=55).pack(side=tk.LEFT, padx=(0, 10))
tk.Button(path_frame, text="Browse", command=browse_folder).pack(side=tk.LEFT)

tk.Label(root, text="Select Quality:", font=("Segoe UI", 10, "bold")).pack()
quality_dropdown = ttk.Combobox(
    root,
    textvariable=quality_var,
    values=["480p", "720p", "1080p"],
    state="readonly",
    width=20,
)
quality_dropdown.pack(pady=(5, 15))

# Buttons
btn_frame = tk.Frame(root)
btn_frame.pack(pady=5)
tk.Button(
    btn_frame,
    text="Download Playlist",
    command=threaded_download,
    bg="#4CAF50",
    fg="white",
    font=("Segoe UI", 10, "bold"),
    padx=15,
    pady=7,
).pack(side=tk.LEFT, padx=10)

tk.Button(
    btn_frame,
    text="Cancel",
    command=cancel_download,
    bg="#f44336",
    fg="white",
    font=("Segoe UI", 10, "bold"),
    padx=15,
    pady=7,
).pack(side=tk.LEFT, padx=10)

# Progress
progress_bar = ttk.Progressbar(root, mode="indeterminate", length=550)
progress_bar.pack(pady=(20, 10))

# Logs
tk.Label(root, text="Download Status:", font=("Segoe UI", 10, "bold")).pack()
log_box = tk.Text(root, height=8, width=80)
log_box.pack(pady=(5, 15))

root.mainloop()