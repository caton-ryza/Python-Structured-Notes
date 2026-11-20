
import json
from pathlib import Path


# ==========================================================
# ORIRI THEME MANAGER
# Central theme settings for the entire application
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
SETTINGS_FILE = DATA_DIR / "settings.json"


THEMES = {

    "Rosé Garden": {
        "background": "#F6E6E8",
        "background_alt": "#FBEFF0",
        "sidebar": "#DFAEB9",
        "sidebar_light": "#F1D4D9",
        "card": "#FFF8F6",
        "card_alt": "#F9E9E9",
        "surface": "#F5DDDF",
        "primary": "#A85F73",
        "secondary": "#C98C9B",
        "accent": "#E5A6B3",
        "accent_light": "#F3D0D6",
        "text": "#573B43",
        "muted": "#9B777F",
        "border": "#EACBD1",
        "flower": "#D98FA0",
        "success": "#78977B"
    },

    "Meadow": {
        "background": "#E8F0E7",
        "background_alt": "#F1F6EF",
        "sidebar": "#A9C7B1",
        "sidebar_light": "#D5E5D5",
        "card": "#F8FAF5",
        "card_alt": "#EDF4EB",
        "surface": "#DCEADB",
        "primary": "#47775D",
        "secondary": "#80A68A",
        "accent": "#9DBFA3",
        "accent_light": "#D5E5D5",
        "text": "#294B3B",
        "muted": "#789381",
        "border": "#D0E0D0",
        "flower": "#D9B9A9",
        "success": "#668B6B"
    },

    "Ocean": {
        "background": "#E5EFF3",
        "background_alt": "#F0F6F8",
        "sidebar": "#A9C9D5",
        "sidebar_light": "#D4E8ED",
        "card": "#F8FCFD",
        "card_alt": "#EAF4F7",
        "surface": "#D8EAF0",
        "primary": "#477D91",
        "secondary": "#78A9B9",
        "accent": "#8CC5D0",
        "accent_light": "#D0EAF0",
        "text": "#315363",
        "muted": "#7899A5",
        "border": "#C9DFE6",
        "flower": "#A9CAD6",
        "success": "#6D9B91"
    },

    "Linen": {
        "background": "#F1EBDD",
        "background_alt": "#F8F4EA",
        "sidebar": "#D8C7A8",
        "sidebar_light": "#EDE1CB",
        "card": "#FFFCF5",
        "card_alt": "#F5EFDF",
        "surface": "#EDE3D0",
        "primary": "#92744D",
        "secondary": "#B69B73",
        "accent": "#C8AA7C",
        "accent_light": "#EDE0C6",
        "text": "#554735",
        "muted": "#99876E",
        "border": "#E2D6BF",
        "flower": "#D6B99B",
        "success": "#82916B"
    },

    "Mist": {
        "background": "#ECEAF3",
        "background_alt": "#F5F3F9",
        "sidebar": "#C3BCD9",
        "sidebar_light": "#E1DCEE",
        "card": "#FBFAFE",
        "card_alt": "#F0EDF7",
        "surface": "#E4DFF0",
        "primary": "#766B9D",
        "secondary": "#A49AC4",
        "accent": "#B7ACD9",
        "accent_light": "#E3DCF3",
        "text": "#49445F",
        "muted": "#89839F",
        "border": "#DCD6EB",
        "flower": "#C2B5DF",
        "success": "#7D9B8C"
    }
}


DEFAULT_THEME = "Rosé Garden"


class ThemeManager:

    def __init__(self, root):

        self.root = root
        self.current_theme = DEFAULT_THEME
        self.listeners = []

        DATA_DIR.mkdir(parents=True, exist_ok=True)

        self.load_theme()
        self.apply_root_theme()

    # ------------------------------------------------------
    # THEME ACCESS
    # ------------------------------------------------------

    @property
    def colors(self):
        return THEMES[self.current_theme]

    def get_color(self, color_name):
        return self.colors.get(color_name, "#FFFFFF")

    def get_all_themes(self):
        return THEMES

    # ------------------------------------------------------
    # LOAD AND SAVE
    # ------------------------------------------------------

    def load_theme(self):

        if not SETTINGS_FILE.exists():
            self.save_settings()
            return

        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
                settings = json.load(file)

            saved_theme = settings.get("theme", DEFAULT_THEME)

            if saved_theme in THEMES:
                self.current_theme = saved_theme

        except (json.JSONDecodeError, OSError):
            self.current_theme = DEFAULT_THEME

    def save_settings(self):

        settings = {}

        if SETTINGS_FILE.exists():
            try:
                with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
                    settings = json.load(file)
            except (json.JSONDecodeError, OSError):
                settings = {}

        settings["theme"] = self.current_theme

        with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
            json.dump(settings, file, indent=4)

    # ------------------------------------------------------
    # CHANGE THEME
    # ------------------------------------------------------

    def set_theme(self, theme_name):

        if theme_name not in THEMES:
            return

        if self.current_theme == theme_name:
            return

        self.current_theme = theme_name

        self.save_settings()
        self.apply_root_theme()
        self.notify_listeners()

    # ------------------------------------------------------
    # APPLY ROOT COLORS
    # ------------------------------------------------------

    def apply_root_theme(self):

        colors = self.colors

        self.root.configure(bg=colors["background"])

    # ------------------------------------------------------
    # PAGE LISTENERS
    # ------------------------------------------------------

    def subscribe(self, callback):

        if callback not in self.listeners:
            self.listeners.append(callback)

    def unsubscribe(self, callback):

        if callback in self.listeners:
            self.listeners.remove(callback)

    def notify_listeners(self):

        for callback in self.listeners[:]:
            try:
                callback(self.colors)
            except Exception as error:
                print("Theme update error:", error)

    # ------------------------------------------------------
    # WIDGET COLOR HELPER
    # ------------------------------------------------------

    def style_frame(self, widget, color="card"):

        widget.configure(
            bg=self.get_color(color)
        )

    def style_label(
        self,
        widget,
        background="card",
        foreground="text"
    ):

        widget.configure(
            bg=self.get_color(background),
            fg=self.get_color(foreground)
        )
