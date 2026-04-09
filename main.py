import tkinter as tk
from login import open_login

def start():
    root = tk.Tk()
    root.title("VCE Railway System")
    root.geometry("600x400")
    root.configure(bg="lightblue")

    label = tk.Label(root, text="🚆 VCE Railway Automation",
                     font=("Arial", 20), bg="lightblue")
    label.pack(pady=100)

    root.after(2000, lambda: [root.destroy(), open_login()])
    root.mainloop()

start()
