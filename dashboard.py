def open_dashboard(user):
    root = tk.Tk()
    root.title("Dashboard")
    root.geometry("500x400")
    root.configure(bg="#6fa8dc")  # blue-gray

    tk.Label(root, text="🚆 Railway System",
             font=("Arial", 18, "bold"),
             bg="#6fa8dc").pack(pady=10)

    tk.Button(root, text="Book Ticket", width=20,
              command=lambda: open_booking(user)).pack(pady=10)

    tk.Button(root, text="Cancel Ticket", width=20,
              command=lambda: cancel_ticket(user)).pack(pady=10)

    tk.Button(root, text="Payment", width=20,
              command=open_payment).pack(pady=10)

    tk.Label(root,
             text="Admin Panel: M.Nikhitha12A1, M.Dhanush12A2, M.Sathwik12A8",
             bg="#6fa8dc").pack(side="bottom")

    root.mainloop()
