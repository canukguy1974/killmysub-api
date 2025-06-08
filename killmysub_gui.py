import tkinter as tk
from tkinter import messagebox

def start_scan():
    email = email_entry.get()
    if not email or "@gmail.com" not in email:
        messagebox.showerror("Error", "Please enter a valid Gmail address.")
        return
    messagebox.showinfo("Scanning", f"Scanning inbox for {email}...\n(This is just a demo for now.)")

root = tk.Tk()
root.title("KillMySub - Gmail Scanner")

canvas = tk.Canvas(root, height=200, width=400)
canvas.pack()

frame = tk.Frame(root)
frame.place(relx=0.5, rely=0.3, anchor="center")

label = tk.Label(frame, text="Enter your Gmail address:")
label.pack()

email_entry = tk.Entry(frame, width=40)
email_entry.pack(pady=5)

scan_button = tk.Button(frame, text="Scan My Subscriptions", command=start_scan)
scan_button.pack(pady=10)

root.mainloop()
