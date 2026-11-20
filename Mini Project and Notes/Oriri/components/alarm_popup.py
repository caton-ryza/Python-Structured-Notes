
import tkinter as tk
from datetime import datetime


# ==========================================================
# ORIRI — ALARM POPUP
# Botanical Glass Edition
# ==========================================================

class AlarmPopup:

    def __init__(
        self,
        parent,
        alarm=None,
        colors=None,
        on_dismiss=None,
        on_snooze=None
    ):
        self.parent = parent
        self.alarm = alarm or {}
        self.colors = colors or self.default_colors()

        self.on_dismiss = on_dismiss
        self.on_snooze = on_snooze

        self.window = tk.Toplevel(parent)
        self.window.title("Oriri | Alarm")
        self.window.geometry("440x570")
        self.window.resizable(False, False)

        self.window.configure(bg=self.color("bg"))
        self.window.transient(parent.winfo_toplevel())

        self.window.protocol(
            "WM_DELETE_WINDOW",
            self.dismiss
        )

        self.build_ui()
        self.update_clock()

        self.window.lift()
        self.window.attributes("-topmost", True)
        self.window.after(
            1000,
            lambda: self.window.attributes("-topmost", False)
        )

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
        return self.colors.get(
            key,
            self.colors["text"]
        )

    # ------------------------------------------------------
    # MAIN UI
    # ------------------------------------------------------

    def build_ui(self):

        # Decorative top section
        header = tk.Frame(
            self.window,
            bg=self.color("primary"),
            height=180
        )
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="✿",
            font=("Georgia", 38),
            fg=self.color("accent_light"),
            bg=self.color("primary")
        ).pack(pady=(23, 0))

        tk.Label(
            header,
            text="TIME TO WAKE",
            font=("Arial", 9, "bold"),
            fg=self.color("accent_light"),
            bg=self.color("primary")
        ).pack(pady=(5, 0))

        # Main content
        content = tk.Frame(
            self.window,
            bg=self.color("bg"),
            padx=35,
            pady=24
        )
        content.pack(fill="both", expand=True)

        tk.Label(
            content,
            text="Good morning",
            font=("Georgia", 23, "bold"),
            fg=self.color("primary"),
            bg=self.color("bg")
        ).pack(pady=(0, 5))

        tk.Label(
            content,
            text=self.alarm.get("label", "Your Alarm"),
            font=("Arial", 12, "bold"),
            fg=self.color("text"),
            bg=self.color("bg")
        ).pack(pady=(0, 6))

        note = self.alarm.get("note", "").strip()

        if note:
            tk.Label(
                content,
                text=note,
                font=("Arial", 9),
                fg=self.color("muted"),
                bg=self.color("bg"),
                wraplength=320
            ).pack(pady=(0, 12))

        # Current time
        self.clock_label = tk.Label(
            content,
            text="",
            font=("Consolas", 35, "bold"),
            fg=self.color("primary"),
            bg=self.color("bg")
        )
        self.clock_label.pack(pady=(10, 20))

        # Snooze button
        tk.Button(
            content,
            text="Snooze  ·  5 minutes",
            font=("Arial", 10, "bold"),
            fg=self.color("primary"),
            bg=self.color("accent_light"),
            activebackground=self.color("secondary"),
            activeforeground=self.color("text"),
            relief="flat",
            cursor="hand2",
            pady=13,
            command=self.snooze
        ).pack(fill="x", pady=(0, 10))

        # Dismiss button
        tk.Button(
            content,
            text="Dismiss Alarm",
            font=("Arial", 10, "bold"),
            fg=self.color("card"),
            bg=self.color("primary"),
            activebackground=self.color("sidebar_text"),
            activeforeground=self.color("card"),
            relief="flat",
            cursor="hand2",
            pady=13,
            command=self.dismiss
        ).pack(fill="x")

        tk.Label(
            content,
            text="A quieter start to every day.",
            font=("Georgia", 9, "italic"),
            fg=self.color("muted"),
            bg=self.color("bg")
        ).pack(pady=(18, 0))

    # ------------------------------------------------------
    # CLOCK
    # ------------------------------------------------------

    def update_clock(self):

        if not self.window.winfo_exists():
            return

        current_time = datetime.now().strftime("%I:%M:%S %p")

        self.clock_label.config(
            text=current_time
        )

        self.window.after(
            1000,
            self.update_clock
        )

    # ------------------------------------------------------
    # SNOOZE
    # ------------------------------------------------------

    def snooze(self):

        if self.on_snooze:
            self.on_snooze(self.alarm)

        self.close()

    # ------------------------------------------------------
    # DISMISS
    # ------------------------------------------------------

    def dismiss(self):

        if self.on_dismiss:
            self.on_dismiss(self.alarm)

        self.close()

    # ------------------------------------------------------
    # CLOSE
    # ------------------------------------------------------

    def close(self):

        if self.window.winfo_exists():
            self.window.destroy()
