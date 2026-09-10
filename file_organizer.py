import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov", ".webm"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".ppt", ".pptx", ".xls", ".xlsx"],
    "Audio": [".mp3", ".wav", ".aac", ".flac", ".ogg"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Programs": [".exe", ".msi", ".apk"],
}

def organize_folder(folder):
    moved = 0

    for filename in os.listdir(folder):
        source = os.path.join(folder, filename)

        if not os.path.isfile(source):
            continue

        extension = os.path.splitext(filename)[1].lower()
        category = "Others"

        for folder_name, extensions in FILE_TYPES.items():
            if extension in extensions:
                category = folder_name
                break

        destination_folder = os.path.join(folder, category)
        os.makedirs(destination_folder, exist_ok=True)

        destination = os.path.join(destination_folder, filename)

        # Avoid overwriting files with the same name
        if os.path.exists(destination):
            name, ext = os.path.splitext(filename)
            counter = 1

            while os.path.exists(destination):
                new_name = f"{name}_{counter}{ext}"
                destination = os.path.join(destination_folder, new_name)
                counter += 1

        shutil.move(source, destination)
        moved += 1

    return moved

def choose_folder():
    folder = filedialog.askdirectory()

    if not folder:
        return

    folder_entry.delete(0, tk.END)
    folder_entry.insert(0, folder)

def organize():
    folder = folder_entry.get().strip()

    if not folder:
        messagebox.showwarning("Warning", "Please select a folder.")
        return

    if not os.path.isdir(folder):
        messagebox.showerror("Error", "Selected folder does not exist.")
        return

    try:
        moved = organize_folder(folder)

        messagebox.showinfo(
            "Completed",
            f"File organization completed!\n\nFiles moved: {moved}"
        )

    except PermissionError:
        messagebox.showerror(
            "Permission Error",
            "You do not have permission to modify this folder."
        )

    except Exception as e:
        messagebox.showerror("Error", str(e))


# GUI
root = tk.Tk()
root.title("File Organizer")
root.geometry("600x350")
root.resizable(False, False)

title = tk.Label(
    root,
    text="📁 File Organizer",
    font=("Arial", 26, "bold")
)
title.pack(pady=25)

tk.Label(
    root,
    text="Select the folder you want to organize:",
    font=("Arial", 13)
).pack()

frame = tk.Frame(root)
frame.pack(pady=15)

folder_entry = tk.Entry(
    frame,
    width=45,
    font=("Arial", 12)
)
folder_entry.pack(side="left", padx=5)

browse_button = tk.Button(
    frame,
    text="Browse",
    font=("Arial", 11, "bold"),
    command=choose_folder
)
browse_button.pack(side="left")

organize_button = tk.Button(
    root,
    text="Organize Files",
    font=("Arial", 14, "bold"),
    command=organize
)
organize_button.pack(pady=20)

info = tk.Label(
    root,
    text="Images • Videos • Documents • Audio • Archives • Programs • Others",
    font=("Arial", 10)
)
info.pack(pady=10)

root.mainloop()
