import tkinter as tk
from tkinter import messagebox
import requests
import webbrowser
import re

API_URL = "https://killmysub-api-production.up.railway.app/scan"  # Confirm this is the correct route

def start_scan():
    email = email_entry.get()
    phone = phone_entry.get()

    if not email or "@gmail.com" not in email:
        messagebox.showerror("Error", "Please enter a valid Gmail address.")
        return

    phone_clean = re.sub(r"[^\d+]", "", phone)
    if not phone_clean.startswith("+") or not phone_clean[1:].isdigit():
        messagebox.showerror("Error", "Enter a valid phone number with country code (e.g., +15195551234).")
        return

    payload = {"email": email, "phone": phone_clean}
    print("👉 Sending to:", API_URL)
    print("👉 Payload:", payload)

    try:
        response = requests.post(API_URL, json=payload)
        print("👉 Response code:", response.status_code)
        print("👉 Response body:", response.text)

        if response.ok:
            messagebox.showinfo("Success", "Scan request sent successfully!")
        else:
            messagebox.showerror("Error", f"Server error: {response.status_code}\n{response.text}")
    except Exception as e:
        messagebox.showerror("Exception", str(e))

def open_kofi():
    webbrowser.open_new("https://ko-fi.com/bestie37134")

# GUI setup
root = tk.Tk()
root.title("KillMySub - Gmail Scanner")
root.geometry("400x370")

frame = tk.Frame(root)
frame.place(relx=0.5, rely=0.35, anchor="center")

tk.Label(frame, text="Enter your Gmail address:").pack(pady=(0, 5))
email_entry = tk.Entry(frame, width=40)
email_entry.pack()

tk.Label(frame, text="Enter your phone number (+ country code):").pack(pady=(15, 5))
phone_entry = tk.Entry(frame, width=40)
phone_entry.pack()

tk.Button(frame, text="Scan My Subscriptions", command=start_scan).pack(pady=20)
tk.Button(root, text="☕ Buy Me a Coffee", command=open_kofi, fg="white", bg="#29abe0").pack(pady=5)

root.mainloop()
