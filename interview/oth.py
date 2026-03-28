import tkinter as tk
from tkinter import messagebox, ttk
from playwright.sync_api import sync_playwright
import subprocess
import threading
import os

def get_master_url(ep_num):
    """Finds the master m3u8 playlist for a specific episode."""
    target_url = f"https://w.shadwo.pro/albaplayer/kurulus-osman-s01e{ep_num:02}/"
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        master_url = None

        # Listen for the playlist file (master.m3u8)
        def intercept(request):
            nonlocal master_url
            if "master.m3u8" in request.url:
                master_url = request.url

        page.on("request", intercept)
        
        try:
            page.goto(target_url, wait_until="networkidle", timeout=30000)
            page.wait_for_timeout(3000) # Give it a moment to load the player
        except:
            pass
        
        browser.close()
        return master_url

def download_engine(start_ep, end_ep, quality, status_label):
    for ep in range(start_ep, end_ep + 1):
        status_label.config(text=f"Ep {ep}: Finding Link...")
        url = get_master_url(ep)
        
        if url:
            status_label.config(text=f"Ep {ep}: Downloading {quality}...")
            # yt-dlp command to select quality and save as mp4
            # 'bestvideo[height<=720]+bestaudio' filters for your choice
            filename = f"Kurulus_Osman_S01E{ep:02}_{quality}.mp4"
            cmd = [
                "yt-dlp", 
                "-f", f"bestvideo[height<={quality[:-1]}]+bestaudio/best[height<={quality[:-1]}]",
                "--merge-output-format", "mp4",
                "-o", filename,
                url
            ]
            subprocess.run(cmd)
        else:
            print(f"Failed to find link for episode {ep}")
            
    status_label.config(text="All Downloads Completed!")
    messagebox.showinfo("Done", "Your episodes are ready.")

def start_task():
    try:
        s = int(ent_start.get())
        e = int(ent_end.get())
        q = combo_quality.get()
        threading.Thread(target=download_engine, args=(s, e, q, lbl_status), daemon=True).start()
    except ValueError:
        messagebox.showerror("Error", "Enter valid episode numbers.")

# --- UI Layout ---
root = tk.Tk()
root.title("Osman Batch Downloader")
root.geometry("350x300")

tk.Label(root, text="Start Episode:").pack(pady=5)
ent_start = tk.Entry(root)
ent_start.pack()

tk.Label(root, text="End Episode:").pack(pady=5)
ent_end = tk.Entry(root)
ent_end.pack()

tk.Label(root, text="Select Quality:").pack(pady=5)
combo_quality = ttk.Combobox(root, values=["1080p", "720p", "480p", "360p"])
combo_quality.set("720p")
combo_quality.pack()

btn_go = tk.Button(root, text="Start Download", command=start_task, bg="#2ecc71", fg="white", font=('bold'))
btn_go.pack(pady=20)

lbl_status = tk.Label(root, text="Status: Ready", fg="blue")
lbl_status.pack()

root.mainloop()