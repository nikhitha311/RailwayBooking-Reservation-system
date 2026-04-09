import tkinter as tk
from booking import open_booking

def open_dashboard(user):
    root = tk.Tk()
    root.title("Dashboard")
    root.geometry("600x400")
    root.configure(bg="#a7c7e7")  # gray-blue

    tk.Label(root, text=f"Welcome {user}", font=("Arial", 16),
             bg="#a7c7e7").pack()

    tk.Button(root, text="Book Ticket",
              command=lambda: open_booking(user)).pack(pady=20)

    tk.Button(root, text="View Ticket").pack()
    tk.Button(root, text="Help").pack(side="left")
    tk.Button(root, text="Settings").pack(side="right")

    # Admin Info
    tk.Label(root,
             text="Admin: M.Nikhitha12A1, M.Dhanush12A2, M.Sathwik12A8",
             bg="#a7c7e7").pack(side="bottom")

    root.mainloop()
