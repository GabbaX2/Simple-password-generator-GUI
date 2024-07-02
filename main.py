import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import string
import secrets
import datetime
import sqlite3


class CustomButton(tk.Button):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.rounded_image = self.create_rounded_image(150, 50, 25, "#4B0082")
        self.rounded_image_hover = self.create_rounded_image(150, 50, 25, "#9370DB")

        self.photo = ImageTk.PhotoImage(self.rounded_image)
        self.photo_hover = ImageTk.PhotoImage(self.rounded_image_hover)

        self.config(
            image=self.photo,
            compound="center",
            relief=tk.FLAT,
            bd=0,
            highlightthickness=0,
            padx=10,
            pady=5,
            font=("Arial", 12, "bold"),
            foreground="white"
        )

        self.bind("<Enter>", self.on_hover)
        self.bind("<Leave>", self.on_leave)

    def create_rounded_image(self, width, height, radius, color):
        image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        draw.rounded_rectangle((0, 0, width, height), radius, fill=color)
        return image

    def on_hover(self, event):
        self.config(image=self.photo_hover)

    def on_leave(self, event):
        self.config(image=self.photo)


def generate_password(length):
    characters = string.ascii_uppercase + string.ascii_lowercase + string.digits
    password = ''.join(secrets.choice(characters) for i in range(length))
    return password


def update_password():
    try:
        length = int(length_entry.get())
        if length < 1:
            raise ValueError
        password = generate_password(length)
        password_text.set(password)
        save_password_to_db(password)
    except ValueError:
        password_text.set("Invalid length")


def save_password_to_db(password):
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS passwords
                 (id INTEGER PRIMARY KEY, timestamp TEXT, password TEXT)''')
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO passwords (timestamp, password) VALUES (?, ?)", (timestamp, password))
    conn.commit()
    conn.close()


def create_tooltip(widget, text):
    tooltip = tk.Toplevel(widget)
    tooltip.withdraw()
    tooltip.wm_overrideredirect(True)
    label = tk.Label(tooltip, text=text, background="pink", relief="solid", borderwidth=1, font=("Arial", 10))
    label.pack()

    def on_enter(event):
        x, y, _, _ = widget.bbox("insert")
        x += widget.winfo_rootx() + 25
        y += widget.winfo_rooty() + 25
        tooltip.wm_geometry(f"+{x}+{y}")
        tooltip.deiconify()

    def on_leave(event):
        tooltip.withdraw()

    widget.bind("<Enter>", on_enter)
    widget.bind("<Leave>", on_leave)


root = tk.Tk()
root.title("Password Generator")
root.geometry("700x450")
root.configure(bg="#000000")

password_text = tk.StringVar()

frame = tk.Frame(root, bg="#000000")
frame.pack(pady=20)

length_label = tk.Label(frame, text="Enter the length of the password:", bg="#000000", font=("Arial", 12))
length_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
length_entry = tk.Entry(frame, font=("Arial", 12))
length_entry.grid(row=0, column=1, padx=10, pady=10)
length_entry.focus()

create_tooltip(length_entry, "Enter a number for the password length")

button = CustomButton(frame, text="Generate Password", command=update_password)
button.grid(row=1, columnspan=2, pady=20)

label = tk.Label(frame, textvariable=password_text, font=("Arial", 14), bg="#000000", fg="#4B0082")
label.grid(row=2, columnspan=2, pady=20)

root.mainloop()
