
import tkinter as tk
from tkinter import messagebox
from datetime import datetime


# ==========================================================
# ORIRI — ALARM EDITOR
# Botanical Glass Edition
# ==========================================================

DAY_NAMES = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


class AlarmEditor:

    def __init__(self, parent, colors=None, alarm=None, on_save=None):
        self.parent = parent
        self.colors = colors or self.default_colors()
        self.alarm = alarm.copy() if alarm else {}
        self.on_save = on_save

        self.editing = alarm is not None

        self.window = tk.Toplevel(parent)
        self.window.title(
            "Edit Alarm" if self.editing else "Create Alarm"
        )
        self.window.geometry("460x680")
        self.window.resizable(False, False)
        self.window.configure(bg=self.colors["bg"])
        self.window.transient(parent.winfo_toplevel())
        self.window.grab_set()

        self.build_window()

    # ------------------------------------------------------
    # DEFAULT COLORS
    # ------------------------------------------------------

    def default_colors(self):
        return {
            "bg": "#E5EEE3",
            "panel": "#EDF4E9",
            "card": "#F8FAF5",
            "sidebar": "#A9C7B1",
            "sidebar_light": "#C2D9C5",
            "sidebar_active": "#DCEBDD",
            "sidebar_text": "#294B3B",
            "text": "#315642",
            "muted": "#789381",
            "primary": "#47775D",
            "secondary": "#A9C7B1",
            "accent": "#8CA875",
            "accent_light": "#D5E5D5",
            "border": "#C9DCC9",
            "flower": "#E5C6A4"
        }

    def color(self, key):
        return self.colors.get(key, self.colors["text"])

    # ------------------------------------------------------
    # WINDOW
    # ------------------------------------------------------

    def build_window(self):
        self.build_header()
        self.build_form()
        self.build_buttons()

    # ------------------------------------------------------
    # HEADER
    # ------------------------------------------------------

    def build_header(self):
        header = tk.Frame(
            self.window,
            bg=self.color("primary"),
            padx=27,
            pady=23
        )
        header.pack(fill="x")

        tk.Label(
            header,
            text="✿  ORIRI",
            font=("Arial", 9, "bold"),
            fg=self.color("accent_light"),
            bg=self.color("primary")
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Edit your alarm" if self.editing else "A new beginning",
            font=("Georgia", 23, "bold"),
            fg=self.color("card"),
            bg=self.color("primary")
        ).pack(anchor="w", pady=(8, 3))

        tk.Label(
            header,
            text="Set a time that works for your day.",
            font=("Arial", 9),
            fg=self.color("accent_light"),
            bg=self.color("primary")
        ).pack(anchor="w")

    # ------------------------------------------------------
    # FORM
    # ------------------------------------------------------

    def build_form(self):
        body = tk.Frame(
            self.window,
            bg=self.color("bg"),
            padx=27,
            pady=20
        )
        body.pack(fill="both", expand=True)

        # Time
        self.field_label(body, "ALARM TIME")

        self.time_var = tk.StringVar(
            value=self.alarm.get("time", "07:00")
        )

        self.time_entry = tk.Entry(
            body,
            textvariable=self.time_var,
            font=("Consolas", 27, "bold"),
            fg=self.color("primary"),
            bg=self.color("card"),
            relief="flat",
            justify="center",
            insertbackground=self.color("primary")
        )
        self.time_entry.pack(
            fill="x",
            ipady=9,
            pady=(7, 17)
        )

        # Name
        self.field_label(body, "ALARM NAME")

        self.name_var = tk.StringVar(
            value=self.alarm.get("label", "")
        )

        self.name_entry = tk.Entry(
            body,
            textvariable=self.name_var,
            font=("Arial", 10),
            fg=self.color("text"),
            bg=self.color("card"),
            relief="flat",
            insertbackground=self.color("primary")
        )
        self.name_entry.pack(
            fill="x",
            ipady=9,
            pady=(7, 17)
        )

        # Note
        self.field_label(body, "NOTE (OPTIONAL)")

        self.note_var = tk.StringVar(
            value=self.alarm.get("note", "")
        )

        self.note_entry = tk.Entry(
            body,
            textvariable=self.note_var,
            font=("Arial", 9),
            fg=self.color("text"),
            bg=self.color("card"),
            relief="flat",
            insertbackground=self.color("primary")
        )
        self.note_entry.pack(
            fill="x",
            ipady=8,
            pady=(7, 17)
        )

        # Repeat
        self.field_label(body, "REPEAT")

        repeat_frame = tk.Frame(
            body,
            bg=self.color("bg")
        )
        repeat_frame.pack(
            fill="x",
            pady=(9, 17)
        )

        saved_days = self.alarm.get("repeat", [])
        self.day_vars = {}

        for day in DAY_NAMES:
            variable = tk.BooleanVar(
                value=day in saved_days
            )

            self.day_vars[day] = variable

            tk.Checkbutton(
                repeat_frame,
                text=day,
                variable=variable,
                font=("Arial", 8, "bold"),
                fg=self.color("text"),
                bg=self.color("accent_light"),
                activebackground=self.color("secondary"),
                selectcolor=self.color("secondary"),
                indicatoron=False,
                relief="flat",
                padx=7,
                pady=8,
                cursor="hand2"
            ).pack(side="left", padx=(0, 5))

        # Enabled
        self.enabled_var = tk.BooleanVar(
            value=self.alarm.get("enabled", True)
        )

        tk.Checkbutton(
            body,
            text="Enable this alarm",
            variable=self.enabled_var,
            font=("Arial", 9, "bold"),
            fg=self.color("text"),
            bg=self.color("bg"),
            activebackground=self.color("bg"),
            selectcolor=self.color("accent_light"),
            cursor="hand2"
        ).pack(anchor="w", pady=(0, 10))

    # ------------------------------------------------------
    # FIELD LABEL
    # ------------------------------------------------------

    def field_label(self, parent, text):
        tk.Label(
            parent,
            text=text,
            font=("Arial", 8, "bold"),
            fg=self.color("primary"),
            bg=self.color("bg")
        ).pack(anchor="w")

    # ------------------------------------------------------
    # BUTTONS
    # ------------------------------------------------------

    def build_buttons(self):
        footer = tk.Frame(
            self.window,
            bg=self.color("bg"),
            padx=27,
            pady=17
        )
        footer.pack(fill="x")

        tk.Frame(
            footer,
            bg=self.color("border"),
            height=1
        ).pack(fill="x", pady=(0, 15))

        tk.Button(
            footer,
            text="Cancel",
            font=("Arial", 9, "bold"),
            fg=self.color("muted"),
            bg=self.color("bg"),
            activebackground=self.color("panel"),
            relief="flat",
            padx=16,
            pady=10,
            cursor="hand2",
            command=self.close
        ).pack(side="left")

        tk.Button(
            footer,
            text="Save Alarm",
            font=("Arial", 9, "bold"),
            fg=self.color("card"),
            bg=self.color("primary"),
            activebackground=self.color("sidebar_text"),
            activeforeground=self.color("card"),
            relief="flat",
            padx=22,
            pady=10,
            cursor="hand2",
            command=self.save
        ).pack(side="right")

    # ------------------------------------------------------
    # SAVE
    # ------------------------------------------------------

    def save(self):
        raw_time = self.time_var.get().strip()

        try:
            datetime.strptime(raw_time, "%H:%M")
        except ValueError:
            messagebox.showerror(
                "Invalid Time",
                "Enter time in 24-hour format, such as 07:30 or 18:45.",
                parent=self.window
            )
            return

        label = self.name_var.get().strip()

        if not label:
            label = "Morning Alarm"

        selected_days = [
            day for day in DAY_NAMES
            if self.day_vars[day].get()
        ]

        new_alarm = {
            "time": raw_time,
            "label": label,
            "note": self.note_var.get().strip(),
            "repeat": selected_days,
            "enabled": self.enabled_var.get()
        }

        if self.on_save:
            self.on_save(new_alarm)

        self.close()

    # ------------------------------------------------------
    # CLOSE
    # ------------------------------------------------------

    def close(self):
        try:
            self.window.grab_release()
        except tk.TclError:
            pass

        self.window.destroy()
