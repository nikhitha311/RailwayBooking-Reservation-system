import tkinter as tk
from tkinter import messagebox
import cx_Oracle
import winsound
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# ================= DATABASE =================
def get_connection():
    return cx_Oracle.connect("system/password@localhost/XE")  # change password

def signup_user(username, password):
    con = get_connection()
    cur = con.cursor()
    cur.execute("INSERT INTO users VALUES(:1,:2)", (username, password))
    con.commit()
    con.close()

def login_user(username, password):
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE username=:1 AND password=:2",
                (username, password))
    result = cur.fetchone()
    con.close()
    return result

def save_booking(user, train, seat):
    con = get_connection()
    cur = con.cursor()
    cur.execute(
        "INSERT INTO tickets VALUES(ticket_seq.NEXTVAL, :1, :2, :3, 'BOOKED')",
        (user, train, seat)
    )
    con.commit()
    con.close()

# ================= SOUND =================
def beep():
    winsound.Beep(1000, 300)

def horn():
    try:
        winsound.PlaySound("horn.wav", winsound.SND_FILENAME)
    except:
        beep()

# ================= PDF =================
def generate_ticket(user, train, seat):
    doc = SimpleDocTemplate("ticket.pdf")
    styles = getSampleStyleSheet()

    content = []
    content.append(Paragraph("🚆 VCE Railway Ticket", styles['Title']))
    content.append(Paragraph(f"User: {user}", styles['Normal']))
    content.append(Paragraph(f"Train: {train}", styles['Normal']))
    content.append(Paragraph(f"Seat: {seat}", styles['Normal']))

    doc.build(content)

# ================= BOOKING =================
COLORS = {
    "available": "gray",
    "girl": "pink",
    "boy": "lightblue",
    "family": "purple"
}

seats = {}

def open_booking(user):
    root = tk.Tk()
    root.title("Seat Booking")

    selected = tk.StringVar(value="boy")

    tk.Label(root, text="Select Passenger Type").pack()
    tk.Radiobutton(root, text="Girl", variable=selected, value="girl").pack()
    tk.Radiobutton(root, text="Boy", variable=selected, value="boy").pack()
    tk.Radiobutton(root, text="Family", variable=selected, value="family").pack()

    frame = tk.Frame(root)
    frame.pack()

    buttons = {}

    def book(r, c):
        key = (r, c)

        if seats.get(key) == "booked":
            beep()
            return

        seats[key] = "booked"
        buttons[key].config(bg=COLORS[selected.get()])

        save_booking(user, "Express", f"{r}{c}")
        generate_ticket(user, "Express", f"{r}{c}")

        horn()
        messagebox.showinfo("Success", "Ticket Booked!")

    for r in range(5):
        for c in range(5):
            btn = tk.Button(frame, text=f"{r}{c}",
                            bg=COLORS["available"],
                            width=5, height=2,
                            command=lambda r=r, c=c: book(r, c))
            btn.grid(row=r, column=c, padx=5, pady=5)

            buttons[(r, c)] = btn
            seats[(r, c)] = "available"

    root.mainloop()
train_var = tk.StringVar()
train_var.set(trains[0][0])

tk.Label(root, text="Select Train").pack()
tk.OptionMenu(root, train_var, *[t[0] for t in trains]).pack()

# ================= PAYMENT =================
def open_payment():
    root = tk.Tk()
    root.title("Payment")

    tk.Label(root, text="Card Number").pack()
    card = tk.Entry(root)
    card.pack()

    tk.Label(root, text="CVV").pack()
    cvv = tk.Entry(root, show="*")
    cvv.pack()

    def pay():
        if card.get() and cvv.get():
            messagebox.showinfo("Success", "Payment Successful ✅")
            root.destroy()
        else:
            messagebox.showerror("Error", "Enter valid details")

    tk.Button(root, text="Pay Now", command=pay).pack(pady=10)

    root.mainloop()

# ================= DASHBOARD =================
def open_dashboard(user):
    root = tk.Tk()
    root.title("Dashboard")
    root.geometry("400x300")
    root.configure(bg="#a7c7e7")

    tk.Label(root, text=f"Welcome {user}", bg="#a7c7e7",
             font=("Arial", 14)).pack(pady=10)

    tk.Button(root, text="Book Ticket",
              command=lambda: open_booking(user)).pack(pady=10)

    tk.Button(root, text="Payment",
              command=open_payment).pack()

    tk.Label(root,
             text="Admin: M.Nikhitha12A1, M.Dhanush12A2, M.Sathwik12A8",
             bg="#a7c7e7").pack(side="bottom")

    root.mainloop()

# ================= LOGIN =================
def open_login():
    root = tk.Tk()
    root.title("Login")

    tk.Label(root, text="Username").pack()
    user = tk.Entry(root)
    user.pack()

    tk.Label(root, text="Password").pack()
    pwd = tk.Entry(root, show="*")
    pwd.pack()

    def login():
        if login_user(user.get(), pwd.get()):
            root.destroy()
            open_dashboard(user.get())
        else:
            messagebox.showerror("Error", "Invalid Login")

    def signup():
        signup_user(user.get(), pwd.get())
        messagebox.showinfo("Success", "Registered Successfully")

    tk.Button(root, text="Login", command=login).pack(pady=5)
    tk.Button(root, text="Sign Up", command=signup).pack()

    root.mainloop()

# ================= START =================
def start():
    root = tk.Tk()
    root.title("VCE Railway System")

    tk.Label(root, text="🚆 VCE Railway Automation",
             font=("Arial", 18)).pack(pady=50)

    root.after(2000, lambda: [root.destroy(), open_login()])
    root.mainloop()

start()
def cancel_ticket(user):
    con = get_connection()
    cur = con.cursor()

    cur.execute("SELECT ticket_id, train_name, seat_type FROM tickets WHERE username=:1",
                (user,))
    data = cur.fetchall()

    if not data:
        messagebox.showinfo("Info", "No tickets found")
        return

    win = tk.Tk()
    win.title("Cancel Ticket")

    tk.Label(win, text="Select Ticket to Cancel").pack()

    for row in data:
        tid, train, seat = row

        def cancel(tid=tid):
            cur.execute("DELETE FROM tickets WHERE ticket_id=:1", (tid,))
            con.commit()

            messagebox.showinfo("Cancelled",
                                "Ticket Cancelled\nRefund in 3-5 days 💰")
            win.destroy()

        tk.Button(win,
                  text=f"{train} - Seat {seat}",
                  command=cancel).pack()

    win.mainloop()
