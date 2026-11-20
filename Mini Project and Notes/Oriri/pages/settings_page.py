
import tkinter as tk
from tkinter import messagebox
import json
import os


# ==========================================================
# ORIRI — SETTINGS
# Botanical Glass Edition
# ==========================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
SETTINGS_FILE = os.path.join(DATA_DIR, "settings.json")
ALARM_FILE = os.path.join(DATA_DIR, "alarms.json")

DEFAULT_SETTINGS = {
    "time_format": "12-hour",
    "sound_enabled": True,
    "notifications_enabled": True,
    "default_enabled": True,
    "default_sound": "",
    "volume": 75
}


def load_settings():
    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(SETTINGS_FILE):
        return DEFAULT_SETTINGS.copy()

    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            return DEFAULT_SETTINGS.copy()

        settings = DEFAULT_SETTINGS.copy()
        settings.update(data)
        return settings

    except (json.JSONDecodeError, OSError):
        return DEFAULT_SETTINGS.copy()


def save_settings(settings):
    os.makedirs(DATA_DIR, exist_ok=True)

    with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
        json.dump(settings, file, indent=4)


# ==========================================================
# SETTINGS PAGE
# ==========================================================

class SettingsPage(tk.Frame):

    def __init__(self, parent, app=None):
        self.app = app

        self.C = app.theme if app else {
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

        self.settings = load_settings()
        self.sound_items = sound_manager.get_available_sounds()

        super().__init__(parent, bg=self.C["bg"])

        self.build_page()

    # ------------------------------------------------------
    # HELPERS
    # ------------------------------------------------------

    def color(self, key):
        return self.C.get(key, self.C["text"])

    def label(self, parent, text, font=("Arial", 10),
              fg=None, bg=None, **kwargs):

        return tk.Label(
            parent,
            text=text,
            font=font,
            fg=fg or self.color("text"),
            bg=bg or self.color("bg"),
            **kwargs
        )

    def section_card(self, parent):
        return tk.Frame(
            parent,
            bg=self.color("card"),
            highlightbackground=self.color("border"),
            highlightthickness=1,
            padx=20,
            pady=18
        )

    def section_heading(self, parent, title, subtitle):
        heading = tk.Frame(parent, bg=self.color("bg"))
        heading.pack(fill="x", pady=(0, 11))

        self.label(
            heading,
            title,
            font=("Georgia", 16, "bold")
        ).pack(anchor="w")

        self.label(
            heading,
            subtitle,
            font=("Arial", 9),
            fg=self.color("muted")
        ).pack(anchor="w", pady=(3, 0))

    def styled_button(self, parent, text, command, primary=False):
        return tk.Button(
            parent,
            text=text,
            font=("Arial", 9, "bold"),
            bg=self.color("primary") if primary else self.color("accent_light"),
            fg="#FFFFFF" if primary else self.color("text"),
            activebackground=self.color("secondary"),
            activeforeground=self.color("text"),
            relief="flat",
            bd=0,
            padx=15,
            pady=9,
            cursor="hand2",
            command=command
        )

    # ------------------------------------------------------
    # PAGE LAYOUT WITH SCROLLING
    # ------------------------------------------------------

    def build_page(self):

        self.scroll_area = ScrollableFrame(
            self,
            colors=self.C
        )

        self.scroll_area.pack(
            fill="both",
            expand=True
        )

        self.container = self.scroll_area.get_frame()

        self.container.configure(bg=self.color("bg"))

        self.container.pack_propagate(True)

        self.build_header()
        self.build_appearance()
        self.build_alarm_preferences()
        self.build_notifications()
        self.build_sound_settings()
        self.build_data_section()
        self.build_about()

    # ------------------------------------------------------
    # HEADER
    # ------------------------------------------------------

    def build_header(self):

        header = tk.Frame(
            self.container,
            bg=self.color("bg")
        )
        header.pack(fill="x", padx=35, pady=(28, 25))

        self.label(
            header,
            "PERSONALIZE YOUR EXPERIENCE",
            font=("Arial", 9, "bold"),
            fg=self.color("primary")
        ).pack(anchor="w")

        self.label(
            header,
            "Settings",
            font=("Georgia", 29, "bold")
        ).pack(anchor="w", pady=(5, 3))

        self.label(
            header,
            "Make Oriri feel a little more like yours.",
            font=("Arial", 10),
            fg=self.color("muted")
        ).pack(anchor="w")

    # ------------------------------------------------------
    # APPEARANCE
    # ------------------------------------------------------

    def build_appearance(self):

        self.section_heading(
            self.container,
            "Appearance",
            "Choose how your personal space looks."
        )

        card = self.section_card(self.container)
        card.pack(fill="x", padx=35, pady=(0, 23))

        current_theme = (
            self.app.selected_theme
            if self.app else "Meadow"
        )

        left = tk.Frame(card, bg=self.color("card"))
        left.pack(side="left", fill="x", expand=True)

        self.label(
            left,
            "Current theme",
            font=("Arial", 10, "bold"),
            bg=self.color("card")
        ).pack(anchor="w")

        self.label(
            left,
            current_theme,
            font=("Georgia", 17, "bold"),
            fg=self.color("primary"),
            bg=self.color("card")
        ).pack(anchor="w", pady=(5, 3))

        self.label(
            left,
            "Your selected palette is applied throughout Oriri.",
            font=("Arial", 9),
            fg=self.color("muted"),
            bg=self.color("card")
        ).pack(anchor="w")

        preview = tk.Frame(
            card,
            bg=self.color("panel"),
            padx=12,
            pady=10
        )
        preview.pack(side="right", padx=(15, 0))

        for shade in [
            self.color("primary"),
            self.color("secondary"),
            self.color("accent"),
            self.color("flower")
        ]:
            tk.Frame(
                preview,
                bg=shade,
                width=23,
                height=23
            ).pack(side="left", padx=3)

    # ------------------------------------------------------
    # ALARM PREFERENCES
    # ------------------------------------------------------

    def build_alarm_preferences(self):

        self.section_heading(
            self.container,
            "Alarm preferences",
            "Set your preferred time display and default behavior."
        )

        card = self.section_card(self.container)
        card.pack(fill="x", padx=35, pady=(0, 23))

        time_row = tk.Frame(card, bg=self.color("card"))
        time_row.pack(fill="x", pady=(0, 16))

        time_info = tk.Frame(time_row, bg=self.color("card"))
        time_info.pack(side="left", fill="x", expand=True)

        self.label(
            time_info,
            "Clock format",
            font=("Arial", 10, "bold"),
            bg=self.color("card")
        ).pack(anchor="w")

        self.label(
            time_info,
            "Choose how alarm times are displayed.",
            font=("Arial", 9),
            fg=self.color("muted"),
            bg=self.color("card")
        ).pack(anchor="w", pady=(3, 0))

        self.time_var = tk.StringVar(
            value=self.settings.get("time_format", "12-hour")
        )

        time_options = tk.Frame(time_row, bg=self.color("card"))
        time_options.pack(side="right")

        for value, text in [
            ("12-hour", "12-hour"),
            ("24-hour", "24-hour")
        ]:
            tk.Radiobutton(
                time_options,
                text=text,
                value=value,
                variable=self.time_var,
                font=("Arial", 9),
                fg=self.color("text"),
                bg=self.color("card"),
                activebackground=self.color("card"),
                selectcolor=self.color("accent_light"),
                command=self.save_preferences
            ).pack(side="left", padx=5)

        tk.Frame(
            card,
            bg=self.color("border"),
            height=1
        ).pack(fill="x", pady=(0, 15))

        self.default_var = tk.BooleanVar(
            value=self.settings.get("default_enabled", True)
        )

        self.setting_row(
            card,
            "Enable new alarms by default",
            "New alarms will be active immediately after saving.",
            self.default_var
        )

    # ------------------------------------------------------
    # NOTIFICATIONS
    # ------------------------------------------------------

    def build_notifications(self):

        self.section_heading(
            self.container,
            "Notifications",
            "Manage your reminder preferences."
        )

        card = self.section_card(self.container)
        card.pack(fill="x", padx=35, pady=(0, 23))

        self.sound_var = tk.BooleanVar(
            value=self.settings.get("sound_enabled", True)
        )

        self.setting_row(
            card,
            "Alarm sound",
            "Allow alarm sounds when an alarm is triggered.",
            self.sound_var
        )

        tk.Frame(
            card,
            bg=self.color("border"),
            height=1
        ).pack(fill="x", pady=14)

        self.notification_var = tk.BooleanVar(
            value=self.settings.get("notifications_enabled", True)
        )

        self.setting_row(
            card,
            "Notifications",
            "Allow reminder notifications from Oriri.",
            self.notification_var
        )

    # ------------------------------------------------------
    # SOUND SETTINGS
    # ------------------------------------------------------

    def build_sound_settings(self):

        self.section_heading(
            self.container,
            "Sound library",
            "Choose the sound you want Oriri to use by default."
        )

        card = self.section_card(self.container)
        card.pack(fill="x", padx=35, pady=(0, 23))

        self.label(
            card,
            "Default alarm sound",
            font=("Arial", 10, "bold"),
            bg=self.color("card")
        ).pack(anchor="w")

        self.label(
            card,
            "Preview different sounds before choosing one.",
            font=("Arial", 9),
            fg=self.color("muted"),
            bg=self.color("card")
        ).pack(anchor="w", pady=(3, 12))

        self.sound_map = {}

        for sound in self.sound_items:
            display_name = sound["name"]
            self.sound_map[display_name] = sound["id"]

        saved_sound = self.settings.get("default_sound", "")

        selected_name = "No sounds found"

        for name, sound_id in self.sound_map.items():
            if sound_id == saved_sound:
                selected_name = name
                break

        if self.sound_map and selected_name == "No sounds found":
            selected_name = next(iter(self.sound_map))

        self.selected_sound_var = tk.StringVar(
            value=selected_name
        )

        self.sound_menu = tk.OptionMenu(
            card,
            self.selected_sound_var,
            *self.sound_map.keys() if self.sound_map else ["No sounds found"],
            command=lambda _: self.save_preferences()
        )

        self.sound_menu.configure(
            font=("Arial", 10),
            bg=self.color("accent_light"),
            fg=self.color("text"),
            activebackground=self.color("secondary"),
            relief="flat",
            bd=0,
            highlightthickness=0,
            padx=10,
            pady=7
        )

        self.sound_menu["menu"].configure(
            bg=self.color("card"),
            fg=self.color("text"),
            activebackground=self.color("accent_light"),
            font=("Arial", 9)
        )

        self.sound_menu.pack(anchor="w", fill="x")

        button_row = tk.Frame(card, bg=self.color("card"))
        button_row.pack(fill="x", pady=(13, 17))

        self.styled_button(
            button_row,
            "▶  Preview",
            self.preview_sound
        ).pack(side="left", padx=(0, 8))

        self.styled_button(
            button_row,
            "■  Stop",
            self.stop_sound
        ).pack(side="left")

        self.sound_status = self.label(
            card,
            "Choose a sound to preview it.",
            font=("Arial", 9),
            fg=self.color("muted"),
            bg=self.color("card")
        )
        self.sound_status.pack(anchor="w", pady=(0, 15))

        tk.Frame(
            card,
            bg=self.color("border"),
            height=1
        ).pack(fill="x", pady=(0, 15))

        self.label(
            card,
            "Alarm volume",
            font=("Arial", 10, "bold"),
            bg=self.color("card")
        ).pack(anchor="w")

        self.volume_var = tk.IntVar(
            value=int(self.settings.get("volume", 75))
        )

        self.volume_scale = tk.Scale(
            card,
            from_=0,
            to=100,
            orient="horizontal",
            variable=self.volume_var,
            showvalue=True,
            resolution=1,
            bg=self.color("card"),
            fg=self.color("text"),
            troughcolor=self.color("accent_light"),
            activebackground=self.color("primary"),
            highlightthickness=0,
            bd=0,
            font=("Arial", 9),
            command=self.change_volume
        )

        self.volume_scale.pack(fill="x", pady=(5, 12))

        self.styled_button(
            card,
            "Save sound settings",
            self.save_preferences,
            primary=True
        ).pack(anchor="e")

        if not self.sound_items:
            self.sound_status.configure(
                text="No audio files found. Add WAV, OGG, or MP3 files to assets/sounds."
            )

    def preview_sound(self):

        if not self.sound_map:
            messagebox.showwarning(
                "No Sounds Available",
                "Add audio files to your assets/sounds folder first.",
                parent=self
            )
            return

        sound_name = self.selected_sound_var.get()
        sound_id = self.sound_map.get(sound_name)

        if not sound_id:
            return

        try:
            sound_manager.set_volume(self.volume_var.get() / 100)
            sound_manager.preview(sound_id)

            self.sound_status.configure(
                text=f"Previewing: {sound_name}"
            )

        except Exception as error:
            messagebox.showerror(
                "Sound Error",
                str(error),
                parent=self
            )

    def stop_sound(self):

        sound_manager.stop()

        self.sound_status.configure(
            text="Sound preview stopped."
        )

    def change_volume(self, value):

        volume = float(value) / 100
        sound_manager.set_volume(volume)

    # ------------------------------------------------------
    # REUSABLE SETTING ROW
    # ------------------------------------------------------

    def setting_row(self, parent, title, description, variable):

        row = tk.Frame(parent, bg=self.color("card"))
        row.pack(fill="x")

        info = tk.Frame(row, bg=self.color("card"))
        info.pack(side="left", fill="x", expand=True)

        self.label(
            info,
            title,
            font=("Arial", 10, "bold"),
            bg=self.color("card")
        ).pack(anchor="w")

        self.label(
            info,
            description,
            font=("Arial", 9),
            fg=self.color("muted"),
            bg=self.color("card")
        ).pack(anchor="w", pady=(3, 0))

        tk.Checkbutton(
            row,
            variable=variable,
            command=self.save_preferences,
            bg=self.color("card"),
            activebackground=self.color("card"),
            selectcolor=self.color("accent_light"),
            fg=self.color("primary"),
            cursor="hand2"
        ).pack(side="right", padx=(10, 0))

    # ------------------------------------------------------
    # DATA MANAGEMENT
    # ------------------------------------------------------

    def build_data_section(self):

        self.section_heading(
            self.container,
            "Data management",
            "Manage your locally saved alarm information."
        )

        card = self.section_card(self.container)
        card.pack(fill="x", padx=35, pady=(0, 23))

        info = tk.Frame(card, bg=self.color("card"))
        info.pack(side="left", fill="x", expand=True)

        self.label(
            info,
            "Clear saved alarms",
            font=("Arial", 10, "bold"),
            bg=self.color("card")
        ).pack(anchor="w")

        self.label(
            info,
            "Remove all alarms saved on this device.",
            font=("Arial", 9),
            fg=self.color("muted"),
            bg=self.color("card")
        ).pack(anchor="w", pady=(3, 0))

        self.styled_button(
            card,
            "Clear alarms",
            self.clear_alarms
        ).pack(side="right")

    def clear_alarms(self):

        confirmed = messagebox.askyesno(
            "Clear All Alarms",
            "Are you sure you want to delete all saved alarms?\n\nThis action cannot be undone.",
            parent=self
        )

        if not confirmed:
            return

        try:
            with open(ALARM_FILE, "w", encoding="utf-8") as file:
                json.dump([], file, indent=4)

            messagebox.showinfo(
                "Alarms Cleared",
                "All saved alarms have been cleared.",
                parent=self
            )

        except OSError as error:
            messagebox.showerror(
                "Error",
                f"Could not clear alarms:\n{error}",
                parent=self
            )

    # ------------------------------------------------------
    # ABOUT
    # ------------------------------------------------------

    def build_about(self):

        card = tk.Frame(
            self.container,
            bg=self.color("panel"),
            highlightbackground=self.color("border"),
            highlightthickness=1,
            padx=20,
            pady=18
        )

        card.pack(fill="x", padx=35, pady=(0, 35))

        self.label(
            card,
            "✿  ORIRI",
            font=("Georgia", 17, "bold"),
            fg=self.color("primary"),
            bg=self.color("panel")
        ).pack(anchor="w")

        self.label(
            card,
            "A quieter start to every day.",
            font=("Arial", 9, "italic"),
            fg=self.color("muted"),
            bg=self.color("panel")
        ).pack(anchor="w", pady=(4, 8))

        self.label(
            card,
            "Version 1.0  •  Botanical Garden Edition",
            font=("Arial", 8),
            fg=self.color("muted"),
            bg=self.color("panel")
        ).pack(anchor="w")

    # ------------------------------------------------------
    # SAVE PREFERENCES
    # ------------------------------------------------------

    def save_preferences(self):

        self.settings["time_format"] = self.time_var.get()
        self.settings["default_enabled"] = self.default_var.get()
        self.settings["sound_enabled"] = self.sound_var.get()
        self.settings["notifications_enabled"] = self.notification_var.get()

        self.settings["volume"] = self.volume_var.get()

        selected_name = self.selected_sound_var.get()
        self.settings["default_sound"] = self.sound_map.get(
            selected_name,
            self.settings.get("default_sound", "")
        )

        sound_manager.set_volume(
            self.volume_var.get() / 100
        )

        try:
            save_settings(self.settings)
        except OSError as error:
            messagebox.showerror(
                "Settings Error",
                f"Could not save settings:\n{error}",
                parent=self
            )

    def destroy(self):
        try:
            sound_manager.stop()
        except Exception:
            pass

        super().destroy()


# ==========================================================
# END OF SETTINGS PAGE
# ==========================================================

import tkinter as tk
from tkinter import messagebox
import json
import os

from modules.sound_manager import sound_manager


# ==========================================================
# ORIRI — SETTINGS
# BOTANICAL GLASS EDITION
# ==========================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
SETTINGS_FILE = os.path.join(DATA_DIR, "settings.json")
ALARM_FILE = os.path.join(DATA_DIR, "alarms.json")


DEFAULT_SETTINGS = {
    "time_format": "12-hour",
    "sound_enabled": True,
    "notifications_enabled": True,
    "default_enabled": True,
    "default_sound": "",
    "volume": 75
}


# ==========================================================
# SETTINGS STORAGE
# ==========================================================

def load_settings():

    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(SETTINGS_FILE):
        return DEFAULT_SETTINGS.copy()

    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            return DEFAULT_SETTINGS.copy()

        settings = DEFAULT_SETTINGS.copy()
        settings.update(data)

        return settings

    except (json.JSONDecodeError, OSError):
        return DEFAULT_SETTINGS.copy()


def save_settings(settings):

    os.makedirs(DATA_DIR, exist_ok=True)

    with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
        json.dump(settings, file, indent=4)


# ==========================================================
# SETTINGS PAGE
# ==========================================================

class SettingsPage(tk.Frame):

    def __init__(self, parent, app=None):

        self.app = app

        self.C = app.theme if app else {
            "bg": "#EAF1E8",
            "panel": "#F1F6EF",
            "card": "#F8FAF5",
            "sidebar": "#315B49",
            "sidebar_light": "#71947D",
            "sidebar_active": "#D5E5D5",
            "sidebar_text": "#F8FAF5",
            "text": "#315642",
            "muted": "#789381",
            "primary": "#47775D",
            "secondary": "#A9C7B1",
            "accent": "#8CA875",
            "accent_light": "#D5E5D5",
            "border": "#C9DCC9",
            "flower": "#E5C6A4"
        }

        self.settings = load_settings()

        try:
            self.sound_items = sound_manager.get_available_sounds()
        except Exception:
            self.sound_items = []

        super().__init__(
            parent,
            bg=self.C["bg"]
        )

        self.build_page()

    # ======================================================
    # HELPERS
    # ======================================================

    def color(self, key):

        return self.C.get(
            key,
            self.C["text"]
        )

    def label(
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

    def section_card(self, parent):

        return tk.Frame(
            parent,
            bg=self.color("card"),
            highlightbackground=self.color("border"),
            highlightthickness=1,
            padx=20,
            pady=18
        )

    def section_heading(self, parent, title, subtitle):

        heading = tk.Frame(
            parent,
            bg=self.color("bg")
        )

        heading.pack(
            fill="x",
            padx=35,
            pady=(0, 11)
        )

        self.label(
            heading,
            title,
            font=("Georgia", 16, "bold")
        ).pack(anchor="w")

        self.label(
            heading,
            subtitle,
            font=("Arial", 9),
            fg=self.color("muted")
        ).pack(
            anchor="w",
            pady=(3, 0)
        )

    def styled_button(
        self,
        parent,
        text,
        command,
        primary=False
    ):

        return tk.Button(
            parent,
            text=text,
            font=("Arial", 9, "bold"),
            bg=(
                self.color("primary")
                if primary
                else self.color("accent_light")
            ),
            fg=(
                "#FFFFFF"
                if primary
                else self.color("text")
            ),
            activebackground=self.color("secondary"),
            activeforeground=self.color("text"),
            relief="flat",
            bd=0,
            padx=15,
            pady=9,
            cursor="hand2",
            command=command
        )

    # ======================================================
    # PAGE LAYOUT
    # Main.py handles scrolling for this entire page.
    # ======================================================

    def build_page(self):

        self.container = self

        self.build_header()
        self.build_appearance()
        self.build_alarm_preferences()
        self.build_notifications()
        self.build_sound_settings()
        self.build_data_section()
        self.build_about()

    # ======================================================
    # HEADER
    # ======================================================

    def build_header(self):

        header = tk.Frame(
            self.container,
            bg=self.color("bg")
        )

        header.pack(
            fill="x",
            padx=35,
            pady=(28, 25)
        )

        self.label(
            header,
            "PERSONALIZE YOUR EXPERIENCE",
            font=("Arial", 9, "bold"),
            fg=self.color("primary")
        ).pack(anchor="w")

        self.label(
            header,
            "Settings",
            font=("Georgia", 29, "bold")
        ).pack(
            anchor="w",
            pady=(5, 3)
        )

        self.label(
            header,
            "Make Oriri feel a little more like yours.",
            font=("Arial", 10),
            fg=self.color("muted")
        ).pack(anchor="w")

    # ======================================================
    # APPEARANCE
    # ======================================================

    def build_appearance(self):

        self.section_heading(
            self.container,
            "Appearance",
            "Choose how your personal space looks."
        )

        card = self.section_card(self.container)

        card.pack(
            fill="x",
            padx=35,
            pady=(0, 23)
        )

        current_theme = (
            self.app.selected_theme
            if self.app
            else "Meadow"
        )

        left = tk.Frame(
            card,
            bg=self.color("card")
        )

        left.pack(
            side="left",
            fill="x",
            expand=True
        )

        self.label(
            left,
            "Current theme",
            font=("Arial", 10, "bold"),
            bg=self.color("card")
        ).pack(anchor="w")

        self.label(
            left,
            current_theme,
            font=("Georgia", 17, "bold"),
            fg=self.color("primary"),
            bg=self.color("card")
        ).pack(
            anchor="w",
            pady=(5, 3)
        )

        self.label(
            left,
            "Your selected palette is applied throughout Oriri.",
            font=("Arial", 9),
            fg=self.color("muted"),
            bg=self.color("card")
        ).pack(anchor="w")

        preview = tk.Frame(
            card,
            bg=self.color("panel"),
            padx=12,
            pady=10
        )

        preview.pack(
            side="right",
            padx=(15, 0)
        )

        for shade in [
            self.color("primary"),
            self.color("secondary"),
            self.color("accent"),
            self.color("flower")
        ]:

            tk.Frame(
                preview,
                bg=shade,
                width=23,
                height=23
            ).pack(
                side="left",
                padx=3
            )

    # ======================================================
    # ALARM PREFERENCES
    # ======================================================

    def build_alarm_preferences(self):

        self.section_heading(
            self.container,
            "Alarm preferences",
            "Set your preferred time display and default behavior."
        )

        card = self.section_card(self.container)

        card.pack(
            fill="x",
            padx=35,
            pady=(0, 23)
        )

        time_row = tk.Frame(
            card,
            bg=self.color("card")
        )

        time_row.pack(
            fill="x",
            pady=(0, 16)
        )

        time_info = tk.Frame(
            time_row,
            bg=self.color("card")
        )

        time_info.pack(
            side="left",
            fill="x",
            expand=True
        )

        self.label(
            time_info,
            "Clock format",
            font=("Arial", 10, "bold"),
            bg=self.color("card")
        ).pack(anchor="w")

        self.label(
            time_info,
            "Choose how alarm times are displayed.",
            font=("Arial", 9),
            fg=self.color("muted"),
            bg=self.color("card")
        ).pack(
            anchor="w",
            pady=(3, 0)
        )

        self.time_var = tk.StringVar(
            value=self.settings.get(
                "time_format",
                "12-hour"
            )
        )

        time_options = tk.Frame(
            time_row,
            bg=self.color("card")
        )

        time_options.pack(side="right")

        for value, text in [
            ("12-hour", "12-hour"),
            ("24-hour", "24-hour")
        ]:

            tk.Radiobutton(
                time_options,
                text=text,
                value=value,
                variable=self.time_var,
                font=("Arial", 9),
                fg=self.color("text"),
                bg=self.color("card"),
                activebackground=self.color("card"),
                selectcolor=self.color("accent_light"),
                command=self.save_preferences
            ).pack(
                side="left",
                padx=5
            )

        tk.Frame(
            card,
            bg=self.color("border"),
            height=1
        ).pack(
            fill="x",
            pady=(0, 15)
        )

        self.default_var = tk.BooleanVar(
            value=self.settings.get(
                "default_enabled",
                True
            )
        )

        self.setting_row(
            card,
            "Enable new alarms by default",
            "New alarms will be active immediately after saving.",
            self.default_var
        )

    # ======================================================
    # NOTIFICATIONS
    # ======================================================

    def build_notifications(self):

        self.section_heading(
            self.container,
            "Notifications",
            "Manage your reminder preferences."
        )

        card = self.section_card(self.container)

        card.pack(
            fill="x",
            padx=35,
            pady=(0, 23)
        )

        self.sound_var = tk.BooleanVar(
            value=self.settings.get(
                "sound_enabled",
                True
            )
        )

        self.setting_row(
            card,
            "Alarm sound",
            "Allow alarm sounds when an alarm is triggered.",
            self.sound_var
        )

        tk.Frame(
            card,
            bg=self.color("border"),
            height=1
        ).pack(
            fill="x",
            pady=14
        )

        self.notification_var = tk.BooleanVar(
            value=self.settings.get(
                "notifications_enabled",
                True
            )
        )

        self.setting_row(
            card,
            "Notifications",
            "Allow reminder notifications from Oriri.",
            self.notification_var
        )

    # ======================================================
    # SOUND SETTINGS
    # ======================================================

    def build_sound_settings(self):

        self.section_heading(
            self.container,
            "Sound library",
            "Choose the sound you want Oriri to use by default."
        )

        card = self.section_card(self.container)

        card.pack(
            fill="x",
            padx=35,
            pady=(0, 23)
        )

        self.label(
            card,
            "Default alarm sound",
            font=("Arial", 10, "bold"),
            bg=self.color("card")
        ).pack(anchor="w")

        self.label(
            card,
            "Preview different sounds before choosing one.",
            font=("Arial", 9),
            fg=self.color("muted"),
            bg=self.color("card")
        ).pack(
            anchor="w",
            pady=(3, 12)
        )

        self.sound_map = {}

        for sound in self.sound_items:

            display_name = sound["name"]
            self.sound_map[display_name] = sound["id"]

        saved_sound = self.settings.get(
            "default_sound",
            ""
        )

        selected_name = ""

        for name, sound_id in self.sound_map.items():

            if sound_id == saved_sound:
                selected_name = name
                break

        if not selected_name and self.sound_map:
            selected_name = next(iter(self.sound_map))

        if not selected_name:
            selected_name = "No sounds found"

        self.selected_sound_var = tk.StringVar(
            value=selected_name
        )

        sound_options = (
            list(self.sound_map.keys())
            if self.sound_map
            else ["No sounds found"]
        )

        self.sound_menu = tk.OptionMenu(
            card,
            self.selected_sound_var,
            *sound_options
        )

        self.sound_menu.configure(
            font=("Arial", 10),
            bg=self.color("accent_light"),
            fg=self.color("text"),
            activebackground=self.color("secondary"),
            relief="flat",
            bd=0,
            highlightthickness=0,
            padx=10,
            pady=7
        )

        self.sound_menu["menu"].configure(
            bg=self.color("card"),
            fg=self.color("text"),
            activebackground=self.color("accent_light"),
            font=("Arial", 9)
        )

        self.sound_menu.pack(
            anchor="w",
            fill="x"
        )

        button_row = tk.Frame(
            card,
            bg=self.color("card")
        )

        button_row.pack(
            fill="x",
            pady=(13, 17)
        )

        self.styled_button(
            button_row,
            "▶  Preview",
            self.preview_sound
        ).pack(
            side="left",
            padx=(0, 8)
        )

        self.styled_button(
            button_row,
            "■  Stop",
            self.stop_sound
        ).pack(side="left")

        self.sound_status = self.label(
            card,
            "Choose a sound to preview it.",
            font=("Arial", 9),
            fg=self.color("muted"),
            bg=self.color("card")
        )

        self.sound_status.pack(
            anchor="w",
            pady=(0, 15)
        )

        tk.Frame(
            card,
            bg=self.color("border"),
            height=1
        ).pack(
            fill="x",
            pady=(0, 15)
        )

        self.label(
            card,
            "Alarm volume",
            font=("Arial", 10, "bold"),
            bg=self.color("card")
        ).pack(anchor="w")

        self.volume_var = tk.IntVar(
            value=int(self.settings.get("volume", 75))
        )

        self.volume_scale = tk.Scale(
            card,
            from_=0,
            to=100,
            orient="horizontal",
            variable=self.volume_var,
            showvalue=True,
            resolution=1,
            bg=self.color("card"),
            fg=self.color("text"),
            troughcolor=self.color("accent_light"),
            activebackground=self.color("primary"),
            highlightthickness=0,
            bd=0,
            font=("Arial", 9),
            command=self.change_volume
        )

        self.volume_scale.pack(
            fill="x",
            pady=(5, 12)
        )

        self.styled_button(
            card,
            "Save sound settings",
            self.save_preferences,
            primary=True
        ).pack(anchor="e")

        if not self.sound_items:

            self.sound_status.configure(
                text=(
                    "No audio files found. Add WAV, OGG, "
                    "or MP3 files to assets/sounds."
                )
            )

    def preview_sound(self):

        if not self.sound_map:

            messagebox.showwarning(
                "No Sounds Available",
                "Add audio files to your assets/sounds folder first.",
                parent=self
            )

            return

        sound_name = self.selected_sound_var.get()
        sound_id = self.sound_map.get(sound_name)

        if not sound_id:
            return

        try:

            sound_manager.set_volume(
                self.volume_var.get() / 100
            )

            sound_manager.preview(sound_id)

            self.sound_status.configure(
                text=f"Previewing: {sound_name}"
            )

        except Exception as error:

            messagebox.showerror(
                "Sound Error",
                str(error),
                parent=self
            )

    def stop_sound(self):

        try:
            sound_manager.stop()
        except Exception:
            pass

        self.sound_status.configure(
            text="Sound preview stopped."
        )

    def change_volume(self, value):

        try:

            volume = float(value) / 100

            sound_manager.set_volume(volume)

        except Exception as error:
            print("Volume error:", error)

    # ======================================================
    # REUSABLE SETTING ROW
    # ======================================================

    def setting_row(
        self,
        parent,
        title,
        description,
        variable
    ):

        row = tk.Frame(
            parent,
            bg=self.color("card")
        )

        row.pack(fill="x")

        info = tk.Frame(
            row,
            bg=self.color("card")
        )

        info.pack(
            side="left",
            fill="x",
            expand=True
        )

        self.label(
            info,
            title,
            font=("Arial", 10, "bold"),
            bg=self.color("card")
        ).pack(anchor="w")

        self.label(
            info,
            description,
            font=("Arial", 9),
            fg=self.color("muted"),
            bg=self.color("card")
        ).pack(
            anchor="w",
            pady=(3, 0)
        )

        tk.Checkbutton(
            row,
            variable=variable,
            command=self.save_preferences,
            bg=self.color("card"),
            activebackground=self.color("card"),
            selectcolor=self.color("accent_light"),
            fg=self.color("primary"),
            cursor="hand2"
        ).pack(
            side="right",
            padx=(10, 0)
        )

    # ======================================================
    # DATA MANAGEMENT
    # ======================================================

    def build_data_section(self):

        self.section_heading(
            self.container,
            "Data management",
            "Manage your locally saved alarm information."
        )

        card = self.section_card(self.container)

        card.pack(
            fill="x",
            padx=35,
            pady=(0, 23)
        )

        info = tk.Frame(
            card,
            bg=self.color("card")
        )

        info.pack(
            side="left",
            fill="x",
            expand=True
        )

        self.label(
            info,
            "Clear saved alarms",
            font=("Arial", 10, "bold"),
            bg=self.color("card")
        ).pack(anchor="w")

        self.label(
            info,
            "Remove all alarms saved on this device.",
            font=("Arial", 9),
            fg=self.color("muted"),
            bg=self.color("card")
        ).pack(
            anchor="w",
            pady=(3, 0)
        )

        self.styled_button(
            card,
            "Clear alarms",
            self.clear_alarms
        ).pack(side="right")

    def clear_alarms(self):

        confirmed = messagebox.askyesno(
            "Clear All Alarms",
            (
                "Are you sure you want to delete all saved alarms?\n\n"
                "This action cannot be undone."
            ),
            parent=self
        )

        if not confirmed:
            return

        try:

            with open(
                ALARM_FILE,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump([], file, indent=4)

            messagebox.showinfo(
                "Alarms Cleared",
                "All saved alarms have been cleared.",
                parent=self
            )

        except OSError as error:

            messagebox.showerror(
                "Error",
                f"Could not clear alarms:\n{error}",
                parent=self
            )

    # ======================================================
    # ABOUT
    # ======================================================

    def build_about(self):

        card = tk.Frame(
            self.container,
            bg=self.color("panel"),
            highlightbackground=self.color("border"),
            highlightthickness=1,
            padx=20,
            pady=18
        )

        card.pack(
            fill="x",
            padx=35,
            pady=(0, 35)
        )

        self.label(
            card,
            "✿  ORIRI",
            font=("Georgia", 17, "bold"),
            fg=self.color("primary"),
            bg=self.color("panel")
        ).pack(anchor="w")

        self.label(
            card,
            "A quieter start to every day.",
            font=("Arial", 9, "italic"),
            fg=self.color("muted"),
            bg=self.color("panel")
        ).pack(
            anchor="w",
            pady=(4, 8)
        )

        self.label(
            card,
            "Version 1.0  •  Botanical Garden Edition",
            font=("Arial", 8),
            fg=self.color("muted"),
            bg=self.color("panel")
        ).pack(anchor="w")

    # ======================================================
    # SAVE PREFERENCES
    # ======================================================

    def save_preferences(self):

        self.settings["time_format"] = self.time_var.get()

        self.settings["default_enabled"] = (
            self.default_var.get()
        )

        self.settings["sound_enabled"] = (
            self.sound_var.get()
        )

        self.settings["notifications_enabled"] = (
            self.notification_var.get()
        )

        self.settings["volume"] = self.volume_var.get()

        selected_name = self.selected_sound_var.get()

        self.settings["default_sound"] = (
            self.sound_map.get(
                selected_name,
                self.settings.get("default_sound", "")
            )
        )

        try:

            sound_manager.set_volume(
                self.volume_var.get() / 100
            )

        except Exception:
            pass

        try:

            save_settings(self.settings)

        except OSError as error:

            messagebox.showerror(
                "Settings Error",
                f"Could not save settings:\n{error}",
                parent=self
            )

    # ======================================================
    # CLEANUP
    # ======================================================

    def destroy(self):

        try:
            sound_manager.stop()
        except Exception:
            pass

        super().destroy()


# ==========================================================
# END OF SETTINGS PAGE
# ==========================================================
