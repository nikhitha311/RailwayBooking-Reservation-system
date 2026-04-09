import tkinter as tk

def open_booking(user):
    root = tk.Tk()
    root.title("Book Ticket")

    tk.Label(root, text="Train Name").pack()
    train = tk.Entry(root)
    train.pack()

    tk.Label(root, text="From").pack()
    source = tk.Entry(root)
    source.pack()

    tk.Label(root, text="To").pack()
    dest = tk.Entry(root)
    dest.pack()

    tk.Label(root, text="Seat Type").pack()
    seat = tk.StringVar()
    tk.Radiobutton(root, text="AC", variable=seat, value="AC").pack()
    tk.Radiobutton(root, text="Non-AC", variable=seat, value="Non-AC").pack()
    tk.Radiobutton(root, text="General", variable=seat, value="General").pack()

    tk.Button(root, text="Confirm Booking").pack(pady=20)

    root.mainloop()
