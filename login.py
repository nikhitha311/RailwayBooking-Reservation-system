import tkinter as tk
from db import get_connection
from dashboard import open_dashboard

def login_user(username, password):
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE username=:1 AND password=:2",
                (username, password))
    if cur.fetchone():
        return True
    return False

def register_user(username, password):
    con = get_connection()
    cur = con.cursor()
    cur.execute("INSERT INTO users VALUES(:1,:2)", (username, password))
    con.commit()

def open_login():
    root = tk.Tk()
    root.title("Login")

    tk.Label(root, text="Username").pack()
    username = tk.Entry(root)
    username.pack()

    tk.Label(root, text="Password").pack()
    password = tk.Entry(root, show="*")
    password.pack()

    def login():
        if login_user(username.get(), password.get()):
            root.destroy()
            open_dashboard(username.get())

    def signup():
        register_user(username.get(), password.get())

    tk.Button(root, text="Login", command=login).pack()
    tk.Button(root, text="Sign Up", command=signup).pack()

    root.mainloop()
