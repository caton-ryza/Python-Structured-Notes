
import tkinter as tk


# ==========================================================
# ORIRI — BUTTON COMPONENTS
# Botanical Glass Edition
# ==========================================================

DEFAULT_COLORS = {
    "bg": "#E5EEE3",
    "card": "#F8FAF5",
    "primary": "#47775D",
    "secondary": "#D5E5D5",
    "text": "#315642",
    "muted": "#789381",
    "border": "#C9DCC9",
    "accent": "#8CA875",
    "danger": "#B96F6F"
}


class OririButton(tk.Frame):

    def __init__(
        self,
        parent,
        text,
        command=None,
        style="primary",
        colors=None,
        width=None,
        **kwargs
    ):
        super().__init__(
            parent,
            bg=parent.cget("bg"),
            bd=0,
            highlightthickness=0
        )

        self.command = command
        self.colors = colors or DEFAULT_COLORS
        self.style = style

        self.normal, self.hover, self.foreground = (
            self.get_style_colors()
        )

        self.button = tk.Label(
            self,
            text=text,
            font=("Arial", 9, "bold"),
            bg=self.normal,
            fg=self.foreground,
            padx=18,
            pady=11,
            cursor="hand2",
            anchor="center",
            width=width
        )

        self.button.pack(fill="both", expand=True)

        self.bind_events(self.button)
        self.bind_events(self)

    def get_style_colors(self):

        if self.style == "primary":
            return (
                self.colors["primary"],
                self.colors.get("accent", "#8CA875"),
                "#FFFFFF"
            )

        if self.style == "secondary":
            return (
                self.colors["secondary"],
                self.colors.get("border", "#C9DCC9"),
                self.colors["text"]
            )

        if self.style == "subtle":
            return (
                self.colors["card"],
                self.colors["secondary"],
                self.colors["text"]
            )

        if self.style == "danger":
            return (
                self.colors.get("danger", "#B96F6F"),
                "#A85E5E",
                "#FFFFFF"
            )

        return (
            self.colors["primary"],
            self.colors["accent"],
            "#FFFFFF"
        )

    def bind_events(self, widget):

        widget.bind(
            "<Enter>",
            lambda event: self.on_hover(True)
        )

        widget.bind(
            "<Leave>",
            lambda event: self.on_hover(False)
        )

        widget.bind(
            "<Button-1>",
            lambda event: self.click()
        )

    def on_hover(self, hovering):

        color = self.hover if hovering else self.normal

        self.button.configure(bg=color)

    def click(self):

        if self.command:
            self.command()

    def set_text(self, text):
        self.button.configure(text=text)

    def set_enabled(self, enabled):

        if enabled:
            self.button.configure(
                fg=self.foreground,
                bg=self.normal,
                cursor="hand2"
            )
            self.command_enabled = True

        else:
            self.button.configure(
                fg=self.colors["muted"],
                bg=self.colors["secondary"],
                cursor="arrow"
            )
            self.command_enabled = False


# ==========================================================
# FACTORY FUNCTIONS
# ==========================================================

def primary_button(parent, text, command=None, colors=None):
    return OririButton(
        parent,
        text,
        command,
        "primary",
        colors
    )


def secondary_button(parent, text, command=None, colors=None):
    return OririButton(
        parent,
        text,
        command,
        "secondary",
        colors
    )


def subtle_button(parent, text, command=None, colors=None):
    return OririButton(
        parent,
        text,
        command,
        "subtle",
        colors
    )


def danger_button(parent, text, command=None, colors=None):
    return OririButton(
        parent,
        text,
        command,
        "danger",
        colors
    )
