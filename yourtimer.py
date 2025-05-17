import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import random
import os

TARGET_FILE = "target_date.txt"

class YourtimeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Your Time..")
        self.root.geometry("500x280")
        self.root.configure(bg="#121212")

        self.font_large = ("Courier New", 24, "bold")
        self.font_medium = ("Courier New", 12)
        self.red_shades = ["#ff0000", "#cc0000", "#aa0000", "#ff2222", "#ff4444"]

        # Input UI
        self.label = tk.Label(root, text="Enter target date (YYYY-MM-DD HH:MM:SS):",
                              fg="#ff4444", bg="#121212", font=self.font_medium)
        self.label.pack(pady=10)

        self.entry = tk.Entry(root, font=self.font_medium, fg="#ff4444", bg="#2a2a2a",
                              insertbackground="#ff4444", justify="center", width=25)
        self.entry.pack(pady=5)

        self.start_button = tk.Button(root, text="Start Countdown", command=self.start_countdown,
                                      bg="#ff0000", fg="#121212", font=self.font_medium,
                                      activebackground="#990000", cursor="hand2")
        self.start_button.pack(pady=10)

        self.output_label = tk.Label(root, text="", font=self.font_large,
                                     fg="#ff2222", bg="#121212")
        self.output_label.pack(pady=15)

        self.footer = tk.Label(root, text="", font=("Courier New", 10, "italic"),
                               fg="#660000", bg="#121212")
        self.footer.pack(pady=5)

        self.target = None
        self.running = False

        self.load_target_date()

    def calculate_difference(self, target):
        now = datetime.now()
        diff = target - now
        if diff.total_seconds() < 0:
            return None

        days = diff.days
        seconds = diff.seconds

        years = days // 365
        days %= 365
        months = days // 30
        days %= 30
        hours = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60

        return years, months, days, hours, minutes, seconds

    def flicker_text(self, text):
        color = random.choice(self.red_shades)
        self.output_label.config(fg=color, text=text)

    def update_countdown(self):
        if not self.running:
            return

        now = datetime.now()
        if self.target <= now:
            self.output_label.config(text=" Time's up. Goodbye. ", fg="#cc0000")
            self.footer.config(text="You cannot escape the inevitable...")
            self.running = False
            return

        time_left = self.calculate_difference(self.target)
        if time_left:
            y, m, d, h, mi, s = time_left
            display = f"{y:02}y {m:02}m {d:02}d {h:02}h {mi:02}m {s:02}s left"
            self.flicker_text(display)
            self.footer.config(text=f"Target: {self.target.strftime('%Y-%m-%d %H:%M:%S')}")
            self.root.after(1000, self.update_countdown)

    def start_countdown(self):
        date_str = self.entry.get()
        try:
            target = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            if target <= datetime.now():
                messagebox.showerror("Error", "Target date must be in the future.")
                return
            self.target = target
            self.save_target_date(target)
            self.running = True
            self.update_countdown()
        except ValueError:
            messagebox.showerror("Error", "Invalid date format.\nUse YYYY-MM-DD HH:MM:SS.")

    def save_target_date(self, target):
        with open(TARGET_FILE, "w") as f:
            f.write(target.strftime("%Y-%m-%d %H:%M:%S"))

    def load_target_date(self):
        if os.path.exists(TARGET_FILE):
            try:
                with open(TARGET_FILE, "r") as f:
                    date_str = f.read().strip()
                    target = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                    if target > datetime.now():
                        self.target = target
                        self.running = True
                        self.update_countdown()
                    else:
                        os.remove(TARGET_FILE)  # Target date is expired
            except Exception:
                pass

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = YourtimeGUI(root)
    root.mainloop()
