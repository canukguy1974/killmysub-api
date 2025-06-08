import smtplib
from email.message import EmailMessage
import tkinter as tk
from tkinter import simpledialog, messagebox

def send_email(sender, password, to_email):
    msg = EmailMessage()
    msg.set_content("Thanks for trying our app! You're now on our early access list.")
    msg["Subject"] = "Welcome to the Future"
    msg["From"] = sender
    msg["To"] = to_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender, password)
            smtp.send_message(msg)
        messagebox.showinfo("Success", "Email sent successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def main():
    root = tk.Tk()
    root.withdraw()

    sender = simpledialog.askstring("Sender Email", "Enter your Gmail address:")
    password = simpledialog.askstring("App Password", "Enter your Gmail app password:", show="*")
    recipient = simpledialog.askstring("Recipient", "Enter recipient email:")

    if sender and password and recipient:
        send_email(sender, password, recipient)
    else:
        messagebox.showerror("Error", "All fields are required.")

if __name__ == "__main__":
    main()
