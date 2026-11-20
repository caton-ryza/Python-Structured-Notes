import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime


# ==========================================================
# ORIRI — MY ALARMS
# Dynamic Theme Edition
# ==========================================================

DAY_NAMES = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
ALARM_FILE = os.path.join(DATA_DIR, "alarms.json")


# ==========================================================
# FILE STORAGE
# ==========================================================

def load_alarms():
    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(ALARM_FILE):
        return []

    try:
        with open(ALARM_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def save_alarms(alarms):
    os.makedirs(DATA_DIR, exist_ok=True)

    with open(ALARM_FILE, "w", encoding="utf-8") as file:
        json.dump(alarms, file, indent=4)


# ==========================================================
# ALARMS PAGE
# ==========================================================

class AlarmsPage(tk.Frame):

    def __init__(self, parent, app=None):
        self.app = app
        self.colors = app.theme if app else {
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

        self.alarms = load_alarms()

        self.C = self.colors

        super().__init__(parent, bg=self.C["bg"])

        self.build_page()

    # ------------------------------------------------------
    # COLOR HELPERS
    # ------------------------------------------------------

    def color(self, key):
        return self.C.get(key, self.C["text"])

    def create_label(
        self,
        parent,
        text,
        font=("Arial", 10),
        fg=None,
        bg=None,
        **kwargs
    ):
        return tk.Label(
            parent,
            text=text,
            font=font,
            fg=fg or self.color("text"),
            bg=bg or self.color("bg"),
            **kwargs
        )

    def create_button(
        self,
        parent,
        text,
        command,
        primary=False,
        **kwargs
    ):
        background = (
            self.color("primary")
            if primary else self.color("accent_light")
        )

        foreground = (
            self.color("card")
            if primary else self.color("text")
        )

        active_background = (
            self.color("sidebar_text")
            if primary else self.color("secondary")
        )

        return tk.Button(
            parent,
            text=text,
            command=command,
            font=("Arial", 9, "bold"),
            bg=background,
            fg=foreground,
            activebackground=active_background,
            activeforeground=foreground,
            relief="flat",
            bd=0,
            padx=15,
            pady=9,
            cursor="hand2",
            **kwargs
        )

    # ------------------------------------------------------
    # PAGE LAYOUT
    # ------------------------------------------------------

    def build_page(self):
        self.container = tk.Frame(
            self,
            bg=self.color("bg")
        )
        self.container.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=28
        )

        self.build_header()
        self.build_summary()
        self.build_alarm_section()
        self.refresh_alarm_cards()

    # ------------------------------------------------------
    # HEADER
    # ------------------------------------------------------

    def build_header(self):
        header = tk.Frame(
            self.container,
            bg=self.color("bg")
        )
        header.pack(fill="x", pady=(0, 25))

        left = tk.Frame(
            header,
            bg=self.color("bg")
        )
        left.pack(side="left", fill="x", expand=True)

        self.create_label(
            left,
            "YOUR DAILY RHYTHM",
            font=("Arial", 9, "bold"),
            fg=self.color("primary")
        ).pack(anchor="w")

        self.create_label(
            left,
            "My Alarms",
            font=("Georgia", 29, "bold")
        ).pack(anchor="w", pady=(5, 3))

        self.create_label(
            left,
            "A gentle reminder to begin each day.",
            font=("Arial", 10),
            fg=self.color("muted")
        ).pack(anchor="w")

        self.create_button(
            header,
            "+  Add Alarm",
            self.open_editor,
            primary=True
        ).pack(side="right", anchor="center")

    # ------------------------------------------------------
    # SUMMARY
    # ------------------------------------------------------

    def build_summary(self):
        summary = tk.Frame(
            self.container,
            bg=self.color("bg")
        )
        summary.pack(fill="x", pady=(0, 27))

        self.total_value = self.create_summary_card(
            summary,
            "TOTAL ALARMS",
            "0",
            "Your saved reminders"
        )

        self.active_value = self.create_summary_card(
            summary,
            "ACTIVE",
            "0",
            "Ready for the day"
        )

        self.next_value = self.create_summary_card(
            summary,
            "NEXT ALARM",
            "--:--",
            "Upcoming reminder"
        )

    def create_summary_card(self, parent, title, value, subtitle):
        card = tk.Frame(
            parent,
            bg=self.color("card"),
            highlightbackground=self.color("border"),
            highlightthickness=1,
            padx=17,
            pady=15
        )

        card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 11)
        )

        self.create_label(
            card,
            title,
            font=("Arial", 8, "bold"),
            fg=self.color("muted"),
            bg=self.color("card")
        ).pack(anchor="w")

        value_label = self.create_label(
            card,
            value,
            font=("Georgia", 22, "bold"),
            fg=self.color("primary"),
            bg=self.color("card")
        )
        value_label.pack(anchor="w", pady=(6, 2))

        self.create_label(
            card,
            subtitle,
            font=("Arial", 8),
            fg=self.color("muted"),
            bg=self.color("card")
        ).pack(anchor="w")

        return value_label

    # ------------------------------------------------------
    # ALARM SECTION
    # ------------------------------------------------------

    def build_alarm_section(self):
        section_header = tk.Frame(
            self.container,
            bg=self.color("bg")
        )
        section_header.pack(fill="x", pady=(0, 13))

        self.create_label(
            section_header,
            "Your reminders",
            font=("Georgia", 18, "bold")
        ).pack(side="left")

        self.count_label = self.create_label(
            section_header,
            "",
            font=("Arial", 9),
            fg=self.color("muted")
        )
        self.count_label.pack(side="right", pady=(7, 0))

        self.cards_area = tk.Frame(
            self.container,
            bg=self.color("bg")
        )
        self.cards_area.pack(fill="both", expand=True)

    # ------------------------------------------------------
    # REFRESH ALARM CARDS
    # ------------------------------------------------------

    def refresh_alarm_cards(self):
        for widget in self.cards_area.winfo_children():
            widget.destroy()

        total = len(self.alarms)

        active = sum(
            1 for alarm in self.alarms
            if alarm.get("enabled", True)
        )

        self.total_value.config(text=str(total))
        self.active_value.config(text=str(active))

        self.count_label.config(
            text=f"{total} saved reminder{'s' if total != 1 else ''}"
        )

        next_alarm = self.get_next_alarm()

        self.next_value.config(
            text=next_alarm if next_alarm else "--:--"
        )

        if not self.alarms:
            self.show_empty_state()
            return

        for column in range(2):
            self.cards_area.grid_columnconfigure(
                column,
                weight=1,
                uniform="alarm_cards"
            )

        for index, alarm in enumerate(self.alarms):
            row = index // 2
            column = index % 2

            self.create_alarm_card(
                self.cards_area,
                alarm,
                index,
                row,
                column
            )

    # ------------------------------------------------------
    # NEXT ALARM
    # ------------------------------------------------------

    def get_next_alarm(self):
        now = datetime.now()
        upcoming = []

        for alarm in self.alarms:
            if not alarm.get("enabled", True):
                continue

            try:
                hour, minute = map(
                    int,
                    alarm.get("time", "00:00").split(":")
                )

                alarm_time = now.replace(
                    hour=hour,
                    minute=minute,
                    second=0,
                    microsecond=0
                )

                if alarm_time > now:
                    upcoming.append(alarm_time)

            except (ValueError, TypeError):
                continue

        if not upcoming:
            return None

        return min(upcoming).strftime("%I:%M %p").lstrip("0")

    # ------------------------------------------------------
    # EMPTY STATE
    # ------------------------------------------------------

    def show_empty_state(self):
        empty = tk.Frame(
            self.cards_area,
            bg=self.color("card"),
            highlightbackground=self.color("border"),
            highlightthickness=1,
            padx=25,
            pady=40
        )
        empty.pack(fill="x", pady=8)

        self.create_label(
            empty,
            "✿",
            font=("Georgia", 35),
            fg=self.color("flower"),
            bg=self.color("card")
        ).pack()

        self.create_label(
            empty,
            "Nothing scheduled just yet",
            font=("Georgia", 17, "bold"),
            bg=self.color("card")
        ).pack(pady=(8, 5))

        self.create_label(
            empty,
            "Create your first alarm and give tomorrow a softer beginning.",
            font=("Arial", 9),
            fg=self.color("muted"),
            bg=self.color("card")
        ).pack(pady=(0, 17))

        self.create_button(
            empty,
            "+  Create your first alarm",
            self.open_editor
        ).pack()

    # ------------------------------------------------------
    # ALARM CARD
    # ------------------------------------------------------

    def create_alarm_card(self, parent, alarm, index, row, column):
        card = tk.Frame(
            parent,
            bg=self.color("card"),
            highlightbackground=self.color("border"),
            highlightthickness=1,
            padx=18,
            pady=16
        )

        card.grid(
            row=row,
            column=column,
            sticky="nsew",
            padx=(0, 11 if column == 0 else 0),
            pady=(0, 13)
        )

        top = tk.Frame(
            card,
            bg=self.color("card")
        )
        top.pack(fill="x")

        time_text = self.format_time(
            alarm.get("time", "07:00")
        )

        self.create_label(
            top,
            time_text,
            font=("Consolas", 25, "bold"),
            fg=self.color("primary"),
            bg=self.color("card")
        ).pack(side="left")

        enabled_var = tk.BooleanVar(
            value=alarm.get("enabled", True)
        )

        toggle = tk.Checkbutton(
            top,
            variable=enabled_var,
            command=lambda i=index, v=enabled_var: self.toggle_alarm(i, v),
            bg=self.color("card"),
            activebackground=self.color("card"),
            fg=self.color("primary"),
            selectcolor=self.color("accent_light"),
            cursor="hand2"
        )
        toggle.pack(side="right")

        self.create_label(
            card,
            alarm.get("label", "Morning Alarm"),
            font=("Arial", 11, "bold"),
            bg=self.color("card")
        ).pack(anchor="w", pady=(7, 2))

        repeat = alarm.get("repeat", [])

        repeat_text = (
            "  ·  ".join(repeat)
            if repeat else "One-time alarm"
        )

        self.create_label(
            card,
            repeat_text,
            font=("Arial", 8),
            fg=self.color("muted"),
            bg=self.color("card")
        ).pack(anchor="w")

        note = alarm.get("note", "")

        if note:
            self.create_label(
                card,
                note,
                font=("Arial", 8, "italic"),
                fg=self.color("muted"),
                bg=self.color("card"),
                wraplength=280,
                justify="left"
            ).pack(anchor="w", pady=(8, 0))

        tk.Frame(
            card,
            bg=self.color("border"),
            height=1
        ).pack(fill="x", pady=(14, 10))

        actions = tk.Frame(
            card,
            bg=self.color("card")
        )
        actions.pack(fill="x")

        self.create_button(
            actions,
            "Edit",
            lambda i=index: self.open_editor(i)
        ).pack(side="left")

        tk.Button(
            actions,
            text="Delete",
            font=("Arial", 8),
            fg=self.color("accent"),
            bg=self.color("card"),
            activebackground=self.color("accent_light"),
            relief="flat",
            padx=10,
            pady=6,
            cursor="hand2",
            command=lambda i=index: self.delete_alarm(i)
        ).pack(side="right")

    # ------------------------------------------------------
    # TIME FORMATTING
    # ------------------------------------------------------

    def format_time(self, value):
        try:
            parsed = datetime.strptime(value, "%H:%M")
            return parsed.strftime("%I:%M %p").lstrip("0")
        except (ValueError, TypeError):
            return value

    # ------------------------------------------------------
    # TOGGLE
    # ------------------------------------------------------

    def toggle_alarm(self, index, variable):
        self.alarms[index]["enabled"] = variable.get()

        save_alarms(self.alarms)
        self.refresh_alarm_cards()

    # ------------------------------------------------------
    # DELETE
    # ------------------------------------------------------

    def delete_alarm(self, index):
        confirmed = messagebox.askyesno(
            "Delete Alarm",
            "Would you like to delete this alarm?",
            parent=self
        )

        if not confirmed:
            return

        self.alarms.pop(index)

        save_alarms(self.alarms)
        self.refresh_alarm_cards()

    # ------------------------------------------------------
    # ADD / EDIT WINDOW
    # ------------------------------------------------------

    def open_editor(self, index=None):
        editing = index is not None

        alarm = (
            self.alarms[index].copy()
            if editing else {}
        )

        window = tk.Toplevel(self)
        window.title(
            "Edit Alarm" if editing else "Create Alarm"
        )
        window.geometry("440x650")
        window.resizable(False, False)
        window.configure(bg=self.color("bg"))
        window.transient(self.winfo_toplevel())
        window.grab_set()

        # Header
        header = tk.Frame(
            window,
            bg=self.color("primary"),
            padx=25,
            pady=22
        )
        header.pack(fill="x")

        self.create_label(
            header,
            "✿  ORIRI",
            font=("Arial", 9, "bold"),
            fg=self.color("accent_light"),
            bg=self.color("primary")
        ).pack(anchor="w")

        self.create_label(
            header,
            "Edit your alarm" if editing else "A new beginning",
            font=("Georgia", 22, "bold"),
            fg=self.color("card"),
            bg=self.color("primary")
        ).pack(anchor="w", pady=(8, 2))

        self.create_label(
            header,
            "Set a time that works for your day.",
            font=("Arial", 9),
            fg=self.color("accent_light"),
            bg=self.color("primary")
        ).pack(anchor="w")

        body = tk.Frame(
            window,
            bg=self.color("bg"),
            padx=25,
            pady=18
        )
        body.pack(fill="both", expand=True)

        # Time
        self.editor_label(body, "ALARM TIME")

        time_var = tk.StringVar(
            value=alarm.get("time", "07:00")
        )

        time_entry = tk.Entry(
            body,
            textvariable=time_var,
            font=("Consolas", 25, "bold"),
            fg=self.color("primary"),
            bg=self.color("card"),
            relief="flat",
            justify="center",
            insertbackground=self.color("primary")
        )
        time_entry.pack(
            fill="x",
            ipady=9,
            pady=(7, 17)
        )

        # Name
        self.editor_label(body, "ALARM NAME")

        name_var = tk.StringVar(
            value=alarm.get("label", "")
        )

        name_entry = tk.Entry(
            body,
            textvariable=name_var,
            font=("Arial", 10),
            fg=self.color("text"),
            bg=self.color("card"),
            relief="flat",
            insertbackground=self.color("primary")
        )
        name_entry.pack(
            fill="x",
            ipady=9,
            pady=(7, 17)
        )

        # Note
        self.editor_label(body, "NOTE (OPTIONAL)")

        note_var = tk.StringVar(
            value=alarm.get("note", "")
        )

        note_entry = tk.Entry(
            body,
            textvariable=note_var,
            font=("Arial", 9),
            fg=self.color("text"),
            bg=self.color("card"),
            relief="flat",
            insertbackground=self.color("primary")
        )
        note_entry.pack(
            fill="x",
            ipady=8,
            pady=(7, 17)
        )

        # Repeat
        self.editor_label(body, "REPEAT")

        repeat_frame = tk.Frame(
            body,
            bg=self.color("bg")
        )
        repeat_frame.pack(
            fill="x",
            pady=(9, 17)
        )

        saved_days = alarm.get("repeat", [])
        day_vars = {}

        for day in DAY_NAMES:
            var = tk.BooleanVar(
                value=day in saved_days
            )
            day_vars[day] = var

            tk.Checkbutton(
                repeat_frame,
                text=day,
                variable=var,
                font=("Arial", 8, "bold"),
                fg=self.color("text"),
                bg=self.color("accent_light"),
                activebackground=self.color("secondary"),
                selectcolor=self.color("secondary"),
                indicatoron=False,
                relief="flat",
                padx=7,
                pady=7,
                cursor="hand2"
            ).pack(side="left", padx=(0, 4))

        # Buttons
        button_row = tk.Frame(
            body,
            bg=self.color("bg")
        )
        button_row.pack(
            fill="x",
            side="bottom",
            pady=(12, 0)
        )

        tk.Button(
            button_row,
            text="Cancel",
            font=("Arial", 9, "bold"),
            fg=self.color("muted"),
            bg=self.color("bg"),
            activebackground=self.color("panel"),
            relief="flat",
            padx=15,
            pady=10,
            cursor="hand2",
            command=window.destroy
        ).pack(side="left")

        def save_alarm():
            raw_time = time_var.get().strip()

            try:
                datetime.strptime(raw_time, "%H:%M")
            except ValueError:
                messagebox.showerror(
                    "Invalid Time",
                    "Please enter the time in 24-hour format, such as 07:30 or 18:45.",
                    parent=window
                )
                return

            label = name_var.get().strip()

            if not label:
                label = "Morning Alarm"

            selected_days = [
                day for day in DAY_NAMES
                if day_vars[day].get()
            ]

            new_alarm = {
                "time": raw_time,
                "label": label,
                "note": note_var.get().strip(),
                "repeat": selected_days,
                "enabled": alarm.get("enabled", True)
            }

            if editing:
                self.alarms[index] = new_alarm
            else:
                self.alarms.append(new_alarm)

            save_alarms(self.alarms)
            self.refresh_alarm_cards()
            window.destroy()

        self.create_button(
            button_row,
            "Save Alarm",
            save_alarm,
            primary=True
        ).pack(side="right")

        time_entry.focus_set()

    # ------------------------------------------------------
    # EDITOR LABEL
    # ------------------------------------------------------

    def editor_label(self, parent, text):
        self.create_label(
            parent,
            text,
            font=("Arial", 8, "bold"),
            fg=self.color("primary"),
            bg=self.color("bg")
        ).pack(anchor="w")


# ==========================================================
# END OF ALARMS PAGE
# ==========================================================