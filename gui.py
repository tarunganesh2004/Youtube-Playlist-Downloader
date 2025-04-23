import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import yt_dlp
import threading


# DOWNLOAD FUNCTION
def download_videos():
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
        "progress_hooks": [hook],
    }

    progress_bar.start()
    log_box.delete("1.0", tk.END)

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([playlist_url])
        append_log("✅ Download complete.")
    except Exception as e:
        append_log(f"❌ Error: {str(e)}")
        messagebox.showerror("Download Error", str(e))
    finally:
        progress_bar.stop()


# HOOK FUNCTION 
def hook(d):
    if d["status"] == "downloading":
        filename = d.get("filename", "Unknown")
        percent = d.get("_percent_str", "").strip()
        append_log(f"📥 Downloading: {filename} — {percent}")
    elif d["status"] == "finished":
        append_log("✅ Finished downloading.")


#  THREAD WRAPPER 
def threaded_download():
    t = threading.Thread(target=download_videos)
    t.start()


# LOG FUNCTION 
def append_log(message):
    log_box.insert(tk.END, f"{message}\n")
    log_box.see(tk.END)


#  BROWSE FOLDER
def browse_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        path_var.set(folder_selected)


#  GUI SETUP 
root = tk.Tk()
root.title("YouTube Playlist Downloader")
root.geometry("620x480")
root.resizable(False, False)

#  VARIABLES 
path_var = tk.StringVar()
quality_var = tk.StringVar(value="480p")

#  WIDGETS 
tk.Label(root, text="Playlist URL:", font=("Segoe UI", 10, "bold")).pack(pady=(15, 5))
url_entry = tk.Entry(root, width=75)
url_entry.pack(pady=(0, 10))

tk.Label(root, text="Download Path:", font=("Segoe UI", 10, "bold")).pack()
path_frame = tk.Frame(root)
path_frame.pack(pady=(5, 10))
tk.Entry(path_frame, textvariable=path_var, width=50).pack(side=tk.LEFT, padx=(0, 10))
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

tk.Button(
    root,
    text="Download Playlist",
    command=threaded_download,
    bg="#4CAF50",
    fg="white",
    font=("Segoe UI", 10, "bold"),
    padx=15,
    pady=7,
).pack()

#  PROGRESS BAR 
progress_bar = ttk.Progressbar(root, mode="indeterminate", length=500)
progress_bar.pack(pady=(20, 10))

#  LOG OUTPUT 
tk.Label(root, text="Download Status:", font=("Segoe UI", 10, "bold")).pack()
log_box = tk.Text(root, height=8, width=72)
log_box.pack(pady=(5, 15))

root.mainloop()
