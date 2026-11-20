
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


# ==========================================================
# ORIRI — ALARM EDITOR
# Botanical Glass Edition
# ==========================================================

class AlarmEditor:

    DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    def __init__(
        self,
        parent,
        alarm=None,
        colors=None,
        on_save=None,
        on_cancel=None
    ):
        self.parent = parent
        self.alarm = alarm or {}
        self.colors = colors or self.default_colors()

        self.on_save = on_save
        self.on_cancel = on_cancel

        self.drag_x = 0
        self.drag_y = 0

        self.window = tk.Toplevel(parent)
        self.window.overrideredirect(True)
        self.window.geometry("460x680")
        self.window.resizable(False, False)
        self.window.configure(bg=self.color("bg"))
        self.window.transient(parent.winfo_toplevel())

        self.window.protocol(
            "WM_DELETE_WINDOW",
            self.cancel
        )

        self.create_variables()
        self.build_ui()
        self.center_window()

        self.window.grab_set()
        self.window.focus_force()

    # ------------------------------------------------------
    # COLORS
    # ------------------------------------------------------

    def default_colors(self):
        return {
            "bg": "#E5EEE3",
            "panel": "#EDF4E9",
            "card": "#F8FAF5",
            "sidebar": "#A9C7B1",
            "sidebar_text": "#294B3B",
            "text": "#315642",
            "muted": "#789381",
            "primary": "#47775D",
            "secondary": "#A9C7B1",
            "accent": "#8CA875",
            "accent_light": "#D5E5D5",
            "border": "#C9DCC9"
        }

    def color(self, key):
        return self.colors.get(key, self.colors["text"])

    # ------------------------------------------------------
    # VARIABLES
    # ------------------------------------------------------

    def create_variables(self):

        stored_time = self.alarm.get("time", "07:00")

        try:
            parsed_time = datetime.strptime(
                stored_time.strip(),
                "%H:%M"
            )

            hour = parsed_time.strftime("%I")
            minute = parsed_time.strftime("%M")
            period = parsed_time.strftime("%p")

        except (ValueError, AttributeError):
            try:
                parsed_time = datetime.strptime(
                    stored_time.strip(),
                    "%I:%M %p"
                )

                hour = parsed_time.strftime("%I")
                minute = parsed_time.strftime("%M")
                period = parsed_time.strftime("%p")

            except (ValueError, AttributeError):
                hour, minute, period = "07", "00", "AM"

        self.hour_var = tk.StringVar(value=hour)
        self.minute_var = tk.StringVar(value=minute)
        self.period_var = tk.StringVar(value=period)

        self.label_var = tk.StringVar(
            value=self.alarm.get("label", "")
        )

        self.note_var = tk.StringVar(
            value=self.alarm.get("note", "")
        )

        self.enabled_var = tk.BooleanVar(
            value=self.alarm.get("enabled", True)
        )

        saved_days = self.alarm.get("repeat", [])

        self.day_vars = {
            day: tk.BooleanVar(value=day in saved_days)
            for day in self.DAYS
        }

    # ------------------------------------------------------
    # WINDOW POSITION
    # ------------------------------------------------------

    def center_window(self):

        self.window.update_idletasks()

        width = 460
        height = 680

        parent = self.parent.winfo_toplevel()

        x = parent.winfo_rootx() + (
            parent.winfo_width() - width
        ) // 2

        y = parent.winfo_rooty() + (
            parent.winfo_height() - height
        ) // 2

        self.window.geometry(
            f"{width}x{height}+{x}+{y}"
        )

    # ------------------------------------------------------
    # CUSTOM TITLE BAR
    # ------------------------------------------------------

    def create_title_bar(self):

        bar = tk.Frame(
            self.window,
            bg=self.color("sidebar"),
            height=38
        )

        bar.pack(fill="x")
        bar.pack_propagate(False)

        tk.Label(
            bar,
            text="ORIRI",
            font=("Georgia", 10, "bold"),
            fg=self.color("sidebar_text"),
            bg=self.color("sidebar")
        ).place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        close_button = tk.Button(
            bar,
            text="×",
            command=self.cancel,
            font=("Arial", 18),
            fg=self.color("sidebar_text"),
            bg=self.color("sidebar"),
            activebackground="#B96C70",
            activeforeground="#FFFFFF",
            relief="flat",
            bd=0,
            width=3,
            cursor="hand2"
        )

        close_button.pack(side="right", fill="y")

        close_button.bind(
            "<Enter>",
            lambda e: close_button.configure(
                bg="#B96C70",
                fg="#FFFFFF"
            )
        )

        close_button.bind(
            "<Leave>",
            lambda e: close_button.configure(
                bg=self.color("sidebar"),
                fg=self.color("sidebar_text")
            )
        )

        bar.bind("<Button-1>", self.start_drag)

        bar.bind("<B1-Motion>", self.drag_window)

        for child in bar.winfo_children():
            if isinstance(child, tk.Label):
                child.bind("<Button-1>", self.start_drag)
                child.bind("<B1-Motion>", self.drag_window)

    def start_drag(self, event):
        self.drag_x = event.x_root - self.window.winfo_x()
        self.drag_y = event.y_root - self.window.winfo_y()

    def drag_window(self, event):
        x = event.x_root - self.drag_x
        y = event.y_root - self.drag_y
        self.window.geometry(f"+{x}+{y}")

    # ------------------------------------------------------
    # UI HELPERS
    # ------------------------------------------------------

    def create_label(self, parent, text, **kwargs):

        return tk.Label(
            parent,
            text=text,
            font=kwargs.get("font", ("Arial", 9, "bold")),
            fg=kwargs.get("fg", self.color("text")),
            bg=kwargs.get("bg", self.color("bg")),
            anchor=kwargs.get("anchor", "w")
        )

    def create_entry(self, parent, variable, width=None):

        return tk.Entry(
            parent,
            textvariable=variable,
            font=("Arial", 10),
            fg=self.color("text"),
            bg=self.color("card"),
            insertbackground=self.color("primary"),
            relief="flat",
            bd=0,
            highlightthickness=1,
            highlightbackground=self.color("border"),
            highlightcolor=self.color("primary"),
            width=width
        )

    # ------------------------------------------------------
    # MAIN UI
    # ------------------------------------------------------

    def build_ui(self):

        self.create_title_bar()

        content = tk.Frame(
            self.window,
            bg=self.color("bg"),
            padx=32,
            pady=20
        )

        content.pack(fill="both", expand=True)

        # Heading
        self.create_label(
            content,
            "Create your alarm" if not self.alarm
            else "Edit your alarm",
            font=("Georgia", 22, "bold"),
            fg=self.color("primary")
        ).pack(anchor="w")

        self.create_label(
            content,
            "Choose a time and set your daily reminder.",
            font=("Arial", 9),
            fg=self.color("muted")
        ).pack(anchor="w", pady=(4, 20))

        # --------------------------------------------------
        # TIME SELECTOR
        # --------------------------------------------------

        self.create_label(
            content,
            "ALARM TIME"
        ).pack(anchor="w", pady=(0, 9))

        time_card = tk.Frame(
            content,
            bg=self.color("card"),
            padx=15,
            pady=15,
            highlightthickness=1,
            highlightbackground=self.color("border")
        )

        time_card.pack(fill="x", pady=(0, 18))

        time_row = tk.Frame(
            time_card,
            bg=self.color("card")
        )

        time_row.pack()

        self.hour_box = ttk.Combobox(
            time_row,
            textvariable=self.hour_var,
            values=[f"{i:02d}" for i in range(1, 13)],
            width=4,
            state="readonly",
            font=("Consolas", 22, "bold"),
            justify="center"
        )

        self.hour_box.pack(side="left", ipady=5)

        tk.Label(
            time_row,
            text=":",
            font=("Consolas", 22, "bold"),
            fg=self.color("primary"),
            bg=self.color("card")
        ).pack(side="left", padx=5)

        self.minute_box = ttk.Combobox(
            time_row,
            textvariable=self.minute_var,
            values=[f"{i:02d}" for i in range(60)],
            width=4,
            state="readonly",
            font=("Consolas", 22, "bold"),
            justify="center"
        )

        self.minute_box.pack(side="left", ipady=5)

        self.period_box = ttk.Combobox(
            time_row,
            textvariable=self.period_var,
            values=["AM", "PM"],
            width=5,
            state="readonly",
            font=("Arial", 13, "bold"),
            justify="center"
        )

        self.period_box.pack(
            side="left",
            padx=(12, 0),
            ipady=7
        )

        # --------------------------------------------------
        # ALARM LABEL
        # --------------------------------------------------

        self.create_label(
            content,
            "ALARM NAME"
        ).pack(anchor="w", pady=(0, 7))

        self.create_entry(
            content,
            self.label_var
        ).pack(fill="x", ipady=10, pady=(0, 16))

        # --------------------------------------------------
        # NOTE
        # --------------------------------------------------

        self.create_label(
            content,
            "NOTE (OPTIONAL)"
        ).pack(anchor="w", pady=(0, 7))

        self.create_entry(
            content,
            self.note_var
        ).pack(fill="x", ipady=10, pady=(0, 17))

        # --------------------------------------------------
        # REPEAT DAYS
        # --------------------------------------------------

        self.create_label(
            content,
            "REPEAT"
        ).pack(anchor="w", pady=(0, 9))

        days_frame = tk.Frame(
            content,
            bg=self.color("bg")
        )

        days_frame.pack(fill="x", pady=(0, 17))

        for index, day in enumerate(self.DAYS):

            day_button = tk.Checkbutton(
                days_frame,
                text=day,
                variable=self.day_vars[day],
                indicatoron=False,
                width=4,
                font=("Arial", 8, "bold"),
                fg=self.color("text"),
                bg=self.color("card"),
                selectcolor=self.color("accent_light"),
                activebackground=self.color("accent_light"),
                activeforeground=self.color("primary"),
                relief="flat",
                bd=0,
                padx=2,
                pady=8,
                cursor="hand2"
            )

            day_button.grid(
                row=0,
                column=index,
                padx=2,
                sticky="ew"
            )

            days_frame.grid_columnconfigure(
                index,
                weight=1
            )

        # --------------------------------------------------
        # ENABLE ALARM
        # --------------------------------------------------

        enabled_frame = tk.Frame(
            content,
            bg=self.color("panel"),
            padx=12,
            pady=10
        )

        enabled_frame.pack(fill="x", pady=(0, 20))

        tk.Checkbutton(
            enabled_frame,
            text="Enable this alarm",
            variable=self.enabled_var,
            font=("Arial", 9, "bold"),
            fg=self.color("text"),
            bg=self.color("panel"),
            activebackground=self.color("panel"),
            activeforeground=self.color("primary"),
            selectcolor=self.color("accent_light"),
            cursor="hand2"
        ).pack(anchor="w")

        # --------------------------------------------------
        # ACTION BUTTONS
        # --------------------------------------------------

        button_frame = tk.Frame(
            content,
            bg=self.color("bg")
        )

        button_frame.pack(fill="x", side="bottom")

        tk.Button(
            button_frame,
            text="Cancel",
            command=self.cancel,
            font=("Arial", 10, "bold"),
            fg=self.color("primary"),
            bg=self.color("accent_light"),
            activebackground=self.color("secondary"),
            relief="flat",
            cursor="hand2",
            pady=12
        ).pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 7)
        )

        tk.Button(
            button_frame,
            text="Save Alarm",
            command=self.save,
            font=("Arial", 10, "bold"),
            fg="#FFFFFF",
            bg=self.color("primary"),
            activebackground=self.color("sidebar_text"),
            activeforeground="#FFFFFF",
            relief="flat",
            cursor="hand2",
            pady=12
        ).pack(
            side="left",
            fill="x",
            expand=True,
            padx=(7, 0)
        )

    # ------------------------------------------------------
    # SAVE
    # ------------------------------------------------------

    def save(self):

        try:
            hour = int(self.hour_var.get())
            minute = int(self.minute_var.get())

            if not 1 <= hour <= 12:
                raise ValueError

            if not 0 <= minute <= 59:
                raise ValueError

        except (ValueError, TypeError):
            messagebox.showerror(
                "Invalid time",
                "Please select a valid alarm time.",
                parent=self.window
            )
            return

        # Convert 12-hour selection into 24-hour storage.
        # Example: 07:30 PM becomes 19:30.
        hour_24 = hour % 12

        if self.period_var.get() == "PM":
            hour_24 += 12

        stored_time = f"{hour_24:02d}:{minute:02d}"

        repeat_days = [
            day
            for day in self.DAYS
            if self.day_vars[day].get()
        ]

        alarm_data = {
            "time": stored_time,
            "label": self.label_var.get().strip() or "Your Alarm",
            "note": self.note_var.get().strip(),
            "repeat": repeat_days,
            "enabled": self.enabled_var.get()
        }

        # Preserve an existing alarm ID if one exists.
        if "id" in self.alarm:
            alarm_data["id"] = self.alarm["id"]

        if self.on_save:
            self.on_save(alarm_data)

        self.close()

    # ------------------------------------------------------
    # CANCEL / CLOSE
    # ------------------------------------------------------

    def cancel(self):

        if self.on_cancel:
            self.on_cancel()

        self.close()

    def close(self):

        try:
            self.window.grab_release()
        except tk.TclError:
            pass

        if self.window.winfo_exists():
            self.window.destroy()

