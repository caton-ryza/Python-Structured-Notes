import tkinter as tk


# ==========================================================
# ORIRI — CARD COMPONENTS
# Botanical Glass Edition
# ==========================================================

DEFAULT_COLORS = {
    "bg": "#E5EEE3",
    "panel": "#EDF4E9",
    "card": "#F8FAF5",
    "primary": "#315C43",
    "secondary": "#A9C7B1",
    "text": "#263F30",
    "muted": "#596F60",
    "border": "#B7CDB9",
    "accent": "#668C58",
    "accent_light": "#D5E5D5"
}


class OririCard(tk.Frame):

    def __init__(
        self,
        parent,
        colors=None,
        title=None,
        subtitle=None,
        padding=18,
        **kwargs
    ):
        self.colors = colors or DEFAULT_COLORS

        super().__init__(
            parent,
            bg=self.colors["card"],
            highlightbackground=self.colors["border"],
            highlightthickness=1,
            bd=0,
            **kwargs
        )

        self.padding = padding

        self.content = tk.Frame(
            self,
            bg=self.colors["card"]
        )
        self.content.pack(
            fill="both",
            expand=True,
            padx=padding,
            pady=padding
        )

        if title or subtitle:
            self.build_heading(title, subtitle)

        self.body = tk.Frame(
            self.content,
            bg=self.colors["card"]
        )
        self.body.pack(
            fill="both",
            expand=True
        )

    def build_heading(self, title, subtitle):

        heading = tk.Frame(
            self.content,
            bg=self.colors["card"]
        )
        heading.pack(fill="x", pady=(0, 15))

        if title:
            tk.Label(
                heading,
                text=title,
                font=("Arial", 11, "bold"),
                fg=self.colors["text"],
                bg=self.colors["card"]
            ).pack(anchor="w")

        if subtitle:
            tk.Label(
                heading,
                text=subtitle,
                font=("Arial", 8),
                fg=self.colors["muted"],
                bg=self.colors["card"]
            ).pack(anchor="w", pady=(4, 0))

    def get_body(self):
        return self.body


# ==========================================================
# STAT CARD
# ==========================================================

class StatCard(OririCard):

    def __init__(
        self,
        parent,
        label,
        value,
        description=None,
        colors=None
    ):
        super().__init__(
            parent,
            colors=colors,
            padding=17
        )

        self.label = tk.Label(
            self.body,
            text=label.upper(),
            font=("Arial", 9, "bold"),
            fg=self.colors["muted"],
            bg=self.colors["card"]
        )
        self.label.pack(anchor="w")

        self.value_label = tk.Label(
            self.body,
            text=value,
            font=("Georgia", 25, "bold"),
            fg=self.colors["primary"],
            bg=self.colors["card"]
        )
        self.value_label.pack(
            anchor="w",
            pady=(7, 3)
        )

        self.description_label = tk.Label(
            self.body,
            text=description or "",
            font=("Arial", 9),
            fg=self.colors["muted"],
            bg=self.colors["card"]
        )
        self.description_label.pack(anchor="w")

    def update_value(self, value):
        self.value_label.configure(text=value)

    def update_description(self, description):
        self.description_label.configure(text=description)


# ==========================================================
# ALARM CARD
# ==========================================================

class AlarmCard(OririCard):

    def __init__(
        self,
        parent,
        time,
        label,
        repeat=None,
        note=None,
        enabled=True,
        colors=None
    ):
        super().__init__(
            parent,
            colors=colors,
            padding=17
        )

        self.repeat = repeat or []
        self.enabled = enabled

        # Convert 24-hour time into 12-hour format with AM/PM
        display_time = self.format_time(time)

        self.time_label = tk.Label(
            self.body,
            text=display_time,
            font=("Consolas", 23, "bold"),
            fg=self.colors["primary"],
            bg=self.colors["card"]
        )
        self.time_label.pack(anchor="w")

        self.name_label = tk.Label(
            self.body,
            text=label,
            font=("Arial", 11, "bold"),
            fg=self.colors["text"],
            bg=self.colors["card"]
        )
        self.name_label.pack(
            anchor="w",
            pady=(5, 3)
        )

        repeat_text = (
            " · ".join(self.repeat)
            if self.repeat
            else "No repeat"
        )

        self.repeat_label = tk.Label(
            self.body,
            text=repeat_text,
            font=("Arial", 9),
            fg=self.colors["muted"],
            bg=self.colors["card"]
        )
        self.repeat_label.pack(anchor="w")

        if note:
            tk.Label(
                self.body,
                text=note,
                font=("Arial", 9),
                fg=self.colors["muted"],
                bg=self.colors["card"],
                wraplength=260,
                justify="left"
            ).pack(
                anchor="w",
                pady=(9, 0)
            )

    @staticmethod
    def format_time(time):
        try:
            from datetime import datetime

            parsed_time = datetime.strptime(time, "%H:%M")
            return parsed_time.strftime("%I:%M %p")

        except (ValueError, TypeError):
            return time

    def update_time(self, time):
        self.time_label.configure(
            text=self.format_time(time)
        )

    def update_name(self, name):
        self.name_label.configure(text=name)


# ==========================================================
# SECTION CARD
# ==========================================================

class SectionCard(OririCard):

    def __init__(
        self,
        parent,
        title,
        subtitle=None,
        colors=None,
        padding=20
    ):
        super().__init__(
            parent,
            colors=colors,
            title=title,
            subtitle=subtitle,
            padding=padding
        )
